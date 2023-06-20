from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import resolve, reverse


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
        """tests that invalide emails redirect to password_reset_done view"""
        redirect_url = reverse('password_reset_done')
        self.assertRedirects(self.response, redirect_url)

    def test_no_reset_email_sent(self):
        """tests that when emailis invalid, no email is sent"""
        self.assertEqual(0, len(mail.outbox))
