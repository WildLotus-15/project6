from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<int:profile_id>", views.show_profile, name="profile"),
    path("send_friend_request/<int:profile_id>", views.send_friend_request, name="send_friend_request"),
    path("accept_friend_request/<int:requestID>", views.accept_friend_request, name="accept_friend_request"),
    path("decline_friend_request/<int:requestID>", views.decline_friend_request, name="decline_friend_request"),
    path("friend_requests", views.friend_requests, name="friend_requests"),
    path("friends/<int:profile_id>", views.friends, name="friends"),
    path("remove_from_friends/<int:requestID>", views.remove_from_friends, name="remove_from_friends"),
    path("remove_profile_friend/<int:profile_id>", views.remove_profile_friend, name="remove_profile_friend"),
    path("cancel_friend_request/<int:profile_id>", views.cancel_friend_request, name="cancel_friend_request"),
    path("edit_profile/<int:profile_id>", views.edit_profile, name="edit_profile"),
    path("search_results", views.search, name="search_results")
]