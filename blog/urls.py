from django.urls import path

from . import views

urlpatterns = [
    path("", views.starting_page_view.as_view(), name="starting-page"),
    path("posts", views.posts_view.as_view(), name="posts-page"),
    path("posts/<slug:post_slug>", views.post_detail_view.as_view(),
         name="post-detail-page"),  # /posts/my-first-post/
    path('read-later', views.read_later_view.as_view(), name='read-later')
]
