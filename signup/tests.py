from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class SignupTests(APITestCase):
  def test_create_account(self):
    """
    Ensure a new account can be created.
    """
    data = {'username': 'test@test.com'}
    response  = self.client.post('/signup/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(get_user_model().objects.count(), 1)
    self.assertEqual(get_user_model().objects.get().username, 'test@test.com')
