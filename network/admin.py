from django.contrib import admin
from .models import FriendRequest, UserProfile, User

# Register your models here.
admin.site.register(FriendRequest)
admin.site.register(UserProfile)
admin.site.register(User)