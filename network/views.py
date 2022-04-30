import json
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Block, FriendRequest, Post, RecentSearch, User, UserProfile, Comment

# Create your views here.
@login_required
def index(request):
    return render(request, "network/index.html", {
        "posts": ignore_blocked_users_posts(request.user.profile),
    })


@login_required
def recent_searches(request):
    recent_searches = RecentSearch.objects.filter(from_user=request.user.profile).order_by('-timestamp').all()
    return JsonResponse([recent_search.serialize() for recent_search in recent_searches], safe=False)


@login_required
def ignore_blocked_users_posts(profile):
    blocked_profiles = profile.blocked.all()
    posts = Post.objects.filter(
        ~Q(author__in=blocked_profiles)
    ).order_by('-timestamp')
    return posts


@login_required
def update_block(request, profile_id):
    try:
        from_user = request.user.profile
        to_user = UserProfile.objects.get(id=profile_id)

        try:
            friend_request = FriendRequest.objects.get(
                Q(from_user=from_user, to_user=to_user) | Q(from_user=from_user, to_user=to_user)
            )

            friend_request.delete()
            from_user.friends.remove(to_user)
            to_user.user.profile.friends.remove(from_user)

        except FriendRequest.DoesNotExist:
            pass

        block, created = Block.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            from_user.blocked.add(to_user)
        else:
            from_user.blocked.remove(to_user)

        blocked_users_amount = from_user.blocked.all().count()
        
    except User.DoesNotExist:
        return JsonResponse({"error": "User matching query does not exist."}, status=400)

    return JsonResponse({"message": "Updated user block successfully.", "newAmount": blocked_users_amount}, status=200)


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
        profile = UserProfile.objects.get(id=profile_id)

        friends = profile.friends.all()

        friend_requests = FriendRequest.objects.filter(
            Q(from_user__in=friends, to_user=profile, active=False) | Q(to_user__in=friends, from_user=profile, active=False)
        )

    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User matching query does not exist."}, status=400)
    
    return render(request, "network/profile_friends.html", {
        "profile": profile,
        "friends": friend_requests
    })


@login_required
def send_friend_request(request, profile_id):
    from_user = request.user.profile

    try:
        to_user = UserProfile.objects.get(id=profile_id)

        if not from_user in to_user.blocked.all() or not to_user in from_user.blocked.all():

            if not to_user in from_user.friends.all() or not from_user in to_user.friends.all():
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

        from_user = friend_request.from_user
        to_user = friend_request.to_user

        if to_user == request.user.profile:
            to_user.friends.add(from_user)
            from_user.friends.add(to_user)

            friend_request.active = False
            friend_request.save()

            friend_requests_amount = FriendRequest.objects.filter(to_user=request.user.profile, active=True).all().count()
        else:
            return JsonResponse({"error": "You do not have the right to perform this action."}, status=403)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Friend request matching query does not exist."}, status=400)

    return JsonResponse({"message": "New friend has been added successfully.", "newAmount": friend_requests_amount}, status=201)


@login_required
def friend_requests(request):
    context = {}

    friend_requests = FriendRequest.objects.filter(to_user=request.user.profile, active=True).all()
    context["friend_requests"] = friend_requests

    # from_users = friend_requests.values_list('from_user', flat=True)
    # print(from_users)

    # from_users_profiles = UserProfile.objects.filter(pk__in=from_users).all()
    # print(from_users_profiles)

    # for from_user_profile in from_users_profiles:
        # from_user_friends = from_user_profile.friends.values_list('pk', flat=True)
        # print(from_user_friends)
    
        # mutual_friends = request.user.profile.friends.filter(pk__in=from_user_friends).all()
        # print(mutual_friends)

        # NEED TO FIX THIS GLOBAL MUTUAL FRIENDS VARIABLE
        # ALL FRIENDS MUST HAVE SPECIFIC TO THEM MUTUAL FRIEND LISTS IN RELATION TO REQUEST USER

        # context["mutual_friends"] = mutual_friends
        # context["mutual_friends_amount"] = mutual_friends.count()

    return render(request, "network/friend_requests.html", context)


