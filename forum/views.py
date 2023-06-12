from django.shortcuts import render
# from django.http import HttpResponse
from .models import Forum


def home(request):
    """renders home page view"""
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums': forums})


def forum_topics(request, pk):
    """renders page containing forums"""
    forum = Forum.objects.get(pk=pk)
    return render(request, 'topics.html', {'forum': forum})
