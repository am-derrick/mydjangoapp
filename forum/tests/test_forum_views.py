from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home, forum_topics, new_topic
from ..models import Forum, Topic, Post
from django.contrib.auth.models import User
from ..forms import NewTopicForm


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
        self.assertEquals(view.func, forum_topics)

    def test_forum_topics_view_has_nav_links(self):
        """tests navigation links on topics page to home and to new_topics page"""
        forum_topics_url = reverse('forum_topics', kwargs={'pk': 1})
        hompage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(forum_topics_url)
        self.assertContains(response, 'href="{0}"'.format(hompage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(TestCase):
    def setUp(self):
        """creates a new topics instance"""
        Forum.objects.create(
            name='Banter', description='This forum is about random banter.')
        User.objects.create_user(
            username='john', email='john@doe.com', password='pass')

    def test_new_topic_view_success_status_code(self):
        """test case for success of new_topics page"""
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        """test case for when new_topics page is not found"""
        url = reverse('new_topic', kwargs={'pk': 98})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        """tests new_topics url resolve"""
        view = resolve('/forum/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_links_to_forum_topics_view(self):
        """tests that new_topic has link that links back to forum_topics"""
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        forum_topics_url = reverse('forum_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(forum_topics_url))

    def test_csrf(self):
        """tests that cross site request forgery token is present"""
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post(self):
        """tests that the post contains valid data"""
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test subject',
            'message': 'Some random text'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post(self):
        """
        test case for when the post contains invalid data
        when invalid, no redirection but the form should show with errors
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_empty_fields(self):
        """
        test case for when the post contains empty data
        when invalid, no redirection but the form should show with errors        
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        """test to verify new_topic contains form"""
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
