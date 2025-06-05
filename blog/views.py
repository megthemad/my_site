from django.shortcuts import render, get_object_or_404
from datetime import date
from django.views.generic import ListView
from django.views import View
from .models import Post
from .forms import comment_form


def get_date(post):
    return post.get('date')


class starting_page_view(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class posts_view(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class post_detail_view(View):
    # Commenting these out because we are now controlling post and get manually and don't need
    #   to define them
    # template_name = "blog/post-detail.html"
    # model = Post
    slug_field = "post_slug"         # model field name
    slug_url_kwarg = "post_slug"

    def get(self, request, slug):
        post = Post.objects.get(post_slug=slug)
        context = {
            'post': post,
            'post_tages': post.tags.all(),
            'comment_form': comment_form()
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request):
        pass

# This code is no longer needed since we are now using a generic view and defining
#  custome post and get functions
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # This line will display all the tags associated with the post
    #     context["post_tags"] = self.object.tags.all()
    #     # This line will pass the comment form data to the HTML template
    #     context["comment_form"] = comment_form()
    #     return context
