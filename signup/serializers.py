from rest_framework import serializers
from django.contrib.auth import get_user_model
from signup.models import UserAuthenticate

import string
import random

class SignupSerializer(serializers.Serializer):
  """
  Serializer for creating a new user
  """
  email = serializers.EmailField(required=True, allow_blank=False, max_length=255)
  password = serializers.CharField(required=True, allow_blank=False, max_length=255, style={'input_type': 'password'})

  def validate_email(self, value):
    """
    Make sure e-mail address isn't already in database.
    """
    if get_user_model().objects.filter(email=value).count():
      raise serializers.ValidationError(value + ' has already been registered.')
    return value

  def save(self):
    """
    Save the results to the database and create a verification link
    """
    user = get_user_model().objects.create(email=self.data['email'], password=self.data['password'], is_active=False)
    user.save()

    auth_path = "{:s}_{:s}".format(str(user.id), ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)))
    auth = UserAuthenticate(user=user, auth_path=auth_path)
    auth.save()
    #TODO send e-mail w/ link
