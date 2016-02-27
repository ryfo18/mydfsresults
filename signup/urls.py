from django.conf.urls import url, include
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from signup.views import SignupViewSet, ValidateSignupViewSet

router = DefaultRouter()
router.register(r'create', SignupViewSet, base_name='signup')
router.register(r'validate', ValidateSignupViewSet, base_name='validate_signup')

urlpatterns = [
  url(r'^', include(router.urls))
]
