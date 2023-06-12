from django.shortcuts import render
from django.http import Http404
from .models import Forum


def home(request):
    """renders home page view"""
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums': forums})


def forum_topics(request, pk):
    """renders page containing forums or raises"""
    try:
        forum = Forum.objects.get(pk=pk)
    except:
        raise Http404
    return render(request, 'topics.html', {'forum': forum})
