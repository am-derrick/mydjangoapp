from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Forum, Post, Topic
from ..views import PostListView


class TopicPostsTests(TestCase):
    def setUp(self):
        """intialises test cases for topic posts"""
        forum = Forum.objects.create(
            name='Banter', description='This forum is about random banter.')
        user = User.objects.create_user(
            username='john', email='john@doe.com', password='abcd12')
        topic = Topic.objects.create(
            subject='Newest topic', forum=forum, opener=user)
        Post.objects.create(
            message='This is the very first thread off this.', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={
                      'pk': forum.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        """tests that the view returns success code"""
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        """tests the view function"""
        view = resolve('/forum/1/topics/1/')
        self.assertEquals(view.func, PostListView)
