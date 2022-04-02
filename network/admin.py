from django.contrib import admin
from .models import FriendRequest, UserProfile, User, Post, RecentSearch

# Register your models here.
admin.site.register(FriendRequest)
admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(RecentSearch)