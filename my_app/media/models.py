from django.contrib.auth.models import User
from django.db import models

class App_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=40, blank=False, null=False)
    email = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

    #function that return comments of current user
    @property
    def user_comments(self):
        return [c for c in Comments.objects.all() if c.user.name == self.name]


class Post(models.Model):
    user = models.ForeignKey(App_User, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    text = models.TextField(max_length=300, null=False, blank=False)
    image = models.ImageField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

    @property
    def post_comments(self):
        return [c for c in Comments.objects.all() if c.post.id == self.id]


    @property
    def sum_comments(self):
        return len(self.post_comments)

    @property
    def post_likes(self):
        return len([like for like in Likes.objects.all() if like.post.id == self.id])


class Comments(models.Model):
    user = models.ForeignKey(App_User, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=300, blank=False, null=False)

    def __str__(self):
        return self.text
    

class Likes(models.Model):
    user = models.ForeignKey(App_User, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
