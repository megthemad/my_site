from django.contrib import admin
from .models import Post, Author, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')
    search_fields = ('title', 'content')
    list_filter = ('date', 'author')
    prepopulated_fields = {"post_slug": ("title",)}
    read_only_fields = ('post_slug',)


class AuthorAdmin(admin.ModelAdmin):
    # list_display = ('irst_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('first_name', 'last_name')


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('user_name', 'user_email')
    list_filter = ('user_name', 'user_email')
    list_display = ('user_name', 'user_email', 'date')


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
