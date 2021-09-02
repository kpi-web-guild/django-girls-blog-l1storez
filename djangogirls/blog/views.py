"""Views for blog."""
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone  # pylint: disable=unused-import
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


@login_required
def post_list(request):
    """Render post list on the webpage."""
    posts = Post.objects.order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required
def post_detail(request, pk):  # pylint: disable=invalid-name
    """Render post detail on the webpage."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    """Render new post on the webpage."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):  # pylint: disable=invalid-name
    """Render edit post on the webpage."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    """Render draft post on the webpage."""
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):  # pylint: disable=invalid-name
    """Render publish post on the webpage."""
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):  # pylint: disable=invalid-name
    """Render remove post on the webpage."""
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
