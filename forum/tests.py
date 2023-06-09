from django.test import TestCase
from django.urls import reverse, resolve
from .views import home


class HomepageTests(TestCase):
    def test_home_view_status_code(self):
        """tests response code for home page"""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """resolves / url to the home view"""
        view = resolve('/')
        self.assertEquals(view.func, home)