@login_required
def edit_profile_bio(request, profile_id):
    if request.method == "POST":

        try:
            profile = UserProfile.objects.get(id=profile_id)

            if request.user == profile.user:
                new_bio = request.POST["new_bio"]
                # If the user cleared their bio it's value will fall back to the default configuration 
                if new_bio == "":
                    profile.bio = "No Bio..."
                else:
                    profile.bio = new_bio
                    
                profile.save()
                
                return JsonResponse({"message": "Profile bio was updated successfully."}, status=201)

            else:
                return JsonResponse({"error": "You do not have the right to perform this action."}, status=403)

        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile matching query does not exist."}, status=400)
        
    else:
        return JsonResponse({"POST request method required."}, status=400)


@login_required
def edit_profile_picture(request, profile_id):
    if request.method == "POST":

        try:
            profile = UserProfile.objects.get(id=profile_id)

            if request.user == profile.user:
                if request.FILES:
                    new_picture = request.FILES["new_picture"]
                    profile.picture = new_picture
                else:
                    # If the user removed their picture it's value will fall back to default configuration 
                    profile.picture = "default_profile_image.png"

                profile.save()
                           
                return JsonResponse({"message": "Profile picture was updated successfully.", "new_picture_url": profile.picture.url}, status=201)

            else:
                return JsonResponse({"error": "You do not have the right to perform this action."}, status=403)

        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile matching query does not exist."}, status=400)
        
    else:
        return JsonResponse({"POST request method required."}, status=400)


@login_required
def remove_profile_friend(request, profile_id):
    try:
        to_user = UserProfile.objects.get(id=profile_id)
        from_user = request.user.profile

        to_user.friends.remove(from_user.profile)
        from_user.friends.remove(to_user.profile)

        friend_request = FriendRequest.objects.get(
            Q(from_user=from_user, to_user=to_user, active=False) | Q(from_user=to_user, to_user=from_user, active=False)
        )
        friend_request.delete()

    except (User.DoesNotExist, FriendRequest.DoesNotExist) as e:
        return JsonResponse({"error": "User or Friend Request matching query does not exist."}, status=400)

    return JsonResponse({"message": "Friend has been successfully removed."}, status=201)


@login_required
def cancel_friend_request(request, profile_id):
    try:
        to_user = UserProfile.objects.get(pk=profile_id)
        from_user = request.user.profile

        friend_request = FriendRequest.objects.get(from_user=from_user, to_user=to_user, active=True)

        if friend_request.from_user == from_user:
            friend_request.delete()

    except (User.DoesNotExist, FriendRequest.DoesNotExist) as e:
        return JsonResponse({"error": "User or Friend Request matching query does not exist."}, status=400)

    return JsonResponse({"message": "Friend request has been successfully unsent."}, status=201)


@login_required
def decline_friend_request(request, requestID):
    try:
        friend_request = FriendRequest.objects.get(pk=requestID)
        if request.user.profile == friend_request.to_user:
            friend_request.delete()
            friend_requests_amount = FriendRequest.objects.filter(to_user=request.user.profile, active=True).all().count()
        else:
            return JsonResponse({"error": "You do not have the right to perform this action."}, status=403)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Specified friend request does not exist."}, status=400)

    return JsonResponse({"message": "Friend request has been declined successfully.", "newAmount": friend_requests_amount}, status=201)


@login_required
def remove_from_friends(request, requestID):
    try:
        friend_request = FriendRequest.objects.get(pk=requestID)

        to_user = friend_request.to_user
        from_user = friend_request.from_user

        if request.user.profile == to_user or request.user.profile == from_user:
            from_user.friends.remove(to_user)
            to_user.friends.remove(from_user)
            friend_request.delete()

            friends_amount = request.user.profile.friends.all().count()
        else:
            return JsonResponse({"error": "You do not have the right to perform this action."}, status=403)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Specified friend request does not exist."}, status=400)

    return JsonResponse({"message": "Friend has been successfully removed.", "newAmount": friends_amount}, status=201)


