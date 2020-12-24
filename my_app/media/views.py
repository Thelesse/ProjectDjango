from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
from .models import *

def post(request):
    if request.method == 'POST':
        form = Posting(request.POST, request.FILES)
        if form.is_valid():
            user = request.user.app_user
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            image = request.POST['image']

            #create new post
            new_post = Post.objects.create(user=user, title=title, text=text, image=image)
            new_post.save()

            return home(request)

        else:
            return render(request, 'html/posting.html', context={"form": form})

    else:
        form = Posting()
    return render(request, 'html/posting.html',context={"form":form})


def home(request):
    posts = Post.objects.all()
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
            if User.objects.filter(username=username).exists():
                note = "username is already taken"
                context = {'note': note}
                return render(request, 'html/Registration.html', context=context)
            else:
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
            user = authenticate(request, username= username, password=password)

            if user is not None:
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
        logout(request)

        return home(request)


def show_post(request, id):

    visitor = request.user.app_user
    post = Post.objects.get(id=id)
    comments = post.post_comments
    like = post.post_likes
    sum_cm = len(comments)

    context={'post':post,'visitor':visitor,'comments':comments, 'likes': like, 'sum': sum_cm}
    return render(request, 'html/post.html', context=context)


def add_cm(request, id):
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
    posts = [p for p in Post.objects.all() if p.user.name == user.name]
    return render(request, 'html/own-page.html', context={'posts':posts})


def add_like(request, id):
    post = Post.objects.get(id=id)
    user = request.user.app_user
    likes = Likes.objects.all()
    b = False
    for like in likes:
        if like.post == post and like.user == user:
            b = True
    if not b:
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
            posts = Post.objects.all().filter(date__range=[start, finish]).filter(user__name=user)
            return render(request, 'html/home.html', context={'posts': posts})
        else:
            return home(request)

    else:
        form = SearchForm()
        return render(request, 'html/search.html', context={'form': form})
