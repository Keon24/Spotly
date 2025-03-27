from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Get custom user model
User = get_user_model()

# Convert user model into JSON
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name"]

# Register serializer to handle user creation
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "password"]

    # Define a function to create and hash the password
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Corrected method
        user.save()
        return user

# Login serializer to validate user credentials
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # Validate and authenticate the user
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            # Return user details and JWT tokens
            return {
                "user": UserSerializer(user).data,  # Fixed user.data issue
                "access_token": str(refresh.access_token),
                "token": str(refresh),
            }

        raise serializers.ValidationError("Invalid email or password")
