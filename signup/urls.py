from django.conf.urls import url, include
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from signup.views import UserCreate, ValidateSignupDetail

router = DefaultRouter()
#router.register(r'create', SignupViewSet, base_name='signup')

urlpatterns = [
  url(r'^\?auth_path=\w+/$', ValidateSignupDetail.as_view()),
  url(r'^', UserCreate.as_view()),
]
