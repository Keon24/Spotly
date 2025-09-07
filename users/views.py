from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer  
from users.authentication.auth import CookieJWTAuthentication 


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user_data = data['user']
            access_token = data['access_token']
            refresh_token = data['token']

            response = Response({
                'user': user_data,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
            
            # Set HTTP-only cookies for authentication
            response.set_cookie(
                'access_token',
                access_token,
                max_age=30*60,  # 30 minutes
                httponly=True,
                secure=True,  # HTTPS only
                samesite='None'  # Cross-origin cookies
            )
            response.set_cookie(
                'refresh_token', 
                refresh_token,
                max_age=7*24*60*60,  # 7 days
                httponly=True,
                secure=True,
                samesite='None'
            )
            
            return response

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]  

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        return Response(data)

class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

@ensure_csrf_cookie
def csrf_cookie_view(request):
    return JsonResponse({"message": "CSRF cookie set"})
