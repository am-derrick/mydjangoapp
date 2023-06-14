from django import forms
from .models import Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Start a conversation/thread.'}),
        max_length=4000,
        help_text='Maximum text length is 4000.')

    class Meta:
        model = Topic
        fields = ['subject', 'message']
