from rest_framework import viewsets, permissions, mixins, serializers
from signup.serializers import SignupSerializer, UserEmailSerializer
from signup.models import UserAuthenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

import string
import random

# Create your views here.
class UserCreate(APIView):
  """
  API endpoint that allows users to be added
  """
  permission_classes = (permissions.AllowAny,)
  # TODO enable this when not testing
#  throttle_scope = 'users'

  def get_object(self, auth_path):
    try:
      return UserAuthenticate.objects.get(auth_path=auth_path)
    except UserAuthenticate.DoesNotExist:
      raise serializers.ValidationError('Invalid Validation Link')

  def get(self, request, format=None):
    """
    Checks to see if auth_path exists and if so makes the user active.
    E-mail verification basically.
    """
    auth_path = self.request.query_params.get('auth_path', None)
    user_auth = self.get_object(auth_path)
    user_auth.user.is_active = True
    user_auth.user.save()
    serializer = SignupSerializer(user_auth.user)
    # don't send the password back to the client
    user_auth.delete()
    return Response(serializer.data)

  # POST handler
  def post(self, request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(): #TODO add error handling
      user = serializer.save()
      auth_path = "{:s}_{:s}".format(str(user.id), ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)))
      auth = UserAuthenticate(user=user, auth_path=auth_path)
      auth.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
