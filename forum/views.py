from django.shortcuts import render, get_object_or_404, redirect
from .models import Forum, Topic, Post
from django.contrib.auth.models import User


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

    if request.method == 'POST':
        theme = request.POST['theme']
        message = request.POST['message']

        user = User.objects.first()  # TODO: implement later, get user logged in

        topic = Topic.objects.create(
            subject=theme,
            forum=forum,
            opener=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        # TODO: redirect user to created topic page
        return redirect('forum_topics', pk=forum.pk)

    return render(request, 'new_topic.html', {'forum': forum})