@login_required
def friends(request):
    try:
        user = request.user.profile

        friends = user.friends.all()

        friend_requests = FriendRequest.objects.filter(
            Q(from_user__in=friends, to_user=user, active=False) | Q(to_user__in=friends, from_user=user, active=False)
        )

        context = {}

        context["friends"] = friend_requests

        # for friend_request in friend_requests:
            # if friend_request.to_user == profile.user:
                # requests_friends = friend_requests.values_list('from_user', flat=True)
            # else:
                # requests_friends = friend_requests.values_list('to_user', flat=True)

            # requests_profiles = UserProfile.objects.filter(pk__in=requests_friends)
            # friends_with_profile = profile.friends.values_list('pk', flat=True)

            # for request_profile in requests_profiles:
                # request_friends = request_profile.friends.filter(pk__in=friends_with_profile)
                # print(request_friends)

            # NEED TO FIX THIS GLOBAL MUTUAL FRIENDS VARIABLE
            # ALL FRIENDS MUST HAVE SPECIFIC TO THEM MUTUAL FRIEND LISTS IN RELATION TO REQUEST USER

            # context["mutual_friends"] = request_friends
            # context["mutual_friends_amount"] = request_friends.count()

    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User profile matching query does not exist."}, status=400)

    return render(request, "network/friends.html", context)


@login_required
def profile_mutuals(request, profile_id):
    try:
        profile = UserProfile.objects.get(id=profile_id)

        profile_friends = profile.friends.all()
        friends_with_profile = profile_friends.values_list('pk', flat=True)
        mutual_friends = request.user.profile.friends.filter(pk__in=friends_with_profile)
    
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "UserProfile matching query does not exist."})
    
    return render(request, "network/profile_mutuals.html", {
        "profile": profile,
        "mutual_friends": mutual_friends
    })


@login_required
def mutual_friends(request_user, profile):
    profile_friends = profile.friends.all()
    friends_with_profile = profile_friends.values_list('pk', flat=True)
    mutual_friends_of_request_user = request_user.friends.filter(pk__in=friends_with_profile)
    return mutual_friends_of_request_user


@login_required
def show_profile(request, profile_id):
    try:
        profile = UserProfile.objects.get(id=profile_id)

        context = {
            "profile": profile,
            "posts": Post.objects.filter(author=profile).order_by('-timestamp'),
            "friend_request_available": not profile in request.user.profile.friends.all() and not profile in request.user.profile.blocked.all() and profile.user != request.user,
            "currently_friended": profile in request.user.profile.friends.all(),
            "self_in_friend_request": self_in_friend_request(profile, request.user.profile),
            "self_in_profile_friend_request": self_in_profile_friend_request(request.user.profile, profile)
        }
                
        if self_in_profile_friend_request(request.user.profile, profile):
            friend_request = FriendRequest.objects.get(to_user=request.user.profile, from_user=profile)
            context["friend_request_id"] = friend_request.id

        if request.user != profile.user:
            context["mutual_friends"] = mutual_friends(request.user.profile, profile)
            context["mutual_friends_amount"] = mutual_friends(request.user.profile, profile).count()

    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User matching query does not exist."})

    return render(request, "network/profile.html", context)


def self_in_friend_request(to_user, from_user):
    try:
        FriendRequest.objects.get(to_user=to_user, from_user=from_user, active=True)
        return True

    except FriendRequest.DoesNotExist:
        return False


def self_in_profile_friend_request(to_user, from_user):
    try:
        FriendRequest.objects.get(to_user=to_user, from_user=from_user, active=True)
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


