from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Post


def get_date(post):
    return post.get('date')


def starting_page_view(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html", {
        "posts": latest_posts
    })


def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html", {
        "all_posts": all_posts
    })


def post_detail(request, slug):
    # left side is the variable name in the url, right side is the argumnent from the function
    identified_post = get_object_or_404(Post, post_slug=slug)
    return render(request, "blog/post-detail.html", {
        "post": identified_post,
    })
