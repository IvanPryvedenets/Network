from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


# Create Blog model
class Blog(models.Model):
    image = models.ImageField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join = models.BooleanField(default=False)
    slug = models.SlugField(max_length=500, unique=True)

    def get_absolute_url(self):  # Get url for each blogs
        return reverse('blog_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # Save slug and get words from user model
        self.slug = slugify('{} {}'.format(self.user.first_name, self.user.last_name))
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Blog of: {} {}'.format(self.user.first_name, self.user.last_name)


# If user was create, create blog
@receiver(post_save, sender=User)
def blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance)


# And save it
@receiver(post_save, sender=User)
def save_blog(sender, instance, **kwargs):
    instance.blog.save()


# Create Post model
class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    date = models.DateTimeField()
    read = models.BooleanField(default=False)

