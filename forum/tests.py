from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, forum_topics
from .models import Forum


class HomepageTests(TestCase):
    def test_home_view_status_code(self):
        """tests response code for home page"""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """checks to resolve / url to the home view"""
        view = resolve('/')
        self.assertEquals(view.func, home)


class ForumTopicsTests(TestCase):
    def setUp(self):
        """creates a forum instance"""
        Forum.objects.create(
            name="Banter", description="This forum is about random banter.")

    def test_forum_topics_view_success_status_code(self):
        """test case for success of status code"""
        url = reverse('forum_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_forum_topics_view_not_found_status_code(self):
        """test case for when not found status code"""
        url = reverse('forum_topics', kwargs={'pk': 98})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_forum_topics_url_resolves_forum_topics_view(self):
        """tests forum_topics url"""
        view = resolve('/forum/1/')
        self.assertEquals(view.func, forum_topics)
