import secrets
import requests
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import login
from django.http import HttpResponseBadRequest, JsonResponse

logger = logging.getLogger(__name__)


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
    try:
        state = request.GET.get("state")
        stored_state = request.session.pop("oauth_state", None)

        # check if state is empty send error to user
        if not stored_state or state != stored_state:
            logger.error(f"Invalid state: stored={stored_state}, received={state}")
            return redirect("https://spotly-frontend-git-main-keon24s-projects.vercel.app/login?error=invalid_state")

        code = request.GET.get("code")
        if not code:
            logger.error("No authorization code received")
            return redirect("https://spotly-frontend-git-main-keon24s-projects.vercel.app/login?error=no_code")

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
            logger.error(f"Token exchange failed: {token_response.text}")
            return redirect("https://spotly-frontend-git-main-keon24s-projects.vercel.app/login?error=token_failed")
        # Extract token from token response
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            logger.error("No access token in response")
            return redirect("https://spotly-frontend-git-main-keon24s-projects.vercel.app/login?error=no_access_token")

        # retrieve user info from google
        userinfo_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"
        userinfo_response = requests.get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if userinfo_response.status_code != 200:
            logger.error(f"Failed to retrieve user info: {userinfo_response.text}")
            return redirect("https://spotly-frontend-git-main-keon24s-projects.vercel.app/login?error=userinfo_failed")

        # extract relevant user info
        data = userinfo_response.json()
        email = data.get("email")
        first_name = data.get("given_name")
        last_name = data.get("family_name")

        if not email:
            logger.error("No email in user info")
            return redirect("https://spotly-frontend-git-main-keon24s-projects.vercel.app/login?error=no_email")

        # get or create user in Django database
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name or '',
                'last_name': last_name or '',
                'is_active': True
            }
        )

        # Update user info if already exists
        if not created:
            user.first_name = first_name or ''
            user.last_name = last_name or ''
            user.save()

        login(request, user)
        logger.info(f"User {email} logged in successfully via Google OAuth")

        # Redirect to frontend dashboard after successful login
        return redirect('https://spotly-frontend-git-main-keon24s-projects.vercel.app/dashboard')

    except Exception as e:
        logger.exception(f"Google OAuth callback error: {str(e)}")
        return redirect(f"https://spotly-frontend-git-main-keon24s-projects.vercel.app/login?error=server_error")