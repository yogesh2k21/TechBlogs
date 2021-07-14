from BlogFeed.models import BlogComment, Post
from django.contrib import admin
from BlogFeed.models import Post

# Register your models here.
admin.site.register(BlogComment)

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInjection.js',)