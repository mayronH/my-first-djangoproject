from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .form import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .filters import PostFilter
from datetime import datetime, timedelta
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag

# Create your views here.

def post_list(request):
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(posts_list, 8)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk = pk)
    # Colocando o formulario de comentário na mesma página.
    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comentário enviado para aprovação com sucesso')
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_list')

@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def post_search(request):
    query = request.GET.get('search')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(text__icontains=query))
    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_filter(request):
    # filter = PostFilter(request.GET, queryset=Post.objects.all())
    days = request.GET.get('date_range')
    time = datetime.today() - timedelta(days=int(days))
    posts = Post.objects.filter(published_date__gte=time)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_group_by_months(request):
    posts = Post.objects.all().dates('published_date','month')
    return {'posts_month' : posts}

def post_date(request, dt):

    data = datetime.strptime(dt, '%Y-%m-%d')

    posts = Post.objects.filter(
        published_date__year__gte=data.year,
        published_date__month__gte=data.month,
        published_date__year__lte=data.year,
        published_date__month__lte=data.month
        ).order_by('published_date')
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_tags(request,slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)

    return render(request, 'blog/post_list.html', {'tag': tag, 'posts': posts})

def common_tags(request):
    common_tags = Post.tags.most_common()[:12]
    return {'common_tags' : common_tags}