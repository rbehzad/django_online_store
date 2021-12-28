from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView

from .forms import *
from .models import Category, Post, Tag


class HomeListView(ListView):
    model = Post
    template_name = 'post/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created_at')
        context['categories'] = Category.objects.all().order_by('-created_at')
        context['tags'] = Tag.objects.all().order_by('-created_at')
        return context

def post_detail(request, slug_text):
    post = Post.objects.filter(slug = slug_text)
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    if post.exists():
        post = post.first()
    else:
        return HttpResponse('<h1>Page Not Found</h1>')

    comments = post.comment_set.all()
    context = {
        'post': post,
        'comments': comments,
        'categories': categories,
        'tags': tags,
    }

    return render(request, 'post/post_detail.html', context)

def class_category(request, slug_text):
    category = Category.objects.get(slug=slug_text)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    context = {
        'category_name': category.title,
        'posts': posts,
        'categories': categories,
        'tags': tags,
    }

    return render(request, 'post/category.html', context)


@login_required(login_url='login')
def dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'post/dashboard.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')
    # return redirect('login')


def loginUser(request):
    page = 'login'
    context = {'page': page}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # if user authenticated below function return user object
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # this is gonna create that session and put into that coockies
            login(request, user)
            return redirect('dashboard')

    return render(request, 'post/login_register.html', context)


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('dashboard')
        
    context = {'form': form, 'page': page}
    return render(request, 'post/login_register.html', context)

@login_required(login_url='login')
def addPost(request):
    page = 'add_post'
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    form = AddPost()
    if request.method == 'POST':
        form = AddPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        if 'submitted' in request.GET:
            submitted = True

    context = {'categories': categories, 'form': form, 'page': page, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def addCategory(request):
    page = 'add_category'
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    form = AddCategory()
    if request.method == 'POST':
        form = AddCategory(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.creator = request.user
            category.save()
            return redirect('categories')
    else:
        if 'submitted' in request.GET:
            submitted = True

    context = {'categories': categories, 'form': form, 'page': page, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def addTag(request):
    page = 'add_tag'
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    form = AddTag()
    if request.method == 'POST':
        form = AddTag(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.creator = request.user
            tag.save()
            return redirect('tags')
    else:
        if 'submitted' in request.GET:
            submitted = True

    context = {'form': form, 'page': page, 'categories': categories, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def deletePost(request, slug):
    page = 'post'
    post = Post.objects.get(slug=slug)
    context = {
        'page': page,
    }
    if request.method == 'POST': # confirming delete
        post.delete()
        return redirect('dashboard')
    return render(request, 'post/delete_confirm.html', context)


@login_required(login_url='login')
def updatePost(request, slug):
    page = 'update_post'
    post = Post.objects.get(slug=slug)
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    form = AddPost()
    if request.method == 'POST':
        form = AddPost(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form, 'page': page, 'categories': categories, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def deleteCategory(request, slug):
    page = 'category'
    category = Category.objects.get(slug=slug)
    context = {
        'page': page,
    }
    if request.method == 'POST': # confirming delete
        category.delete()
        return redirect('categories')
    return render(request, 'post/delete_confirm.html', context)


@login_required(login_url='login')
def updateCategory(request, slug):
    page = 'update_category'
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    category = Category.objects.get(slug=slug)
    form = AddCategory()
    if request.method == 'POST':
        form = AddCategory(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')

    context = {'form': form, 'page': page, 'categories': categories, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def categoryList(request):
    user = request.user
    page = 'categories'
    categories = Category.objects.order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')

    my_categories = Category.objects.filter(creator=user).order_by('-created_at')
    context = {
        'categories': categories,
        'tags': tags,
        'page': page,
        'my_categories': my_categories,
    }
    return render(request, 'post/delete_updateButton.html', context)


@login_required(login_url='login')
def tagList(request):
    user = request.user
    page = 'tags'
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')

    my_tags = Tag.objects.filter(creator=user).order_by('-created_at')
    context = {
        'categories': categories,
        'tags': tags,
        'page': page,
        'my_tags': my_tags,
    }
    return render(request, 'post/delete_updateButton.html', context)


@login_required(login_url='login')
def deleteTag(request, slug):
    page = 'tag'
    context = {
        'page': page,
    }
    tag = Tag.objects.get(slug=slug)
    if request.method == 'POST': # confirming delete
        tag.delete()
        return redirect('tags')
    return render(request, 'post/delete_confirm.html', context)



@login_required(login_url='login')
def updateTag(request, slug):
    page = 'update_tag'
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    tag = Tag.objects.get(slug=slug)
    form = AddTag()
    if request.method == 'POST':
        form = AddTag(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tags')

    context = {'form': form, 'page': page, 'categories': categories, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def addComment(request, slug):
    page = 'add_comment'
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    form = AddComment()
    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(slug=slug)
            comment.save()
            return redirect(reverse('post_detail', args=[slug]))

    else:
        if 'submitted' in request.GET:
            submitted = True

    context = {'categories': categories, 'form': form, 'page': page, 'tags': tags}
    return render(request, 'post/add_update.html', context)


def searchPost(request):
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')

    if request.method == 'POST':
        searched = request.POST['search']
        posts = Post.objects.filter(Q(title__contains=searched) | Q(content__contains=searched))
        context = {
            'searched': searched,
            'posts': posts,
            'categories': categories,
            'tags': tags,
        }
        return render(request, 'post/search.html', context)
    else:
        context = {}
        return render(request, 'post/search.html', context)


def contact(request):
    categories = Category.objects.all().order_by('-created_at')
    tags = Tag.objects.all().order_by('-created_at')
    context = {'categories': categories, 'tags': tags}
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']
        send_mail(
            'message from ' + message_name, # subject
            message, # message
            message_email, # from email
            ['rezebehzadfard.02@gmail.com'], # to email
        )

        context['message_name'] = message_name
        return render(request, 'post/contact.html', context)
    
    else:
        return render(request, 'post/contact.html', context)
