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
    name = models.CharField(max_length=64, blank=True, null=True)
    bio = models.TextField(blank=True)
    picture = models.ImageField(blank=True, default="default_profile_image.png")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    blocked = models.ManyToManyField(User, blank=True, related_name="blocked")


    def serialize(self, user):
        return {
            "username": self.user.username,
            "picture": self.picture.url,
            "currently_friended": self.user in user.profile.friends.all()
        }


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

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


class RecentSearch(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content
        }


class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=64)
    only_friends = models.BooleanField(default=False)
    only_me = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)


@receiver(post_save, sender=User)
def create_user_profile(created, sender, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
