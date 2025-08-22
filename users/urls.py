from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, LogoutView, csrf_cookie_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csrf/', csrf_cookie_view, name='csrf-cookie'),
]
