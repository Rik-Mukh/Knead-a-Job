from __future__ import annotations

import os
import base64
from typing import List, Dict, Optional, Any

from django.utils import timezone
from allauth.socialaccount.models import SocialToken, SocialApp

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ---- Config ----
GMAIL_SCOPE_READONLY = "https://www.googleapis.com/auth/gmail.readonly"
SCOPES = [GMAIL_SCOPE_READONLY]

# ---- Token / Credentials ----
def _load_allauth_credentials(user) -> Optional[Credentials]:
    """
    Build Google OAuth2 Credentials from django-allauth SocialToken + SocialApp.
    Attempts to include refresh_token if available.
    """
    social_token = SocialToken.objects.select_related("account").get(
        account__user=user, account__provider="google"
    )
    social_app = SocialApp.objects.get(provider="google")

    # Many setups store refresh_token in token_secret (Google returns it only once)
    refresh_token = social_token.token_secret or None

    creds = Credentials(
        token=social_token.token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=social_app.client_id,
        client_secret=social_app.secret,
        scopes=SCOPES,
    )
    return creds


def _maybe_refresh_and_persist(user, creds: Credentials) -> Credentials:
    """
    Refresh access token if needed, and persist updated access/expiry/refresh to SocialToken when possible.
    """
    if creds and creds.expired and creds.refresh_token:
        # Refresh in-place
        creds.refresh(Request())

        # Persist back to allauth so future requests don’t break mid-session
        try:
            social_token = SocialToken.objects.select_related("account").get(
                account__user=user, account__provider="google"
            )
            social_token.token = creds.token
            # Google rarely re-issues refresh_token; if present, keep it updated
            if creds.refresh_token:
                social_token.token_secret = creds.refresh_token
            # Store expiry when available
            if creds.expiry:
                social_token.expires_at = timezone.make_aware(creds.expiry) if timezone.is_naive(creds.expiry) else creds.expiry
            social_token.save(update_fields=["token", "token_secret", "expires_at"])
        except Exception:
            # If persisting fails, keep going with refreshed creds
            pass

    return creds


def get_gmail_service(user):
    """
    Authenticated Gmail API service for a given Django user (django-allauth).
    Refreshes tokens when expired and persists updates.
    """
    try:
        creds = _load_allauth_credentials(user)
        if not creds:
            return None
        creds = _maybe_refresh_and_persist(user, creds)
        return build("gmail", "v1", credentials=creds)
    except SocialToken.DoesNotExist:
        return None
    except SocialApp.DoesNotExist:
        return None
    except Exception:
        return None


# ---- Helpers (match your preferred script) ----
def list_message_ids(service, q: str = "", max_results: int = 10) -> List[Dict]:
    """
    Search using Gmail's query language (e.g., 'in:inbox newer_than:7d subject:invoice')
    Returns minimal [{id, threadId}...] dicts.
    """
    resp = service.users().messages().list(userId="me", q=q, maxResults=max_results).execute()
    return resp.get("messages", [])


def get_headers_map(headers_list) -> Dict[str, str]:
    return {h.get("name", "").lower(): h.get("value", "") for h in headers_list or []}


def b64url_decode(s: str) -> str:
    if not s:
        return ""
    return base64.urlsafe_b64decode(s).decode("utf-8", errors="ignore")


def extract_bodies(payload) -> Dict[str, str]:
    """
    Recursively walk MIME tree to extract text/plain and text/html bodies.
    """
    out = {"text": "", "html": ""}

    def walk(part):
        mime = part.get("mimeType", "")
        body = part.get("body", {}) or {}
        data = body.get("data", "")

        if mime == "text/plain" and data and not out["text"]:
            out["text"] = b64url_decode(data)
        elif mime == "text/html" and data and not out["html"]:
            out["html"] = b64url_decode(data)

        for sub in part.get("parts", []) or []:
            walk(sub)

        # Fallback: single-part messages sometimes put content directly in body.data
        if not part.get("parts") and data and not (out["text"] or out["html"]):
            out["text"] = b64url_decode(data)

    if payload:
        walk(payload)
    return out


def fetch_messages(service, ids: List[Dict], save_html: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch full messages and return normalized dicts:
    { id, from, date, subject, text_body, html_body, html_file? }
    """
    if not ids:
        return []

    messages = []
    for i, m in enumerate(ids, start=1):
        msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        payload = msg.get("payload", {})
        hdrs = get_headers_map(payload.get("headers", []))
        bodies = extract_bodies(payload)

        from_h = hdrs.get("from", "")
        date_h = hdrs.get("date", "")
        subj_h = hdrs.get("subject", "")
        text_body = (bodies["text"] or "").strip()
        html_body = (bodies["html"] or "").strip()

        item = {
            "id": m["id"],
            "from": from_h,
            "date": date_h,
            "subject": subj_h,
            "text_body": text_body,
            "html_body": html_body,
        }

        if save_html and html_body:
            fn = f"message_{i}.html"
            with open(fn, "w", encoding="utf-8") as f:
                f.write(html_body)
            item["html_file"] = fn

        messages.append(item)

    return messages


# ---- Public API: match the "better" script's shape ----
def get_emails(user, query: str = "in:inbox newer_than:7d", max_results: int = 5, save_html: bool = False) -> Dict[str, Any]:
    """
    High-level: authenticate (django-allauth), search, fetch, and return normalized payload.
    """
    try:
        service = get_gmail_service(user)
        if service is None:
            return {
                "success": False,
                "count": 0,
                "messages": [],
                "error": "No valid Google credentials for this user.",
            }

        ids = list_message_ids(service, q=query, max_results=max_results)
        messages = fetch_messages(service, ids, save_html=save_html)

        return {
            "success": True,
            "count": len(messages),
            "messages": messages,
        }
    except Exception as e:
        return {
            "success": False,
            "count": 0,
            "messages": [],
            "error": str(e),
        }
