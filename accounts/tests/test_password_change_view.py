from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm


class PasswordChangeTests(TestCase):
    def setUp(self):
        """intialises password chnage view tests"""
        username = 'john'
        password = 'abdc1234'
        user = User.objects.create_user(
            username=username, email='john@doe.com', password=password)
        url = reverse('password_change')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        """tests that a 200 success code is returned"""
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        """tests that the view function is Password Change View"""
        view = resolve('/settings/password/')
        self.assertEquals(view.func.view_class, PasswordChangeView)

    def test_csrf(self):
        """tests existence of csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """tests presence of Password Change Form"""
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        """tests form inputs -> csrf, old password, new password 1 and 2"""
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)


class LoginRequiresPasswordChangeTests(TestCase):
    def test_redirection(self):
        """tests that password_change redirects to login page when accessed without logging in"""
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    """
    Base test cases for form processing
    Other classes will inherit from this class
    """

    def setUp(self, data={}):
        """initialises base test case"""
        self.user = User.objects.create_user(
            username='john', email='john@doe.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='john', password='old_password')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        """intialises tests for successful password change tests"""
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_paswword2': 'new_password',
        })

    def test_redirection(self):
        """tests that when valid, redirects to password change done"""
        self.assertRedirects(
            self.response, reverse('password_change_done'))

    def test_password_change(self):
        """tests that password changed and updated from database"""
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        """tests that user is authenticated by accessing the user context"""
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        """tests that invalid submission returns successfully to the same page"""
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        """tests that errors produced when invalid submission"""
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_password_change_fail(self):
        """tests that when database refreshes, password didn't change"""
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
        # would work too -> self.assertFalse(self.user.check_password('new_password'))
