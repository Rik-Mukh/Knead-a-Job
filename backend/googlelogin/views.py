from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from job_tracker.serializers import UserSerializer
from .gmail_service import get_gmail_service, get_recent_messages

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
    try:
        # Get Gmail service for the user
        service = get_gmail_service(request.user)
        
        if service:
            # Get recent messages
            messages = get_recent_messages(service)
    except Exception as e:
        print(f"Error in test_gmail view: {e}")
    
    # Return the home template with messages as context
    return render(request, 'home.html', {'messages': messages})