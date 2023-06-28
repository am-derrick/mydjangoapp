from django.forms import ModelForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Forum, Post, Topic
from ..views import PostUpdateView


class EditTestCase(TestCase):
    """base test case for `PostUpdateView` view tests"""

    def setUp(self):
        """initialises the base case test case"""
        self.forum = Forum.objects.create(
            name='Banter', description='This is some random banter')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(
            username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(
            subject='Start conversation', forum=self.forum, opener=user)
        self.post = Post.objects.create(
            message='This is a starter conversation', topic=self.topic, created_by=user)
        self.url = reverse('edit', kwargs={
            'pk': self.forum.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })


class LoginRequiredEditTests(EditTestCase):
    def test_redirection(self):
        """test that redirects to login when one tries to edit without logging in"""
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedEditTests(EditTestCase):
    def setUp(self):
        """initialises unauthorized edit test cases"""
        super().setUp()
        username = 'jane'
        password = '321'
        user = User.objects.create_user(
            username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """topic edited by user, otherwise returns a 404"""
        self.assertEquals(self.response.status_code, 404)


class EditTests(EditTestCase):
    def setUp(self):
        """intitalises edit tests"""
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """tests that a success status code is returned"""
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        """tests that view function matches PostUpdateView"""
        view = resolve('/forum/1/topics/1/posts/1/edit/')
        self.assertEquals(view.func.view_class, PostUpdateView)

    def test_csrf(self):
        """tests presence of csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """tests that edit view contains Model Form"""
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        """tests that view contains csrf and message textarea"""
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulEditTests(EditTestCase):
    def setUp(self):
        """intialises succesful edit tests"""
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(
            self.url, {'message': 'edited message'})

    def test_redirection(self):
        """tests that when successful, a user is redirected"""
        topic_posts_url = reverse('topic_posts', kwargs={
                                  'pk': self.forum.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(self.response, topic_posts_url)

    def test_post_changed(self):
        """refreshes database to check if message changed"""
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, 'edited message')


class InvalidEditTests(EditTestCase):
    def setUp(self):
        """intialises invalid edi tests, by passing empty data"""
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        """when invalid, a 200 status code is returned"""
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        """tests that when invalid, form has errors"""
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
