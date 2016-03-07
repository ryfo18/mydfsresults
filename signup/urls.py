from django.conf.urls import url, include
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from signup.views import UserCreate

router = DefaultRouter()
#router.register(r'create', SignupViewSet, base_name='signup')

urlpatterns = [
  url(r'^', UserCreate.as_view()),
]
