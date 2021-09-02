"""Model for blog."""
from django.db import models
from django.utils import timezone
from django.conf import settings


class Post(models.Model):
    """Post model for blog."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """Publish the post."""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        """Render a text (string) with a Post title."""
        return str(self.title)

    def approved_comments(self):
        """Render approved comments."""
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    """Comment model for blog."""

    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        """Docstring."""
        self.approved_comment = True
        self.save()

    def __str__(self):
        """Docstring."""
        return str(self.text)
