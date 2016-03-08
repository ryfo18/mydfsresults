from rest_framework import viewsets, permissions, mixins, serializers
from signup.serializers import SignupSerializer
from signup.models import UserAuthenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

# Create your views here.
class UserCreate(APIView):
  """
  API endpoint that allows users to be added
  """
  permission_classes = (permissions.AllowAny,)
  throttle_scope = 'signup'

  def get_object(self, auth_path):
    try:
      return UserAuthenticate.objects.get(auth_path=auth_path)
    except UserAuthenticate.DoesNotExist:
      raise Http404

  def get(self, request, format=None):
    auth_path = self.request.query_params.get('auth_path', None)
    user_auth = self.get_object(auth_path)
    user_auth.user.is_active = True
    user_auth.user.save()
    serializer = SignupSerializer(user_auth.user)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user_auth.user)
    token = jwt_encode_handler(payload)
    print(token)
    user_auth.delete()
    return Response(serializer.data)

  # POST handler
  def post(self, request):
    serializer = SignupSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid(): #TODO add error handling
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
