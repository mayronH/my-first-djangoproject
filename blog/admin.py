from django.contrib import admin
from .models import Post,Comment


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'headline', 'text', 'created_date', 'published_date', 'author', 'tags', 'post_image', 'thumbnail',]
    readonly_fields = ('thumbnail',)

    list_display = ('title', 'created_date', 'published_date', 'author',)
    list_filter = ['published_date']

# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)