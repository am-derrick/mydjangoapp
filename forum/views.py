from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Forum, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator


def home(request):
    """renders home page view"""
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums': forums})


def forum_topics(request, pk):
    """renders page containing forums"""
    forum = get_object_or_404(Forum, pk=pk)
    topics = forum.topics.order_by(
        '-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'forum': forum, 'topics': topics})


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
    topic.views += 1
    topic.save()
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


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    """class for updating post, extends from the generic views - UpdateView"""
    model = Post
    fields = ('message', )
    template_name = 'edit.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.forum.pk, topic_pk=post.topic.pk)
