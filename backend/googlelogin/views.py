from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from job_tracker.serializers import UserSerializer
from .gmail_service import get_gmail_service, get_emails  # Changed from get_recent_messages
def home(request):
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)
    return JsonResponse({'success': True})

@ensure_csrf_cookie
def get_auth_status(request):
    """Return authentication status and user info for frontend"""
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return JsonResponse({
            'isAuthenticated': True,
            'user': serializer.data
        })
    return JsonResponse({'isAuthenticated': False})

def get_csrf_token(request):
    """Return CSRF token for the frontend"""
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

def auth_success(request):
    """Handle successful Google authentication"""
    return redirect('http://localhost:3000/auth-success')

@login_required
def test_gmail(request):
    """Test view to display recent Gmail messages in the template"""
    messages = []
    error_message = None
    
    try:
        # Use get_emails directly - it handles everything internally
        result = get_emails(
            user=request.user,
            query="in:inbox", 
            max_results=10
        )
        
        if result["success"]:
            messages = result["messages"]
        else:
            error_message = result.get("error", "Could not connect to Gmail. Please check your permissions.")
    
    except Exception as e:
        error_message = f"Error accessing Gmail: {str(e)}"
        print(f"Error in test_gmail view: {e}")
    
    print(f"Fetched {len(messages)} messages from Gmail.")
    print(messages)
    # Return the home template with messages and error context
    return render(request, 'home.html', {
        'messages': messages,
        'error_message': error_message
    })