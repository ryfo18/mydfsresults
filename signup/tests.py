from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings
from signup.models import UserAuthenticate


# Create your tests here.
class SignupTests(APITestCase):
  def test_create_account(self):
    """
    Ensure a new account can be created.
    """
    data = {'email': 'test@test.com', 'password': 'testpass'}
    response  = self.client.post('/api/users/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(get_user_model().objects.count(), 1)
    self.assertEqual(get_user_model().objects.get().email, 'test@test.com')
    self.assertEqual(get_user_model().objects.get().is_active, False)

  def test_create_account_exists(self):
    """
    Ensure a duplicate account can't be created.
    """
    data = {'email': 'test@test.com', 'password': 'testpass'}
    self.client.post('/api/users/', data, format='json')
    response  = self.client.post('/api/users/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_validate_account(self):
    """
    Ensure a new account can be validated.
    """
    data = {'email': 'test@test.com', 'password': 'testpass'}
    response  = self.client.post('/api/users/', data, format='json')
    self.assertEqual(get_user_model().objects.get().email, 'test@test.com')
    self.assertEqual(get_user_model().objects.count(), 1)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(get_user_model().objects.get().is_active, False)

    auth_path = UserAuthenticate.objects.get().auth_path
    response = self.client.get('/api/users/?auth_path=' + auth_path)
    self.assertEqual(get_user_model().objects.get().is_active, True)
    self.assertEqual(UserAuthenticate.objects.count(), 0)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.data)

  def test_bad_validate_link(self):
    """
    Ensure a new account can be created.
    """
    response = self.client.get('/api/users/?auth_path=31_bad')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_throttle(self):
    """
    Ensure throttling works for signup API since anyone can post to it.
    """
    throttle = int(settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['users'].split('/')[0])
    for i in range(throttle + 2):
      data = {'email': 'test' + str(i) + '@test.com'}
      response = response = self.client.post('/api/users/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
