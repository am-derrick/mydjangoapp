from django.test import TestCase
from django.urls import resolve, reverse
from .views import signup
from django.contrib.auth.forms import UserCreationForm


class SignUpTests(TestCase):
    def setUp(self):
        """initialises sign up tests"""
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        """tests that the sign up page returns success status"""
        self.assertEquals(self.response.status_code, 200)

    def test_signup_resolves_signup_view(self):
        """tests that the sign up view / resolves"""
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        """tests crsf token presence"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """tests that sign up page contains form"""
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)
