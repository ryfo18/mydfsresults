from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings


# Create your tests here.
class SignupTests(APITestCase):
  def test_create_account(self):
    """
    Ensure a new account can be created.
    """
    data = {'email': 'test@test.com'}
    response  = self.client.post('/signup/create/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(get_user_model().objects.count(), 1)
    self.assertEqual(get_user_model().objects.get().email, 'test@test.com')

  def test_create_account_exists(self):
    """
    Ensure a duplicate account can't be created.
    """
    data = {'email': 'test@test.com'}
    self.client.post('/signup/create/', data, format='json')
    response  = self.client.post('/signup/create/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_throttle(self):
    """
    Ensure throttling works for signup API since anyone can post to it.
    """
    throttle = int(settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['signup'].split('/')[0])
    for i in range(throttle + 2):
      data = {'email': 'test' + str(i) + '@test.com'}
      response = response = self.client.post('/signup/create/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
