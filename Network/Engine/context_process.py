from django.contrib.auth.models import User
from .models import Blog


# Display some info in main page
def context_process(request):
    user = User.objects.get(is_staff=True)
    users = User.objects.all()
    blog = Blog.objects.get(user=user)
    blogs = Blog.objects.filter(join=True)

    return {'blog': blog, 'users': users, 'blogs': blogs}
