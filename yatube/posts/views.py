from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Group, Post, Comment, Follow, User


def index(request):
    """Функция отображения главной страницы"""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGE_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Функция отображения страницы всех постов группы"""
    group = get_object_or_404(Group, slug=slug)
    group_list = group.posts.all()
    paginator = Paginator(group_list, settings.PAGE_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


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
    if request.method != 'POST':
        form = PostForm(instance=post)
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
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, settings.PAGE_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_post = Post.objects.filter(author=user).count()
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, author=user).exists():
            following = True
        else:
            following = False
    else:
        following = False
    context = {
        'author': user,
        'page_obj': page_obj,
        'num_post': num_post,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Функция отображения выбранного поста"""
    post = get_object_or_404(Post, pk=post_id)
    count = Post.objects.filter(author=post.author).count()
    comments = Comment.objects.filter(post_id=post_id)
    form_comments = CommentForm(request.POST or None)
    context = {
        'post': post,
        'count': count,
        'comments': comments,
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
    user = request.user
    posts = Post.objects.filter(author__following__user=user)
    paginator = Paginator(posts, settings.PAGE_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """Подписаться на автора"""
    author = get_object_or_404(User, username=username)
    if author == request.user:
        return redirect(
            'posts:profile',
            username=username
        )
    follower = Follow.objects.filter(
        user=request.user,
        author=author
    ).exists()
    if follower is True:
        return redirect(
            'posts:profile',
            username=username
        )
    Follow.objects.create(user=request.user, author=author)
    return redirect(
        'posts:profile',
        username=username
    )


@login_required
def profile_unfollow(request, username):
    """Отписаться от автора"""
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