@login_required
def search(request):
    query = request.GET.get('q')

    blocked_profiles = request.user.profile.blocked.all()

    blocked_users = User.objects.filter(profile__in=blocked_profiles).all()

    post_query_list = Post.objects.filter(
        Q(description__icontains=query) | Q(author__user__username__icontains=query) & ~Q(author__in=blocked_profiles)
    )

    profile_query_list = UserProfile.objects.filter(
        Q(user__username__icontains=query) & ~Q(user__in=blocked_users)
    )

    recent_search, created = RecentSearch.objects.get_or_create(from_user=request.user.profile, content=query)
    if not created:
        recent_search.timestamp = timezone.now()
        recent_search.save()
    
    try:
        user = User.objects.get(username=query)

        return HttpResponseRedirect(reverse("profile", args=(user.profile.id,)))
    except User.DoesNotExist:
        pass

    return render(request, "network/index.html", {
        "posts": post_query_list,
        "profiles": profile_query_list,
        "search": True
    })


@login_required
def search_json(request):
    query = request.GET.get('q')

    query_list = []

    blocked_profiles = request.user.profile.blocked.all()
    blocked_users = User.objects.filter(profile__in=blocked_profiles)

    if query:      
        profile_query_list = UserProfile.objects.filter(
            Q(user__username__icontains=query) & ~Q(user__in=blocked_users)
        )

        for profile in profile_query_list:
            query_list.append(profile.serialize(request.user))

    return JsonResponse({
        "query_list": query_list
    })


@login_required
def comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)

        comments = post.comments.all().order_by('-timestamp')

        return JsonResponse({
            "comments": [comment.serialize() for comment in comments]
        }, safe=False)

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post matching query does not exist."}, status=400)


@login_required
def comment(request, post_id):
    if request.method == "POST":

        try:
            post = Post.objects.get(id=post_id)

            data = json.loads(request.body)
            description = data.get("comment")
            comment = Comment(post=post, author=request.user.profile, description=description)
            comment.save()

            newAmount = post.comments.count()

            return JsonResponse({"message": "Comment was added successfully.", "newAmount": newAmount}, status=201)

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post matching query does not exist."}, status=400)

    else:
        return JsonResponse({"error": "POST request method required."}, status=400)


@login_required
def update_reaction(request, post_id):
    if request.method == "POST":

        try:
            post = Post.objects.get(id=post_id)

            data = json.loads(request.body)

            if data["reaction"] == "like":
                if request.user.profile in post.likes.all():
                    post.likes.remove(request.user.profile)
                    newStatus = False
                else:
                    post.likes.add(request.user.profile)
                    newStatus = True

            else:
                if request.user.profile in post.dislikes.all():
                    post.dislikes.remove(request.user.profile)
                    newStatus = False
                else:
                    post.dislikes.add(request.user.profile)
                    newStatus = True

            newAmount = post.likes.all().count() + post.dislikes.all().count()

            return JsonResponse({"message": "Reaction was updated successfully.", "newStatus": newStatus, "newAmount": newAmount}, status=201)

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post matching query does not exist."}, status=400)

    else:
        return JsonResponse({"error": "POST request method required."}, status=400)


def delete_post(request, post_id):
    if request.method == "DELETE":

        try:
            post = Post.objects.get(id=post_id)

            if post.author == request.user.profile:
                post.delete()
            
            else:
                return JsonResponse({"error": "You are not the author of the post matching query."}, status=403)
            
            return JsonResponse({"message": "Post was deleted successfully."}, status=201)

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post matching query does not exist."}, status=400)

    else:
        return JsonResponse({"error": "DELETE request method required."}, status=400)
    

def edit_post(request, post_id):
    if request.method == "PUT":

        try:
            post = Post.objects.get(id=post_id)

            if post.author == request.user.profile:
                data = json.loads(request.body)
                post.description = data["description"]
                post.only_me = data["only_me"]
                post.only_friends = data["only_friends"]
                post.save()

                if post.only_friends:
                    newVisibility = "only_friends"
                else:
                    newVisibility = "only_me"
            
            else:
                return JsonResponse({"error": "You are not the author of the post matching query."}, status=403)
            
            return JsonResponse({"message": "Post was updated successfully.", "newVisibility": newVisibility}, status=201)

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post matching query does not exist."}, status=400)

    else:
        return JsonResponse({"error": "PUT request method required."}, status=400)