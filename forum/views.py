from django.shortcuts import render, get_object_or_404
from .models import Forum


def home(request):
    """renders home page view"""
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums': forums})


def forum_topics(request, pk):
    """renders page containing forums"""
    forum = get_object_or_404(Forum, pk=pk)
    return render(request, 'topics.html', {'forum': forum})


def new_topic(request, pk):
    """renders page where a user can add a new topic"""
    forum = get_object_or_404(Forum, pk=pk)
    return render(request, 'new_topic.html', {'forum': forum})
