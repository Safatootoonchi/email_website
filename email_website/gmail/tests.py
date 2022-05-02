from django.test import TestCase
from django.urls import reverse
from user.models import User
from .models import *


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

    def test_view_url_accessible_by_name_sent(self):
        response = self.client.get(reverse('sent'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_search_email(self):
        response = self.client.get(reverse('search_email'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_search_contact(self):
        response = self.client.get(reverse('search_contact'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_trash(self):
        response = self.client.get(reverse('trash'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_csv(self):
        response = self.client.get(reverse('csv'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_test(self):
        response = self.client.get(reverse('test'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_draft(self):
        response = self.client.get(reverse('draft'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_archive(self):
        response = self.client.get(reverse('trash'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_trash_detail(self):
        response = self.client.get('/email/trash-detail/<int:10000000>/')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_trash_detail_archive_detail(self):
        response = self.client.get('/email/archive-detail/<int:10000000>/')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_trash_detail_draft_detail(self):
        response = self.client.get('/email/draft-detail/<int:10000000>/')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_trash_detail_delete_sign(self):
        response = self.client.get('/email/delete-sign/<int:10000000>/')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_trash_detail_signature_detail(self):
        response = self.client.get('/email/signature-detail/<int:10000000>/')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_trash_detail_contact_detail(self):
        response = self.client.get('/email/contact-detail/<int:10000000>/')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_trash_detail_label_detail(self):
        response = self.client.get('/email/detail-label/<int:10000000>/')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_trash_detail_email_detail_sent(self):
        response = self.client.get('/email/detail-send/<int:10000000>/')
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template_draft(self):
        response = self.client.get(reverse('draft'))
        self.assertTemplateUsed(response, 'gmail/draft.html')

    def test_view_uses_correct_template_sent(self):
        response = self.client.get(reverse('sent'))
        self.assertTemplateUsed(response, 'gmail/sent.html')

    def test_view_uses_correct_template_trash(self):
        response = self.client.get(reverse('trash'))
        self.assertTemplateUsed(response, 'gmail/trash.html')

    def test_logged_in_uses_correct_template_home(self):
        login = self.client.login(name='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'), follow=True)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_logged_in_uses_correct_template_sign(self):
        login = self.client.login(name='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('signature_list'), follow=True)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
