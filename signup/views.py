from rest_framework import viewsets, permissions, mixins, generics
from signup.serializers import SignupSerializer
from django.contrib.auth import get_user_model

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
    print(serializer)
    if serializer.is_valid(): #TODO add error handling
      temp_pw = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
      u = get_user_model().objects.create(email=serializer['username'], password=temp_pw, is_active=False)
      u.save()

      user = get_user_model().objects.filter(email=serializer['username'])
      print(user)
      auth_path = "{%s_%s}".format(str(user.id, ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))))
      auth = UserAuthenticate(user.id, auth_path)
      auth.save()
      #TODO send e-mail w/ link
