from django import forms
from .models import Comment


class comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            'user_name': 'Your name',
            'user_email': 'Your email',
            'text': 'Your comment'
        }
        error_messages = {
            'user_name': {
                'required': 'Please enter your user name',
                'max_length': 'User name cannot exceed 100 characters'
            },
            'text': {
                'required': 'Please enter your comment',
                'max_length': 'Comment cannot exceed 400 characters'
            }
        }
