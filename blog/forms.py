"""Forms for app."""
from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Docstring."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Docstring."""

        model = Post
        fields = ('title', 'text')


class CommentForm(forms.ModelForm):
    """Form to add comment."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Model for comment."""

        model = Comment
        fields = ('author', 'text')
