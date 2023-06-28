from django.shortcuts import render, get_object_or_404, redirect
from .models import Forum, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ForumListView(ListView):
    """class for home view, extends from the generic views - ListView"""
    model = Forum
    context_object_name = 'forums'
    template_name = 'home.html'


def forum_topics(request, pk):
    """renders page containing forums"""
    forum = get_object_or_404(Forum, pk=pk)
    queryset = forum.topics.order_by(
        '-last_updated').annotate(replies=Count('posts') - 1)
    # page 1
    page = request.GET.get('page', 1)
    # paginate to show 25 posts
    paginator = Paginator(queryset, 25)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # go back to page 1
        topics = paginator.page(1)
    except EmptyPage:
        # go to last page
        topics = paginator.page(paginator.num_pages)

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
