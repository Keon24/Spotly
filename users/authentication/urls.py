from django.urls import path
from .google_view import google_callback, google_login_redirect



urlpatterns = [
    path('callback/', google_callback, name='google-callback'),
    path('redirect/', google_login_redirect, name='google-redirect'),


]
