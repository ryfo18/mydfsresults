from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from signup.serializers import SignupSerializer
from django.contrib.auth import get_user_model

import random
import string

# Create your views here.
class SignupViewSet(APIView):
  """
  API endpoint that allows users to be added
  """
  serializer_class = SignupSerializer
  permission_classes = (permissions.AllowAny,)

  def perform_create(self, serializer):
    if serializer.is_valid(): #TODO add error handling
      auth_path = "{%s_%s}.format(str(user.pk, ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)))"
      u = get_user_model(email=serializer.object.username, password=auth_path, is_active=False)
      u.save()

      user = get_user_model().filter(email=serializer.object.username)
      auth = UserAuthenticate(user.pk, auth_path)
      auth.save()
      #TODO send e-mail w/ link
