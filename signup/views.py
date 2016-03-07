from rest_framework import viewsets, permissions, mixins, serializers
from signup.serializers import SignupSerializer
from signup.models import UserAuthenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

# Create your views here.
class UserCreate(CreateAPIView):
  """
  API endpoint that allows users to be added
  """
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
  # TODO Need to have a throttle on this for sure
#  throttle_scope = 'validate-signup'

  def get_object(self, auth_path):
    try:
      return UserAuthenticate.objects.get(auth_path=auth_path)
    except UserAuthenticate.DoesNotExist:
      raise Http404

  def get(self, request, format=None):
    auth_path = self.request.query_params.get('auth_path', None)
    print(auth_path)
    user = self.get_object(auth_path)
    print(user.user)
    serializer = SignupSerializer(user.user)
    print(serializer.data)
    return Response(serializer.data)
