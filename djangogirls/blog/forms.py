"""Forms for app."""
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Docstring."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Docstring."""

        model = Post
        fields = ('title', 'text')
