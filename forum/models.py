from django.db import models
from django.contrib.auth.models import User


class Forum(models.Model):
    """Forum/Board class representing the name and description"""
    name = models.CharField(max_length=24, unique=True)
    description = models.CharField(max_length=100)


class Topic(models.Model):
    """class representing topic under a forum"""
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    forum = models.ForeignKey(
        Forum, related_name='topics', on_delete=models.CASCADE)
    opener = models.ForeignKey(
        User, related_name='topics', on_delete=models.CASCADE)


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
