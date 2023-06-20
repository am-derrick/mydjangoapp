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
    path('', views.home, name='home'),
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
    path('forum/<int:pk>/', views.forum_topics, name='forum_topics'),
    path('forum/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('admin/', admin.site.urls),
]
