"""Blog metadata."""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Configuration for blog."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
