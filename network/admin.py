from django.contrib import admin
from .models import FriendRequest, UserProfile, User, Post, RecentSearch, Block, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(RecentSearch)
admin.site.register(FriendRequest)
admin.site.register(Block)
admin.site.register(Post)
admin.site.register(Comment)