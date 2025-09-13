from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

def home(request):
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)
    return redirect('http://localhost:3000/login')

def auth_success(request):
    """Redirect authenticated users back to React frontend"""
    # Generate token or use session as needed
    return redirect('http://localhost:3000/auth-success')

@ensure_csrf_cookie
def get_auth_status(request):
    """Return authentication status and user info for frontend"""
    if request.user.is_authenticated:
        return JsonResponse({
            'isAuthenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        })
    return JsonResponse({'isAuthenticated': False})