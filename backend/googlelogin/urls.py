from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("api/auth/status/", views.get_auth_status, name="auth_status"),
    path("api/auth/csrf-token/", views.get_csrf_token, name="csrf_token"),
    path("auth-success/", views.auth_success, name="auth_success"),
    path("test-gmail/", views.test_gmail, name="test_gmail"),
    path("api/gmail/messages/", views.get_gmail_messages, name="get_gmail_messages"),  # New endpoint

]