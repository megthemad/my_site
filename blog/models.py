from django.db import models
from django.urls import reverse
from datetime import date
from django.utils.text import slugify

# Create your models here.


class Author(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True,
                          serialize=False, verbose_name='ID')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Optional field for author bio
    bio = models.TextField(null=True)

    def full_name(self):
        # This method returns the full name of the author by concatenating first and last names
        return f"{self.first_name} {self.last_name}"

    def __str__(self):  # This method returns a string representation of the model instance
        # This ensures that anytime we print an Author instance, we get a readable string in the format determined below
        return self.full_name()


class Post(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True,
                          serialize=False, verbose_name='ID')
    title = models.CharField(default="", max_length=100)
    content = models.TextField(default="", blank=True)
    excerpt = models.CharField(default="", max_length=20)
    image = models.CharField(default="mountains.jpg", max_length=100)
    email = models.EmailField(default="email@server.com")
    date = models.DateField(auto_now=False)
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="posts", null=True)
    post_slug = models.SlugField(
        null=False, db_index=True, blank=False, unique=True)
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return self.excerpt

    def save(self, *args, **kwargs):
        if not self.post_slug:
            self.post_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post-detail-page", args=[self.post_slug])


class Tag(models.Model):
    captions = models.CharField(max_length=20)

    def __str__(self):
        return self.captions


class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(default="email@server.com")
    date = models.DateField(auto_now=True)
    text = models.TextField(max_length=400)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", null=True)

    def __str__(self):
        return self.user_name
