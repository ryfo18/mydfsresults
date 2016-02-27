from rest_framework import serializers

class SignupSerializer(serializers.Serializer):
  """
  Serializer for creating a new user
  """
  email = serializers.EmailField(required=True, allow_blank=False, max_length=255)

class ValidateSignupSerializer(serializers.Serializer):
  """
  Serializer for validating a new user and changing password
  """
  email = serializers.EmailField(required=True, allow_blank=False, max_length=255)
