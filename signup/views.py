from rest_framework import viewsets, permissions, mixins, serializers
from signup.serializers import SignupSerializer
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_jwt.settings import api_settings

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
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
