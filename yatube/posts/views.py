from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Group, Post, Follow, User


def paginate(queryset, request, page_size=settings.PAGE_POSTS):
    return Paginator(queryset, page_size).get_page(request.GET.get('page'))


def index(request):
    """Функция отображения главной страницы"""
    return render(request, 'posts/index.html', {
        'page_obj': paginate(Post.objects.all(), request),
    })


def group_posts(request, slug):
    """Функция отображения страницы всех постов группы"""
    group = get_object_or_404(Group, slug=slug)
    return render(request, 'posts/group_list.html', {
        'group': group,
        'page_obj': paginate(group.posts.all(), request),
    })


@login_required
def post_create(request):
    """Функция отображения страницы создания поста.
    Доступна только авторизованным пользователям"""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    """Функция редактирования поста.
    Доступна только авторизованным пользователям"""
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)


def profile(request, username):
    """Функция отображения страницы всех постов пользователя"""
    author = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        Follow.objects.filter(user=request.user, author=author).exists()
    return render(request, 'posts/profile.html', {
        'author': author,
        'page_obj': paginate(author.posts.all(), request, settings.PAGE_POSTS),
        'following': Follow.objects.all(),
    })


def post_detail(request, post_id):
    """Функция отображения выбранного поста"""
    post = get_object_or_404(Post, pk=post_id)
    form_comments = CommentForm(request.POST or None)
    context = {
        'post': post,
        'form_comments': form_comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def add_comment(request, post_id):
    """Функция добавления комментария к посту"""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Отображение страницы подписок"""
    return render(request, 'posts/follow.html', {
        'page_obj': paginate(Post.objects.all().filter(
            author__following__user=request.user), request),
    })


@login_required
def profile_follow(request, username):
    """Подписаться на автора"""
    author = get_object_or_404(User, username=username)
    if author != request.user and not author.following.filter(
        user=request.user,
    ).exists():
        Follow.objects.get_or_create(
            user=request.user,
            author=author,
        )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """Отписаться от автора"""
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
