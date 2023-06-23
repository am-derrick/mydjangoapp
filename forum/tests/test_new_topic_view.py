from django.test import TestCase
from django.urls import reverse, resolve
from ..views import new_topic
from ..models import Forum, Topic, Post
from django.contrib.auth.models import User
from ..forms import NewTopicForm


class NewTopicTests(TestCase):
    def setUp(self):
        """creates a new topics instance"""
        Forum.objects.create(
            name='Banter', description='This forum is about random banter.')
        User.objects.create_user(
            username='john', email='john@doe.com', password='pass')
        self.client.login(username='john', password='pass')

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
            'message': '',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        """test to verify new_topic contains form"""
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(form, NewTopicForm)


class LoginRequiredTests(TestCase):
    def setUp(self):
        """initialises tests login required for new topic view"""
        Forum.objects.create(
            name='Banter', description='This forum is about random banter.')
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        """
        tests that redirection to login page
        when a user tries to add a new topic and not authorised
        """
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')
