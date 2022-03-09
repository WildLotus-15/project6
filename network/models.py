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
    friends = models.ManyToManyField(User, blank=True)

    def serialize(self):
        return {
            "profile_username": self.user.username
        }


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=64)
    timestamp = models.DateField(default=timezone.now)

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
