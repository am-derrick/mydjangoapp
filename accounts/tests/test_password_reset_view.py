from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class PasswordResetTests(TestCase):
    def setUp(self):
        """initialises password reset tests"""
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        """tests status code success"""
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        """tests view function"""
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, PasswordResetView)

    def test_csrf(self):
        """tests presence of csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """tests that view has password reset form"""
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """tests that view has csrf and email inputs"""
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        """initilaises inavlid password reset testcases"""
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'invalid@email.com'})

    def test_redirection(self):
        """tests that invalid emails redirect to password_reset_done view"""
        redirection_url = reverse('password_reset_done')
        self.assertRedirects(self.response, redirection_url)

    def test_no_reset_email_sent(self):
        """tests that when emailis invalid, no email is sent"""
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        """initialises tests for when password reset is done"""
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        """tests success status code"""
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        """tests password reset done view func"""
        view = resolve('/reset/done/')
        self.assertEquals(view.func.view_class, PasswordResetDoneView)


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        """
        initialises tests for password reset confirmation

        Create a valid password reset token 
        https://github.com/django/django/blob/1.11.5/django/contrib/auth/forms.py -- line 280 & 282
        """
        user = User.objects.create_user(
            username='john', email='john@doe.com', password='123abc')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)
        url = reverse('password_reset_confirm', kwargs={
                      'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        """tests success of view"""
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        """tests view function for password reset confirm"""
        view = resolve(
            '/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, PasswordResetConfirmView)

    def test_contains_csrf(self):
        """tests that view has csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """tests that password rest confirm view has set password form"""
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        """tests the inputs (csrf and two password fields) in the password reset confirm form"""
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        """initialises invalid password reset confirm tests"""
        user = User.objects.create_user(
            username='john', email='john@doe.com', password='123abc')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        user.set_password('456xyz')  # change password to invalidate token
        user.save
        url = reverse('password_reset_confirm', kwargs={
                      'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        """
        tests status code returns 200 when invalid password reset confirm
        invalid reset still returns a 200 status code
        """
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        """tests that when invalid, link to password reset is present"""
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'Password reset link invalid')
        self.assertContains(
            self.response, 'href="{0}"'.format(password_reset_url))


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        """intialises the tests for password reset complete"""
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        """tests success status code"""
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        """tests view function for password reser complete"""
        view = resolve('/reset/complete/')
        self.assertEquals(view.func.view_class, PasswordResetCompleteView)
