import base64
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialToken, SocialApp

def get_gmail_service(user):
    """
    Creates a Gmail API service object for the given user.
    
    Args:
        user: The Django user to get the service for
        
    Returns:
        A Gmail API service object or None if no valid credentials
    """
    try:
        # Get token for the user
        social_token = SocialToken.objects.get(account__user=user, account__provider='google')
        social_app = SocialApp.objects.get(provider='google')
        
        # Create credentials
        credentials = Credentials(
            token=social_token.token,
            refresh_token=social_token.token_secret,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=social_app.client_id,
            client_secret=social_app.secret,
            scopes=['https://www.googleapis.com/auth/gmail.readonly']
        )
        
        # Return the Gmail service
        return build('gmail', 'v1', credentials=credentials)
    except Exception as e:
        print(f"Error creating Gmail service: {e}")
        return None

def get_recent_messages(service, max_results=5):
    """
    Gets the most recent emails from the user's inbox.
    
    Args:
        service: The Gmail API service object
        max_results: Maximum number of messages to return
        
    Returns:
        A list of message objects with parsed content
    """
    try:
        # Get the list of messages
        results = service.users().messages().list(
            userId='me', maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        parsed_messages = []
        
        for msg in messages:
            message = service.users().messages().get(
                userId='me', id=msg['id'], format='full'
            ).execute()
            
            # Extract headers we care about
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'].lower() == 'date'), 'Unknown')
            
            # Get snippet
            snippet = message.get('snippet', '')
            
            parsed_messages.append({
                'id': msg['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'snippet': snippet
            })
        
        return parsed_messages
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return []