from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
from .models import *

#function that make new post
def post(request):
    if request.method == 'POST':#method is post because we are sending data to server
        form = Posting(request.POST, request.FILES)
        if form.is_valid():#it means the form is filled
            user = request.user.app_user
            #we get data from the form
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            image = request.POST['image']

            #create new post
            new_post = Post.objects.create(user=user, title=title, text=text, image=image)
            #save the post in database
            new_post.save()

            return home(request)

        else:
            return render(request, 'html/posting.html', context={"form": form})

    else:
        form = Posting()
    #context is what we use in our html file for example here form is in context and in posting.html
    #we used form in {{form}}
    return render(request, 'html/posting.html',context={"form":form})


def home(request):
    #get all posts from database
    posts = Post.objects.all()
    #get all comments from database
    comments = len([c for c in Comments.objects.all()])
    return render(request, 'html/home.html', context={'posts':posts, 'com': comments})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #we check in database is that username is token or not
            if User.objects.filter(username=username).exists():
                note = "username is already taken"
                context = {'note': note}
                return render(request, 'html/Registration.html', context=context)
            else:
                #if it isnt token we create a new user and a new App-user and save them
                user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
                app_user = App_User.objects.create(user=user, email=email, name=name)
                user.save()
                app_user.save()

                return home(request)

    else:
        form = RegisterForm()
        return render(request, 'html/Registration.html',context={'form':form})


def sign_in(request):
    if request.method == 'POST':
        form = SignIn(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            #this is ready method in django to check are username and password coorect
            #if they are correct make sign-in
            user = authenticate(request, username= username, password=password)

            if user is not None:
                #ready method in django to sign-in
                login(request, user)
                return home(request)
            else:
                form = SignIn()
                return render(request, 'html/sign-in.html', context={'form':form})
    else:
        form = SignIn()

    return render(request, 'html/sign-in.html', context={'form': form})


def log_out(request):
    if request.method == 'GET':
        #ready method in django to log-out
        logout(request)

        return home(request)


def show_post(request, id):

    visitor = request.user.app_user
    #get current post from database
    post = Post.objects.get(id=id)
    #get comments of current post
    comments = post.post_comments
    #get likes of current post
    like = post.post_likes
    #get sum of likes
    sum_cm = len(comments)

    context={'post':post,'visitor':visitor,'comments':comments, 'likes': like, 'sum': sum_cm}
    return render(request, 'html/post.html', context=context)


def add_cm(request, id):
    #check is user log-in or not
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user.app_user
            post = Post.objects.get(id=id)
            text = request.POST['comment']
            #create comment and save it
            comment = Comments.objects.create(user=user, post=post, text=text)
            comment.save()

        return show_post(request, id)
    else:
        return show_post(request, id)


def own_page(request):
    user = request.user.app_user
    #just get posts of current user
    posts = [p for p in Post.objects.all() if p.user.name == user.name]
    return render(request, 'html/own-page.html', context={'posts':posts})


def add_like(request, id):
    post = Post.objects.get(id=id)
    user = request.user.app_user
    likes = Likes.objects.all()
    #check if current user didnt like this post he is able to like
    #but if he already likes it he isnt able to like anymore
    b = False
    for like in likes:
        if like.post == post and like.user == user:
            b = True
    if not b:
        #he didnt like this post then we create new like in database
        new_like = Likes.objects.create(post=post, user=user)

        new_like.save()

    return show_post(request, id)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            finish = form.cleaned_data['finish_date']
            user = form.cleaned_data['user']
            #method of search , teacher already did it , tell him i followed your way
            posts = Post.objects.all().filter(date__range=[start, finish]).filter(user__name=user)
            return render(request, 'html/home.html', context={'posts': posts})
        else:
            return home(request)

    else:
        form = SearchForm()
        return render(request, 'html/search.html', context={'form': form})