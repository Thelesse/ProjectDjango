from django.contrib.auth.models import User
from django.db import models


#models almost are our objects in database for example for our App-user we have user,name and email
#fields in database
#when you write models.oneToOneFiled it means connection between 2 models are one to one
#when you write models.ForeignKey it means connection is one to many
class App_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=40, blank=False, null=False)
    email = models.CharField(max_length=40, blank=True, null=True)

    #when you call the app_user return the name
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

    #function that return the url of post image
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

    #function that returns text of all comments of current post
    @property
    def post_comments(self):
        return [c for c in Comments.objects.all() if c.post.id == self.id]

    #function that returns the number of comments of current post
    @property
    def sum_comments(self):
        return len(self.post_comments)

    #returns number of likes of current post
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
