from rest_framework import serializers

class SignupSerializer(serializers.Serializer):
  """
  Serializer for creating a new user
  """
  username = serializers.EmailField(required=True, allow_blank=False, max_length=255)
  # key is just a field we'll require the app to add to prevent hijacking
  key = serializers.CharField(required=True, allow_blank=False, max_length=30)
