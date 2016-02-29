from rest_framework import viewsets, permissions, mixins, serializers
from signup.serializers import SignupSerializer
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from signup.models import UserAuthenticate
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_jwt.settings import api_settings

import random
import string

# Create your views here.
class SignupViewCreate(CreateAPIView):
  """
  API endpoint that allows users to be added
  """
  serializer_class = SignupSerializer
  permission_classes = (permissions.AllowAny,)
  throttle_scope = 'signup'

  # POST handler
  def post(self, request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(): #TODO add error handling
      temp_pw = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
      try:
        u = get_user_model().objects.create(email=serializer.data['email'], password=temp_pw, is_active=False)
        u.save()
      except IntegrityError:
        content = {"errors": {"email": serializer.data['email'] + " has already been registered."} }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

      user = get_user_model().objects.get(email=serializer.data['email'])
      auth_path = "{:s}_{:s}".format(str(user.id), ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)))
      auth = UserAuthenticate(user=user, auth_path=auth_path)
      auth.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      #TODO send e-mail w/ link

class ValidateSignupDetail(APIView):
  """
  API endpoint for signup confirmation.
  """
  permission_classes = (permissions.AllowAny,)
  renderer_classes = (JSONRenderer,)
  # TODO Need to have a throttle on this for sure
#  throttle_scope = 'validate-signup'

  def get(self, request, auth, format=None):
    print(auth)
    query = UserAuthenticate.objects.filter(auth_path=auth)
    if query.count() != 1:
      content = {'user_validation': 'validation link not found'}
      print('HERE')
      return Response(content, status=status.HTTP_204_NO_CONTENT)
    else:
      print(query[0].user)
      get_user_model().objects.filter(email=query[0].user).update(is_active=True)
      user = get_user_model().objects.get(email=query[0].user)
      query.delete()
      jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
      jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
      payload = jwt_payload_handler(user)
      return Response({'token': jwt_encode_handler(payload)})
