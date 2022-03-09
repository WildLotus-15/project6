from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("load_posts", views.load_posts, name="load_posts"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<int:profile_id>", views.show_profile, name="show_profile"),
    path("update_friend_request/<int:profile_id>", views.send_friend_request, name="update_friend_request"),
    path("accept_friend_request/<int:requestID>", views.accept_friend_request, name="accept_friend_request")
]