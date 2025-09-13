from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("auth-success/", views.auth_success, name="auth_success"),
    path("api/auth/status/", views.get_auth_status, name="auth_status"),
]