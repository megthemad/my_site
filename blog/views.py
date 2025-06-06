from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from django.views.generic import ListView
from django.views import View
from .models import Post
from .forms import CommentForm


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

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, post_slug):
        post = Post.objects.get(post_slug=post_slug)

        # This would be better if it was a method of the view class instead of repeated here and below
        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comments': post.comments.all().order_by('-id'),
            'comment_form': CommentForm(),
            # This lets us change the "Read Later" button to reflect if something was already saved for later
            'saved_for_later': self.is_stored_post(request, post.id)
        }
        return render(request, 'blog/post-detail.html', context)

    # Because the HTML is set up to use post_slug, we can use it here
    def post(self, request, post_slug):
        # Validate submitted form, add comment or do something then
        #  show same form again
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(post_slug=post_slug)

        if comment_form.is_valid():
            # Because our model excludes the "post" field, we need to edit the record on save
            comment = comment_form.save(commit=False)
            comment.post = post  # This will add the post name to the comment record
            comment.save()  # Now we save the comment record
            # This will get the post again, plus the added comment
            return HttpResponseRedirect(reverse('post-detail-page', args=[post_slug]))

        # If the form is invalid, we will just reload the page as before
        context = {
            'post': post,
            'post_tages': post.tags.all(),
            'comments': post.comments.all().order_by('-id'),
            'comment_form': comment_form,
            'saved_for_later': self.is_stored_post(request, post.id)
        }
        return render(request, 'blog/post-detail.html', context)

# This code is no longer needed since we are now using a generic view and defining
#  custome post and get functions
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # This line will display all the tags associated with the post
    #     context["post_tags"] = self.object.tags.all()
    #     # This line will pass the comment form data to the HTML template
    #     context["comment_form"] = comment_form()
    #     return context


class read_later_view(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            # This will only fetch the posts where the IDs are part of the stored_posts list
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context['has_posts'] = True

        return render(request, 'blog/stored-posts.html', context)

    def post(self, request):
        # Get any existing read later posts
        stored_posts = request.session.get('stored_posts')
        # Check if stored posts is empty
        if stored_posts is None:
            stored_posts = []
        # Set the post id as an integer to a variable
        post_id = (int(request.POST['post_id']))

        # Add post id to stored_posts only if it's not already there
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect('/')
