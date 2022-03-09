import json
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import Post, User

# Create your views here.
def index(request):
    return render(request, "network/index.html")


def load_posts(request):
    posts = Post.objects.order_by('-timestamp')
    return JsonResponse({
        "posts": [post.serialize() for post in posts]
    })


def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        description = data.get("description")
        post = Post(author=request.user.profile, description=description)
        post.save() 
        return JsonResponse({"message": "Post was created successfully."}, status=200)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "This username is already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
