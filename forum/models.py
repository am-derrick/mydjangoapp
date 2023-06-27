from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


class Forum(models.Model):
    """Forum/Board class representing the name and description"""
    name = models.CharField(max_length=24, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_number(self):
        """returns number of posts"""
        return Post.objects.filter(topic__forum=self).count()

    def get_most_previous_post(self):
        """returns the last post"""
        return Post.objects.filter(topic__forum=self).order_by('-created_at').first()


class Topic(models.Model):
    """class representing topic under a forum"""
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    forum = models.ForeignKey(
        Forum, related_name='topics', on_delete=models.CASCADE)
    opener = models.ForeignKey(
        User, related_name='topics', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class Post(models.Model):
    """class representing a post on the forum"""
    message = models.TextField(max_length=400)
    topic = models.ForeignKey(
        Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        short_message = Truncator(self.message)
        return short_message.chars(30)
