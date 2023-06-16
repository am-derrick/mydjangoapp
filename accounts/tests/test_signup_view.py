from django.test import TestCase
from django.urls import resolve, reverse
from ..views import signup
from django.contrib.auth.models import User
from ..forms import SignUpForm


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
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        """
        tests the input accepted in the sign up form
        must contain username, email, password1, password2, crsf token
        """
        self.assertContains(self.response, 'type="text" ', 1)
        self.assertContains(self.response, 'type="email" ', 1)
        self.assertContains(self.response, 'type="password"', 2)
        self.assertContains(self.response, '<input', 5)


class SuccessSignUpTests(TestCase):
    def setUp(self):
        """initialises tests for successful sign up"""
        url = reverse('signup')
        data = {
            'username': 'new_user',
            'email': 'new@user.com',
            'password1': 'new_password',
            'password2': 'new_password'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirected(self):
        """
        tests that valid user is redirected
        when form is valid, user is directed to home page
        """
        self.assertRedirects(self.response, self.home_url)

    def test_user_created(self):
        """tests whether user has been created"""
        self.assertTrue(User.objects.exists())

    def test_user_authenticated(self):
        """tests that user is successfully authenticated"""
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        """intialises test cases for invalid sign ups"""
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        """when sign up is invalid, returns to the same page"""
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        """tests that form has errors on invalid sign up"""
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_user_not_created(self):
        """tests that on invalid sign up, user object isn't created"""
        self.assertFalse(User.objects.exists())
