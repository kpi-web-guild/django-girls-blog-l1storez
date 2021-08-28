"""Views for blog."""
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_list(request):
    """Render post list on the webpage."""
    posts = Post.objects.order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """Render post detail on the webpage."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    """Render new post on the webpage."""
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
