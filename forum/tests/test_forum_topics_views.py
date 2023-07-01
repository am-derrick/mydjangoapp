from django.test import TestCase
from django.urls import reverse, resolve
from ..views import TopicListView
from ..models import Forum


class ForumTopicsTests(TestCase):
    def setUp(self):
        """creates a forum instance"""
        Forum.objects.create(
            name="Banter", description="This forum is about random banter.")

    def test_forum_topics_view_success_status_code(self):
        """test case for success of forum_topics page"""
        url = reverse('forum_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_forum_topics_view_not_found_status_code(self):
        """test case for when not found forum_topics page"""
        url = reverse('forum_topics', kwargs={'pk': 98})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_forum_topics_url_resolves_forum_topics_view(self):
        """tests forum_topics url"""
        view = resolve('/forum/1/')
        self.assertEquals(view.func, TopicListView)

    def test_forum_topics_view_has_nav_links(self):
        """tests navigation links on topics page to home and to new_topics page"""
        forum_topics_url = reverse('forum_topics', kwargs={'pk': 1})
        hompage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(forum_topics_url)
        self.assertContains(response, 'href="{0}"'.format(hompage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
