from django.test import TestCase

from django.urls import reverse
from .models import User


class AuthorListViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(name='testuser1', password='1X<ISRUkw+tuK',
                                              email="gsh@shs.com",
                                              phone=123222222)
        test_user2 = User.objects.create_user(name='testuser2', password='2HJ1vRV0Z&3iD',
                                              email="gsdhh@shs.com",
                                              phone=12322243222)

        test_user1.save()
        test_user2.save()

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_user_register(self):
        response = self.client.get(reverse('user_register'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_validation_form(self):
        response = self.client.get(reverse('validation-form'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_user_register(self):
        response = self.client.get(reverse('user_register'))
        self.assertTemplateUsed(response, 'user/user_register.html')
