from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..forms import PostForm
from ..models import Forum, Post, Topic
from ..views import reply


class ReplyTestCase(TestCase):
    """base test case for reply views tests"""

    def setUp(self):
        """intialises base case tests"""
        self.forum = Forum.objects.create(
            name='Banter', description='This is some random banter')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(
            username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(
            subject='Start conversation', forum=self.forum, opener=user)
        Post.objects.create(
            message='This is a starter conversation', topic=self.topic, created_by=user)
        self.url = reverse(
            'reply', kwargs={'pk': self.forum.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTests(ReplyTestCase):
    def test_redirection(self):
        """tests redirection url present in topic view"""
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class ReplyTests(ReplyTestCase):
    def setUp(self):
        """intialises tests for reply"""
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """tests that view has 200 success code"""
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        """tests the view function"""
        view = resolve('/forum/1/topics/1/reply/')
        self.assertEquals(view.func, reply)

    def test_csrf(self):
        """tests existence of csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """tests presence of Post Form"""
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        """Tests that reply view contains two inputs: csrf, message textarea"""
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyTests(ReplyTestCase):
    def setUp(self):
        """intialises tests for successful reply"""
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(
            self.url, {'message': 'hello, world!'})

    def test_redirection(self):
        """tests that a valid form submission should redirect the user"""
        topic_posts_url = reverse('topic_posts', kwargs={
                                  'pk': self.forum.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        """
        tests that post count is 2
        first created by `ReplyTopicTestCase` setUp and 
        another created by the post data in this class
        """
        self.assertEquals(Post.objects.count(), 2)


class InvalidReplyTests(ReplyTestCase):
    def setUp(self):
        """
        intialises tests when reply is invalid
        data passed is empty
        """
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        """tests that invalid reply still returns 200 success code"""
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        """tests presence of errors in form"""
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
