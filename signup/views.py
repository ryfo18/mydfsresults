from rest_framework import viewsets, permissions, mixins, serializers
from signup.serializers import SignupSerializer
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from signup.models import UserAuthenticate


import random
import string

# Create your views here.
class SignupViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
  """
  API endpoint that allows users to be added
  """
  serializer_class = SignupSerializer
  permission_classes = (permissions.AllowAny,)

  def perform_create(self, request, *args, **kwargs):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(): #TODO add error handling
      temp_pw = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
      try:
        u = get_user_model().objects.create(email=serializer['username'], password=temp_pw, is_active=False)
        u.save()
      except IntegrityError:
        raise serializers.ValidationError({"username": ["E-mail address has already been registered."]}) 

      user = get_user_model().objects.get(email=serializer['username'])
      print(user.id)
      auth_path = "{:s}_{:s}".format(str(user.id), ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)))
      print(auth_path)
      auth = UserAuthenticate(user=user, auth_path=auth_path)
      auth.save()
      #TODO send e-mail w/ link
