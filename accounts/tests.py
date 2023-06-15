from django.test import TestCase
from django.urls import resolve, reverse
from .views import signup


class SignUpTests(TestCase):
    def test_signup_status_code(self):
        """tests that the sign up page returns success status"""
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_signup_resolves_signup_view(self):
        """tests that the sign up view / resolves"""
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)
