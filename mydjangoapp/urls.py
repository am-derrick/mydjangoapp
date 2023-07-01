"""
URL configuration for mydjangoapp project.
"""
from django.contrib import admin
from django.urls import path

from forum import views
from accounts import views as accounts_views
from django.contrib.auth.views import (LogoutView, LoginView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetCompleteView,
                                       PasswordResetConfirmView, PasswordChangeDoneView, PasswordChangeView)


urlpatterns = [
    path('', views.ForumListView.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', accounts_views.signup, name='signup'),
    path('reset/', PasswordResetView.as_view(template_name='password_reset.html',
                                             email_template_name='password_reset_email.html',
                                             subject_template_name='password_reset_subject.txt'),
         name='password_reset'),
    path('reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('settings/password/', PasswordChangeView.as_view(
        template_name='password_change.html'), name='password_change'),
    path('settings/password/done/', PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'), name="password_change_done"),
    path('forum/<int:pk>/topics/<int:topic_pk>/reply/',
         views.reply, name='reply'),
    path('forum/<int:pk>/topics/<int:topic_pk>/',
         views.topic_posts, name='topic_posts'),
    path('forum/<int:pk>/', views.TopicListView.as_view(), name='forum_topics'),
    path('forum/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('forum/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/',
         views.PostUpdateView.as_view(), name='edit'),
    path('admin/', admin.site.urls),
]
