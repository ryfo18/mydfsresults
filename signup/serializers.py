from rest_framework import serializers
from django.contrib.auth import get_user_model


class SignupSerializer(serializers.ModelSerializer):
  """
  Serializer for creating a new user
  """
  is_active = serializers.BooleanField(default=False, write_only=True)
  class Meta:
    model = get_user_model()
    fields = ('email', 'password', 'is_active')
    extra_kwargs = {
      'password': {'write_only': True}
    }

  def validate_email(self, value):
    """
    Make sure e-mail address isn't already in database.
    """
    if get_user_model().objects.filter(email=value).count():
      raise serializers.ValidationError(value + ' has already been registered.')
    return value

  def create(self, validated_data):
    """
    Return an instance of the new user that is created
    """
    return get_user_model().objects.create(**validated_data)

class UserEmailSerializer(serializers.Serializer):
  """
  This is needed just to return the e-mail address of a user after they have
  validated.
  """
  email = serializers.EmailField(required=True, allow_blank=False, max_length=255)
