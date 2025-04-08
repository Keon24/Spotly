from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

# note similar to nodejs validator
# Get custom user model
User = get_user_model()

# Convert user model into JSON
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name"]

# Register serializer to handle user creation
class RegisterSerializer(serializers.ModelSerializer):
    # User is required to have matching passwords 
    password = serializers.CharField(write_only=True,validate=validate_password)
    password2 = serializers.CharField(write_only =True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "password"]
        
    # Here we take the data form JSON and compare passwords to see if they match
    def validate(self,attrs):
       if attrs["password"] != attrs["password2"]:
           raise serializers.ValidationError({"message:","passswords do not match"})
       return attrs
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
        try:   
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
    
        if not user.check_password(password):
            raise serializers.ValidationError("invalid username or password")
        
        if not user.is_active:
            raise serializers.ValidationError("kicked out for inactivity")
        
        
        refresh = RefreshToken.for_user(user)
            # Return user details and JWT tokens
        return {
       "user": UserSerializer(user).data,  # Fixed user.data issue
       "access_token": str(refresh.access_token),
       "token": str(refresh),
       
        }

    
