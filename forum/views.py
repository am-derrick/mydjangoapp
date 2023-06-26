from django.shortcuts import render, get_object_or_404, redirect
from .models import Forum, Topic, Post
from .forms import NewTopicForm, PostForm
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
        new_form = NewTopicForm(request.POST)
        if new_form.is_valid():
            topic = new_form.save(commit=False)
            topic.forum = forum
            topic.opener = request.user
            topic.save()
            Post.objects.create(
                message=new_form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        new_form = NewTopicForm()
    return render(request, 'new_topic.html', {'forum': forum, 'form': new_form})


def topic_posts(request, pk, topic_pk):
    """renders page containing topic posts"""
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply(request, pk, topic_pk):
    """renders page containing reply to topic posts"""
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        reply_form = PostForm(request.POST)
        if reply_form.is_valid():
            post = reply_form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        reply_form = PostForm()
    return render(request, 'reply.html', {'topic': topic, 'form': reply_form})
