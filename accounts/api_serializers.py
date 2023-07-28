from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from accounts import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = models.User
        fields = ('name', 'sex', 'birth_date', 'phone_number', 'password')

    def validate(self, attrs):
        # Create a User instance from the validated data
        user = models.User(attrs)

        errors = dict()

        # Get the password from the input data
        password = attrs['password']

        try:
            # Validate the password and catch any validation errors
            validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        # Call the parent validate method to validate any other fields
        return super().validate(attrs)

    def save(self, **kwargs):
        user = models.User.objects.create_user(**self.validated_data)
        return user
