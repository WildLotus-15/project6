from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<uuid:profile_id>", views.show_profile, name="profile"),
    path("send_friend_request/<uuid:profile_id>", views.send_friend_request, name="send_friend_request"),
    path("accept_friend_request/<uuid:requestID>", views.accept_friend_request, name="accept_friend_request"),
    path("decline_friend_request/<uuid:requestID>", views.decline_friend_request, name="decline_friend_request"),
    path("friend_requests", views.friend_requests, name="friend_requests"),
    path("friends", views.friends, name="friends"),
    path("remove_from_friends/<uuid:requestID>", views.remove_from_friends, name="remove_from_friends"),
    path("remove_profile_friend/<uuid:profile_id>", views.remove_profile_friend, name="remove_profile_friend"),
    path("cancel_friend_request/<uuid:profile_id>", views.cancel_friend_request, name="cancel_friend_request"),
    path("edit_profile_bio/<uuid:profile_id>", views.edit_profile_bio, name="edit_profile_bio"),
    path("search_results", views.search, name="search_results"),
    path("profile_friends/<uuid:profile_id>", views.profile_friends, name="profile_friends"),
    path("profile_mutuals/<uuid:profile_id>", views.profile_mutuals, name="profile_mutuals"),
    path("profile/<uuid:profile_id>/update_block", views.update_block, name="update_block"),
    path("blocked_users", views.blocked_users, name="blocked_users"),
    path("search", views.search_json, name="search_results_json"),
    path("recent_searches", views.recent_searches, name="recent_searches"),
    path("edit_profile_picture/<uuid:profile_id>", views.edit_profile_picture, name="edit_profile_picture"),
    path("post/<uuid:post_id>/comments", views.comments, name="comments"),
    path("post/<uuid:post_id>/comment", views.comment, name="comment"),
    path("post/<uuid:post_id>/update_reaction", views.update_reaction, name="update_reaction")
]