from django.contrib import admin
from .models import Post, Author, Tag


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


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
