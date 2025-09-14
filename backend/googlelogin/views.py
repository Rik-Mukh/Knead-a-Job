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
    return redirect('http://localhost:3000/dashboard')

@login_required
def test_gmail(request):
    """Test view to display recent Gmail messages in the template"""
    messages = []
    error_message = None
    
    try:
        from django.contrib.auth.models import User
        # Use get_emails directly - it handles everything internally
        result = get_emails(
            user=request.user,
            query="in:inbox newer_than:7d",  # Example query to fetch emails from the last 7 days
            max_results=5
        )
        
        if result["success"]:
            messages = result["messages"]
            user, created = User.objects.get_or_create(
                username='halalkingxi',  # This should be your user's username
                defaults={'email': 'rik@ualberta.ca', 'first_name': 'Rik', 'last_name': 'Mukherji'}
            )
            
            from job_tracker.models import Notification, JobApplication
            from django.utils import timezone

            job_app = None
            
            try:
                job_app = JobApplication.objects.first()
            except:
                pass  # No job applications found, will create notification without it
            
            for message in messages:
                # Check if a notification for this email already exists
                existing = Notification.objects.filter(
                    message__contains=message['id']  # Use email ID in message to check for duplicates
                ).first()
                
                if not existing:
                    # print(message.keys())
                    # Create a new notification
                    Notification.objects.create(
                        user=user,
                        job_application=job_app,  # This can be None with our model change
                        title=f"New Email: {message['subject']}",
                        message=f"From: {message['from']}\n\n{message["text_body"][:1000]}\n\nEmail ID: {message['id']}",
                        show_date=timezone.now(),
                        is_read=False,
                        is_active=True
                    )
                    print('creating notification')
                

        else:
            error_message = result.get("error", "Could not connect to Gmail. Please check your permissions.")
    
    except Exception as e:
        error_message = f"Error accessing Gmail: {str(e)}"
        print(f"Error in test_gmail view: {e}")
    
    print(f"Fetched {len(messages)} messages from Gmail.")
    # Return the home template with messages and error context
    return render(request, 'home.html', {
        'messages': messages,
        'error_message': error_message
    })
    
    
"""
Testing Gmail Message Integration
"""
    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  # Change from AllowAny to IsAuthenticated
def get_gmail_messages(request):
    """API endpoint to get Gmail messages for the frontend"""
    print("Starting of get_gmail")
    # print(request.user)
    # return Response({
    #         'success': True,
    #         'error': 'User is authenticated'
    #         }, status=200)
    try:
        # Check if user is authenticated with valid session
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'User not authenticated'
            }, status=401)
            
        result = get_emails(
            user=request.user,
            query="in:inbox newer_than:7d",
            max_results=5
        )
        
        if result["success"]:
            messages = result["messages"]
            return Response({
                'success': True,
                'messages': messages,
                'notifications_created': 0
            })
        else:
            return Response({
                'success': False,
                'error': result.get("error", "Could not connect to Gmail")
            }, status=400)
            
    except Exception as e:
        print(f"Gmail API error: {str(e)}")  # Add logging
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)