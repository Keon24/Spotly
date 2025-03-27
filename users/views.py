from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import RegisterSerializer, LoginSerializer 
# IMPLEMENT APPLICATION SECURITY PRACTICES

#create a class registerview that takes in api
class RegisterView(APIView):
# create a function that makes a post request and pass the incoming data to the serializer 
    def post (self, request):
        serializer = RegisterSerializer( data=request.data)
#validate the serializer 
        if serializer.is_valid():
# save the serializer 
            user = serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
          

            
            
class LoginSerializer(APIView):
    def post(self,request):
        serializer = LoginSerializer(data= request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.validate_data, status=status.HTTP_201_OK)
        return Response(serializer.errors,status=status.HTTP_401_UNATHORIZED)
            
                       


