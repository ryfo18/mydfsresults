'''
from django.conf.urls import url, include
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from signup.views import SignupViewSet

router = DefaultRouter()
router.register(r'signup', SignupViewSet)

urlpatterns = [
  url(r'^', include(router.urls))
]

'''
