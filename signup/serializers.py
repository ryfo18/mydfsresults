from rest_framework import serializers

class SignupSerializer(serializers.Serializer):
  """
  Serializer for creating a new user
  """
  email = serializers.EmailField(required=True, allow_blank=False, max_length=255)
