import json
from tkinter.tix import Tree
from django.db.models import Q
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import FriendRequest, Post, User, UserProfile
from .forms import EditProfileForm

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-timestamp')
    return render(request, "network/index.html", {
        "posts": posts,
    })


def send_friend_request(request, profile_id):
    from_user = request.user

    try:
        to_user = User.objects.get(pk=profile_id)

        if not to_user in from_user.profile.friends.all() or not from_user in to_user.profile.friends.all():
            friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
            if created:
                return JsonResponse({"message": "Friend request was sent successfully."}, status=201)
            else:
                return JsonResponse({"message": "Friend request has been already sent."}, status=409)

        else:
            return JsonResponse({"error": "You are already friends."}, status=409)
    
    except User.DoesNotExist:
        return JsonResponse({"error": "User matching query does not exist."}, status=400)


def accept_friend_request(request, requestID):
    try:
        friend_request = FriendRequest.objects.get(pk=requestID)
        if friend_request.to_user == request.user:
            friend_request.to_user.profile.friends.add(friend_request.from_user)
            friend_request.from_user.profile.friends.add(friend_request.to_user)
            friend_request.active = False
            friend_request.save()
        else:
            return JsonResponse({"error": "You do not have the right to perform this action."}, status=403)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Specified friend request does not exist."}, status=400)

    return JsonResponse({"message": "New friend has been added successfully."}, status=201)


def friend_requests(request):
    context = {}

    friend_requests = FriendRequest.objects.filter(to_user=request.user, active=True).all()
    from_users = friend_requests.values_list('from_user', flat=True)
    print(from_users)

    context["friend_requests"] = friend_requests

    from_users_profiles = UserProfile.objects.filter(pk__in=from_users).all()
    print(from_users_profiles)

    for from_user_profile in from_users_profiles:
        from_user_friends = from_user_profile.friends.values_list('pk', flat=True)
        print(from_user_friends)
    
        mutual_friends = request.user.profile.friends.filter(pk__in=from_user_friends).all()
        print(mutual_friends)

        # NEED TO FIX THIS GLOBAL MUTUAL FRIENDS VARIABLE
        # ALL FRIENDS MUST HAVE SPECIFIC TO THEM MUTUAL FRIEND LISTS IN RELATION TO REQUEST USER

        context["mutual_friends"] = mutual_friends
        context["mutual_friends_amount"] = mutual_friends.count()

    return render(request, "network/friend_requests.html", context)


def edit_profile(request, profile_id):
    if request.method == "POST":
        profile = UserProfile.objects.get(pk=profile_id)
        if profile.user == request.user:
            form = EditProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("edit_profile", args=(profile.user.id,)))
        else:
            return JsonResponse({"error": "You do not have the permisson to perform this action."}, status=403)

    else:
        profile = UserProfile.objects.get(pk=profile_id)
        form = EditProfileForm(instance=profile)

    return render(request, "network/edit_profile.html", {
        "profile": profile,
        "form": form
    })


def remove_profile_friend(request, profile_id):
    try:
        to_user = User.objects.get(pk=profile_id)
        from_user = request.user

        to_user.friends.remove(from_user.profile)
        from_user.friends.remove(to_user.profile)

        friend_request = FriendRequest.objects.get(
            Q(from_user=from_user, to_user=to_user) | Q(from_user=to_user, to_user=from_user)
        )
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


def friends(request, profile_id):
    try:
        profile = UserProfile.objects.get(pk=profile_id)

        friends = profile.friends.all()

        friend_requests = FriendRequest.objects.filter(
            Q(from_user__in=friends) | Q(to_user__in=friends)
        )

        context = {}

        if request.user.is_authenticated:
            context["friends"] = friend_requests

            for friend_request in friend_requests:
                if friend_request.to_user == profile.user:
                    requests_friends = friend_requests.values_list('from_user', flat=True)
                else:
                    requests_friends = friend_requests.values_list('to_user', flat=True)

                requests_profiles = UserProfile.objects.filter(pk__in=requests_friends)
                friends_with_profile = profile.friends.values_list('pk', flat=True)

                for request_profile in requests_profiles:
                    request_friends = request_profile.friends.filter(pk__in=friends_with_profile)
                    print(request_friends)

                # NEED TO FIX THIS GLOBAL MUTUAL FRIENDS VARIABLE
                # ALL FRIENDS MUST HAVE SPECIFIC TO THEM MUTUAL FRIEND LISTS IN RELATION TO REQUEST USER

                context["mutual_friends"] = request_friends
                context["mutual_friends_amount"] = request_friends.count()

    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User profile matching query does not exist."}, status=400)

    return render(request, "network/friends.html", context)


def mutual_friends(request_user, profile):
    profile_friends = profile.friends.all()
    friends_with_profile = profile_friends.values_list('pk', flat=True)
    mutual_friends_of_request_user = request_user.friends.filter(pk__in=friends_with_profile)
    print(friends_with_profile)
    return mutual_friends_of_request_user


def show_profile(request, profile_id):
    try:
        profile = UserProfile.objects.get(pk=profile_id)

        context = {
            "profile": profile,
            "posts": Post.objects.filter(author=profile).order_by('-timestamp'),
            "friend_request_available": not request.user.is_anonymous and not profile.user in request.user.profile.friends.all() and profile.user != request.user,
            "currently_friended": not request.user.is_anonymous and profile.user in request.user.profile.friends.all(),
            "friend_request_available": not request.user.is_anonymous and profile.user != request.user and not profile.user in request.user.profile.friends.all(),
        }
        
        if request.user.is_authenticated:
            context["self_in_friend_request"] = self_in_friend_request(profile.user, request.user)

            context["self_in_profile_friend_request"] = self_in_profile_friend_request(request.user, profile.user)
            
            if self_in_profile_friend_request(request.user, profile.user):
                friend_request = FriendRequest.objects.get(to_user=request.user, from_user=profile.user)
                context["friend_request_id"] = friend_request.id

            if request.user != profile.user:
                context["mutual_friends"] = mutual_friends(request.user.profile, profile)
                context["mutual_friends_amount"] = mutual_friends(request.user.profile, profile).count()

    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User matching query does not exist."})

    return render(request, "network/profile.html", context)


def self_in_friend_request(to_user, from_user):
    try:
        FriendRequest.objects.get(to_user=to_user, from_user=from_user)
        return True

    except FriendRequest.DoesNotExist:
        return False


def self_in_profile_friend_request(to_user, from_user):
    try:
        FriendRequest.objects.get(to_user=to_user, from_user=from_user)
        return True

    except FriendRequest.DoesNotExist:
        return False

def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        description = data.get("description")
        only_friends = data.get("only_friends")
        only_me = data.get("only_me")
        post = Post(author=request.user.profile, description=description, only_friends=only_friends, only_me=only_me)
        post.save()
        return JsonResponse({"message": "Post was created successfully."}, status=201)


def search(request):
    query = request.GET.get('q')
    post_query_list = Post.objects.filter(
        Q(description__icontains=query) | Q(author__user__username__icontains=query)
    )
    profile_query_list = UserProfile.objects.filter(
        Q(user__username__icontains=query)
    )
    return render(request, "network/index.html", {
        "posts": post_query_list,
        "profiles": profile_query_list,
        "search": True
    })


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
