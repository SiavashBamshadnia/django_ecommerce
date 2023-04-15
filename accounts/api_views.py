from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts import api_serializers


class RegistrationView(APIView):
    # Create a serializer instance with the request data
    serializer_class = api_serializers.RegistrationSerializer

    def post(self, request):
        serializer = api_serializers.RegistrationSerializer(data=request.data)

        # If the data is not valid, return a response with the errors and an HTTP status code of 400 (Bad Request)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If the data is valid, save the serializer and create a new user instance
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
