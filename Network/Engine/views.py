from django.shortcuts import render
from django.views import View

from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.models import User
import datetime

from .models import Blog, Post
from .forms import PostForm


class StoryPage(View):
    def get(self, request):

        blogs = Blog.objects.filter(join=True).order_by('-id')
        posts = Post.objects.all().order_by('-id')

        return render(request, 'Engine/Story.html', context={'blogs': blogs, 'posts': posts})

    def post(self, request):

        id = request.POST.get('post')
        post = Post.objects.get(id=id)

        if post and post.read is False:  # Change 'read' field in post models
            post.read = True
            post.save()
        else:
            post.read = False
            post.save()

        blogs = Blog.objects.filter(join=True).order_by('-id')
        posts = Post.objects.all().order_by('-id')

        return render(request, 'Engine/Story.html', context={'blogs': blogs, 'posts': posts})


class BlogPage(View):
    def get(self, request, slug):

        blog = Blog.objects.get(slug__iexact=slug)
        form = PostForm
        posts = Post.objects.filter(blog=blog).order_by('-id')

        return render(request, 'Engine/Blog.html', context={'blog': blog, 'form': form, 'posts': posts})

    def post(self, request, slug):

        form = PostForm(request.POST)
        blog = Blog.objects.get(slug__iexact=slug)

        if form.is_valid():  # Create posts
            post = Post.objects.create(
                blog=blog,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                date=datetime.datetime.now()
            )

        form = PostForm
        posts = Post.objects.filter(blog=blog).order_by('-id')

        # Send emails
        superuser = User.objects.get(is_staff=True)
        email_list = [blog.user.email for blog in Blog.objects.filter(join=True)]

        subject = 'User {} add new post.'.format(superuser.get_full_name)
        message = 'http://127.0.0.1:8000/{}'.format(superuser.blog.get_absolute_url())
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list=email_list, fail_silently=False)

        return render(request, 'Engine/Blog.html', context={'form': form, 'blog': blog, 'posts': posts})


class BlogsPage(View):
    def get(self, request):

        users = User.objects.filter(is_active=False)
        posts = Post.objects.all()

        return render(request, 'Engine/Blogs.html', context={'users': users, 'posts': posts})


# Change join field in blog models
def join(request):

    user = request.POST.get('user')
    blog = Blog.objects.get(user=user)

    if user and blog.join is False:
        blog.join = True
        blog.save()
    else:
        blog.join = False
        blog.save()

    users = User.objects.filter(is_active=False)
    posts = Post.objects.all()

    return render(request, 'Engine/Blog.html', context={'users': users, 'posts': posts})
