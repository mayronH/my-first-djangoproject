from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    post_image = models.ImageField(upload_to='images/', default='images/default.png')
    headline = models.CharField(max_length=200, default='Plain headline for a plain post')
    tags = TaggableManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def thumbnail(self):
        return mark_safe('<img src="{url}" height="{height}"/>'.format(
            url = self.post_image.url,
            height = 250,
        ))


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
