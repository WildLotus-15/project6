import json
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FriendRequest, Post, RecentSearch, User, UserProfile
from .forms import EditProfileForm
from django.core import serializers

# Create your views here.
@login_required
def index(request):
    recent_searches = RecentSearch.objects.filter(from_user=request.user).order_by('-timestamp').all()
    historicals = serializers.serialize("json", RecentSearch.objects.filter(from_user=request.user).order_by('-timestamp').all(), fields=["id", "content"])
    print(historicals)
    return render(request, "network/index.html", {
        "posts": ignore_blocked_users(request.user.profile),
        "recent_searches": recent_searches,
        "historicals": historicals
    })


def recent_searches(request):
    recent_searches = RecentSearch.objects.filter(from_user=request.user).order_by('-timestamp').all()
    return JsonResponse([recent_search.serialize() for recent_search in recent_searches], safe=False)


@login_required
def ignore_blocked_users(profile):
    blocked_users = profile.blocked.all()
    blocked_users_profiles = UserProfile.objects.filter(user__in=blocked_users).all()
    posts = Post.objects.filter(
        ~Q(author__in=blocked_users_profiles)
    ).order_by('-timestamp')
    return posts


@login_required
def update_block(request, profile_id):
    try:
        user = User.objects.get(pk=profile_id)

        try:
            friend_request = FriendRequest.objects.get(
                Q(from_user=request.user, to_user=user) | Q(from_user=user, to_user=request.user)
            )

            friend_request.delete()
            user.profile.friends.remove(request.user)
            request.user.profile.friends.remove(user)

        except FriendRequest.DoesNotExist:
            pass

        if user in request.user.profile.blocked.all():
            request.user.profile.blocked.remove(user)
        else:
            request.user.profile.blocked.add(user)
        
    except User.DoesNotExist:
        return JsonResponse({"error": "User matching query does not exist."}, status=400)

    return JsonResponse({"message": "Updated user block, friendship successfully."}, status=200)


@login_required
def blocked_users(request):
    blocked_users = request.user.profile.blocked.all()
    print(blocked_users)
    return render(request, "network/blocked_users.html", {
        "blocked_users": blocked_users
    })


@login_required
def profile_friends(request, profile_id):
    try:
        profile = UserProfile.objects.get(pk=profile_id)

        friends = profile.friends.all()

        friend_requests = FriendRequest.objects.filter(
            Q(from_user__in=friends, to_user=profile.user) | Q(to_user__in=friends, from_user=profile.user)
        )

    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User matching query does not exist."}, status=400)
    
    return render(request, "network/profile_friends.html", {
        "profile": profile,
        "friends": friend_requests
    })


@login_required
def send_friend_request(request, profile_id):
    from_user = request.user

    try:
        to_user = User.objects.get(pk=profile_id)

        if not from_user in to_user.profile.blocked.all() or not to_user in from_user.profile.blocked.all():

            if not from_user in to_user.profile.blocked.all() or to_user in from_user.profile.blocked.all():
                if not to_user in from_user.profile.friends.all() or not from_user in to_user.profile.friends.all():
                    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
                    if created:
                        return JsonResponse({"message": "Friend request was sent successfully."}, status=201)
                    else:
                        return JsonResponse({"message": "Friend request has been already sent."}, status=409)

                else:
                    return JsonResponse({"error": "You are already friends."}, status=409)
            
        else:
            return JsonResponse({"error": "User matching query has blocked you."}, status=400)
        
    except User.DoesNotExist:
        return JsonResponse({"error": "User matching query does not exist."}, status=400)


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def friends(request):
    try:
        profile = UserProfile.objects.get(pk=request.user.id)

        friends = profile.friends.all()

        friend_requests = FriendRequest.objects.filter(
            Q(from_user__in=friends, to_user=request.user) | Q(to_user__in=friends, from_user=request.user)
        )

        context = {}

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


@login_required
def profile_mutuals(request, profile_id):
    try:
        profile = UserProfile.objects.get(pk=profile_id)

        profile_friends = profile.friends.all()
        friends_with_profile = profile_friends.values_list('pk', flat=True)
        mutual_friends_of_request_user = request.user.profile.friends.filter(pk__in=friends_with_profile)
        print(friends_with_profile)
    
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "UserProfile matching query does not exist."})
    
    return render(request, "network/profile_mutuals.html", {
        "profile": profile,
        "mutual_friends": mutual_friends_of_request_user
    })


def mutual_friends(request_user, profile):
    profile_friends = profile.friends.all()
    friends_with_profile = profile_friends.values_list('pk', flat=True)
    mutual_friends_of_request_user = request_user.friends.filter(pk__in=friends_with_profile)
    print(friends_with_profile)
    return mutual_friends_of_request_user


def limited_mutual_friends(request_user, profile):
    profile_friends = profile.friends.all()[:9]
    friends_with_profile = profile_friends.values_list('pk', flat=True)
    mutual_friends_of_request_user = request_user.friends.filter(pk__in=friends_with_profile)
    print(mutual_friends_of_request_user)
    return mutual_friends_of_request_user


def show_profile(request, profile_id):
    try:
        profile = UserProfile.objects.get(pk=profile_id)

        context = {
            "profile": profile,
            "posts": Post.objects.filter(author=profile).order_by('-timestamp'),
            "friend_request_available": not request.user.is_anonymous and not profile.user in request.user.profile.friends.all() and profile.user != request.user and not profile.user in request.user.profile.blocked.all(),
            "currently_friended": not request.user.is_anonymous and profile.user in request.user.profile.friends.all(),
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

                if context["mutual_friends_amount"] >= 8:
                    context["limited_mutual_friends"] = limited_mutual_friends(request.user.profile, profile)

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

    elif request.method == "GET":
        return JsonResponse({"error": "POST request required."}, status=400)


def search(request):
    query = request.GET.get('q')

    blocked_users = request.user.profile.blocked.all()

    blocked_users_profiles = UserProfile.objects.filter(user__in=blocked_users).all()

    post_query_list = Post.objects.filter(
        Q(description__icontains=query) | Q(author__user__username__icontains=query) & ~Q(author__in=blocked_users_profiles)
    )

    profile_query_list = UserProfile.objects.filter(
        Q(user__username__icontains=query) & ~Q(user__in=blocked_users)
    )

    recent_search, created = RecentSearch.objects.get_or_create(from_user=request.user, content=query)
    if not created:
        recent_search.timestamp = timezone.now()
        recent_search.save()
    
    try:
        profile = User.objects.get(username=query)

        return HttpResponseRedirect(reverse("profile", args=(profile.id,)))
    except User.DoesNotExist:
        pass

    return render(request, "network/index.html", {
        "posts": post_query_list,
        "profiles": profile_query_list,
        "search": True
    })


def search_json(request):
    query = request.GET.get('q')

    query_list = []

    blocked_users = request.user.profile.blocked.all()

    if query:      
        profile_query_list = UserProfile.objects.filter(
            Q(user__username__icontains=query) & ~Q(user__in=blocked_users)
        )

        for profile in profile_query_list:
            query_list.append(profile.serialize(request.user))

    return JsonResponse({
        "query_list": query_list
    })
