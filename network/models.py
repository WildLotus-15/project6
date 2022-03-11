from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name="profile", on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def serialize(self, user):
        return {
            "profile_username": self.user.username,
            "friend_request_available": not user.is_anonymous and not self in user.friends.all() and self.user != user,
            "currently_friended": not user.is_anonymous and self in user.friends.all(),
            "self_in_friend_request": self_in_friend_request(self.user, user)  
        }


def self_in_friend_request(to_user, from_user):
    try:
        FriendRequest.objects.get(to_user=to_user, from_user=from_user)
        return True
    except FriendRequest.DoesNotExist:
        return False


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def serialize(self):
        return {
            "id": self.id,
            "from_user": self.from_user.username,
            "to_user": self.to_user.username,
            "from_user_id": self.from_user.id,
            "to_user_id": self.to_user.id
        }

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["from_user", "to_user"]
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_friending",
                check=~models.Q(from_user=models.F("to_user")),
            ),
        ]


class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=64)
    timestamp = models.DateTimeField(default=timezone.now)

    def serialize(self):
        return {
            "author_username": self.author.user.username,
            "author_id": self.author.user.id,
            "description": self.description,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }


@receiver(post_save, sender=User)
def create_user_profile(created, sender, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
