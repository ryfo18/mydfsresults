from django.db import models
from django.conf import settings

# Create your models here.
class UserAuthenticate(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  auth_path = models.CharField(max_length=40)
