from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import FriendRequest, Post, User, UserProfile
from .forms import NewPostForm

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-timestamp')
    return render(request, "network/index.html", {
        "posts": posts,
        "form": NewPostForm()
    })


def send_friend_request(request, profile_id):
    from_user = request.user
    to_user = User.objects.get(pk=profile_id)

    if not to_user in from_user.profile.friends.all() or not from_user in to_user.profile.friends.all():
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user)
        if created:
            return JsonResponse({"message": "Friend request was sent successfully."}, status=201)
        else:
            return JsonResponse({"message": "Friend request has been already sent."}, status=201)

    else:
        return JsonResponse({"error": "You are already friends."}, status=200)


def accept_friend_request(request, requestID):
    try:
        friend_request = FriendRequest.objects.get(pk=requestID)
        if friend_request.to_user == request.user:
            friend_request.to_user.profile.friends.add(
                friend_request.from_user)
            friend_request.from_user.profile.friends.add(
                friend_request.to_user)
            friend_request.active = False
            friend_request.save()
        else:
            return JsonResponse({"error": "You do not have the right to perform this action."}, status=403)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Specified friend request does not exist."}, status=400)

    return JsonResponse({"message": "New friend has been added successfully."}, status=201)


def friend_requests(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user, active=True)
    return render(request, "network/friend_requests.html", {
        "friend_requests": friend_requests
    })

def remove_profile_friend(request, profile_id):
    try:
        to_user = User.objects.get(pk=profile_id)
        from_user = request.user

        to_user.friends.remove(from_user.profile)
        from_user.friends.remove(to_user.profile)

        friend_request = FriendRequest.objects.get(from_user=from_user, to_user=to_user)
        friend_request.delete()

    except (User.DoesNotExist, FriendRequest.DoesNotExist) as e:
        return JsonResponse({"error": "User or Friend Request matching query does not exist."}, status=400)

    return JsonResponse({"message": "Friend has been successfully removed."}, status=201)


def cancel_friend_request(request, profile_id):
    try:
        to_user = User.objects.get(pk=profile_id)
        from_user = request.user

        friend_request = FriendRequest.objects.get(from_user=from_user, to_user=to_user)

        if friend_request.from_user == from_user:
            friend_request.delete()

    except (User.DoesNotExist, FriendRequest.DoesNotExist) as e:
        return JsonResponse({"error": "User or Friend Request matching query does not exist."}, status=400)

    return JsonResponse({"message": "Friend request has been successfully unsent."}, status=201)


def friends(request, profile_id):
    friends = UserProfile.objects.get(pk=profile_id).friends.all()
    friend_requests = FriendRequest.objects.filter(from_user__in=friends)
    return render(request, "network/friends.html", {
        "friends": friend_requests
    })

def decline_friend_request(request, requestID):
    try:
        friend_request = FriendRequest.objects.get(pk=requestID)
        if request.user == friend_request.to_user:
            friend_request.delete()
        else:
            return JsonResponse({"error": "You do not have the right to perform this action."}, status=403)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Specified friend request does not exist."}, status=400)

    return JsonResponse({"message": "Friend request has been declined successfully."}, status=201)


def remove_from_friends(request, requestID):
    try:
        friend_request = FriendRequest.objects.get(pk=requestID)

        to_user = friend_request.to_user
        from_user = friend_request.from_user

        if request.user == to_user or request.user == from_user:
            from_user.friends.remove(to_user.profile)
            to_user.friends.remove(from_user.profile)
            friend_request.delete()
        else:
            return JsonResponse({"error": "You do not have the right to perform this action."}, status=403)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Specified friend request does not exist."}, status=400)

    return JsonResponse({"message": "Friend has been successfully removed."}, status=201)


def show_profile(request, profile_id):
    try:
        profile = UserProfile.objects.get(pk=profile_id)
    
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User matching query does not exist."})
        
    return render(request, "network/profile.html", {
        "profile": profile,
        "posts": Post.objects.filter(author=profile).order_by('-timestamp'),
        "friend_request_available": not request.user.is_anonymous and not profile.user in request.user.profile.friends.all() and profile.user != request.user,
        "currently_friended": not request.user.is_anonymous and profile.user in request.user.profile.friends.all(),
        "friend_request_available": not request.user.is_anonymous and profile.user != request.user and not profile.user in request.user.profile.friends.all(),
        "self_in_friend_request": self_in_friend_request(profile.user, request.user)
    })


def self_in_friend_request(to_user, from_user):
    try:
        FriendRequest.objects.get(to_user=to_user, from_user=from_user)
        return True

    except FriendRequest.DoesNotExist:
        return False


def create_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.author = request.user.profile
            newPost.save()
            return HttpResponseRedirect(reverse("index"))


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
