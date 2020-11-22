from django.urls import path, include
from .views import *

urlpatterns = [
    path('', StoryPage.as_view(), name='story_url'),  # Page with stories
    path('blog/<str:slug>/', BlogPage.as_view(), name='blog_url'),  # Blog page
    path('blogs/', BlogsPage.as_view(), name='blogs_url'),  # Page with all the blogs

    path('join/', join, name='join_url')  # Url to function that change join field in blog
]
