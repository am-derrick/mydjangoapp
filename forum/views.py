from django.shortcuts import render, get_object_or_404, redirect
from .models import Forum, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm
from django.contrib.auth.decorators import login_required


def home(request):
    """renders home page view"""
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums': forums})


def forum_topics(request, pk):
    """renders page containing forums"""
    forum = get_object_or_404(Forum, pk=pk)
    return render(request, 'topics.html', {'forum': forum})


@login_required
def new_topic(request, pk):
    """renders page where a user can add a new topic"""
    forum = get_object_or_404(Forum, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum = forum
            topic.opener = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('forum_topics', pk=forum.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'forum': forum, 'form': form})
