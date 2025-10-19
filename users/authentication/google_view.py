import secrets 
import requests
from django.conf import settings 
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import login
from django.http import HttpResponseBadRequest


User = get_user_model()

# User will redirect after login
def google_login_redirect(request):
    state = secrets.token_urlsafe(16)
    request.session['oauth_state'] = state
    
    google_auth_url = ("https://accounts.google.com/o/oauth2/v2/auth"
        f"?response_type=code"
        f"&client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_OAUTH2_REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
        f"&state={state}"
    )
    
    return redirect(google_auth_url)
        

def google_callback(request):
    state = request.GET.get("state")
    stored_state = request.session.pop("oauth_state", None)
    # check if state is empty send error to user 
    if not stored_state or state!= stored_state:
        return redirect("/?error=invalid_state")
    
    code = request.GET.get("code")
    
    
    
    # Exchange auth code for token
    token_endpoint = "https://oauth2.googleapis.com/token"
    token_response = requests.post(
        token_endpoint,
        data={
            "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_OAUTH2_REDIRECT_URI
        }
    )
    
    if token_response.status_code != 200:
        return HttpResponseBadRequest("faied to retrieve token")
    # Extract token fromm token response
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    
    if not access_token:
        return HttpResponseBadRequest("Request failed")

        
    
    # retrieve user info from google 
    userinfo_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"
    userinfo_response = requests.get(
        userinfo_endpoint,
         headers = {"Authorization": f"Bearer {access_token}"}
    )
    if userinfo_response.status_code != 200:
        return HttpResponseBadRequest("Failed to retrieve user info")
    # extra relevant user info
    data = userinfo_response.json()
    email = data.get("email")
    first_name = data.get("given_name")
    last_name = data.get ('family_name')
    # get or create user in Django database
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'is_active': True
        }
    )
    # Update user info if already exists
    if not created:
        user.first_name = first_name
        user.last_name = last_name
        user.save() 
    
    login(request, user)
    # Redirect to frontend dashboard after successful login
    return redirect('https://spotly-frontend-git-main-keon24s-projects.vercel.app/dashboard')