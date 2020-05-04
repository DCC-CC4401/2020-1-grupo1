import pytest

from django.urls import reverse


# View testing. Simply test if the views are working.


def test_register_not_logged_user_view(client):
   url = reverse('registerUser')
   response = client.get(url)
   assert response.status_code == 200

def test_login_not_logged_view(client):
   url = reverse('login')
   response = client.get(url)
   assert response.status_code == 200

def test_home_logged_user_view(admin_client):
   url = reverse('home')
   response = admin_client.get(url)
   assert response.status_code == 200

def test_edit_profile_logged_user_view(admin_client):
   url = reverse('edit')
   response = admin_client.get(url)
   assert response.status_code == 200

def test_edit_password_logged_user_view(admin_client):
   url = reverse('editPassword')
   response = admin_client.get(url)
   assert response.status_code == 200

