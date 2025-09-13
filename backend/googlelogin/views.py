from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from job_tracker.serializers import UserSerializer

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