from django.conf.urls import url, include
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from signup.views import SignupViewCreate, ValidateSignupDetail

router = DefaultRouter()
#router.register(r'create', SignupViewSet, base_name='signup')

urlpatterns = [
  url(r'^', SignupViewCreate.as_view()),
  url(r'^validate/(?P<auth>\d+_\w+)/$', ValidateSignupDetail.as_view()),
]
