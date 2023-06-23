from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home
from ..models import Forum


class HomepageTests(TestCase):
    def setUp(self):
        """creates a forum instance"""
        self.forum = Forum.objects.create(
            name="Banter", description="This forum is about random banter.")
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        """tests response code for home page"""
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """checks to resolve / url to the home view"""
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_links_to_topics_page(self):
        """tests navigation links to topics page"""
        forum_topics_url = reverse(
            'forum_topics', kwargs={'pk': self.forum.pk})
        self.assertContains(
            self.response, 'href="{0}"'.format(forum_topics_url))

    def test_forum_topics_view_links_to_homepage(self):
        """tests navigation links from topics page back to home page"""
        forum_topics_url = reverse('forum_topics', kwargs={'pk': 1})
        response = self.client.get(forum_topics_url)
        hompage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(hompage_url))
