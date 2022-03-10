import json
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import FriendRequest, Post, User, UserProfile

# Create your views here.
def index(request):
    return render(request, "network/index.html")


def load_posts(request):
    profile = request.GET.get("profile")
    if (profile):
        posts = Post.objects.filter(author=profile).order_by('-timestamp')
    else:        
        posts = Post.objects.order_by('-timestamp')
    return JsonResponse({
        "posts": [post.serialize() for post in posts]
    }, safe=False)


def send_friend_request(request, profile_id):
    from_user = request.user
    to_user = User.objects.get(pk=profile_id)

    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return JsonResponse({"message": "Friend request was sent successfully."}, status=201)
    else:
        return JsonResponse({"message": "Friend request has been already sent or you are actually friends."}, status=201)


def accept_friend_request(request, requestID):
    try:
        friend_request = FriendRequest.objects.get(pk=requestID)
        if friend_request.to_user == request.user:
            friend_request.to_user.profile.friends.add(friend_request.from_user)
            friend_request.from_user.profile.friends.add(friend_request.to_user)
        else:
            return JsonResponse({"error": "You do not have the right to perform this action!"}, status=403)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Specified friend request does not exist."}, status=400)

    return JsonResponse({"message": "New friend has been added successfully."}, status=201)


def friend_requests(request):
    requests = FriendRequest.objects.filter(to_user=request.user).values('id', 'to_user', 'from_user')
    return JsonResponse(json.dumps(list(requests)), safe=False)


def decline_friend_request(request, requestID):
    try:
        friend_request = FriendRequest.objects.get(pk=requestID)
        if request.user == friend_request.to_user:
            friend_request.delete()
        else:
            return JsonResponse({"error": "You do not have the right to perform this action!"}, status=403)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Specified friend request does not exist."}, status=400)

    return JsonResponse({"message": "Friend request has been declined successfully."}, status=201)        


def show_profile(request, profile_id):
    profile = UserProfile.objects.get(pk=profile_id)
    return JsonResponse(profile.serialize(request.user), safe=False)


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
