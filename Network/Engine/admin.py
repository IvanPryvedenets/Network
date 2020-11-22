from django.contrib import admin
from .models import Post, Blog


# Register Blog model
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'join')

    fieldsets = (
        ('Info about blog', {
            'fields': ('user', 'image', 'join', 'slug')
        }),

    )

    def has_add_permission(self, request, obj=None):
        return False


# Register Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'date', 'read')


