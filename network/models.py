import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    pass


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField(default="No Bio...", max_length=101)
    picture = models.ImageField(default="default_profile_image.png")
    friends = models.ManyToManyField(to="self", blank=True, related_name="+", symmetrical=False)
    blocked = models.ManyToManyField(to="self", blank=True, related_name="+", symmetrical=False)


    def serialize(self, user):
        return {
            "username": self.user.username,
            "picture": self.picture.url,
            "currently_friended": self.user in user.profile.friends.all()
        }


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(UserProfile, related_name="+", on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name="+", on_delete=models.CASCADE)
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

    
class Block(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="+")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="+")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["from_user", "to_user"],
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_block",
                check=~models.Q(from_user=models.F("to_user")),
            ),
        ]


class RecentSearch(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "picture": self_in_user(self.content)
        }


def self_in_user(content):
    try:
        user = User.objects.get(username=content)

        return user.profile.picture.url

    except User.DoesNotExist:
        pass


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField()
    only_friends = models.BooleanField(default=False)
    only_me = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(UserProfile, blank=True, related_name="dislikes")


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def serialize(self):
        return {
            "post_id": self.post.id,
            "id": self.id,
            "author_id": self.author.id,
            "author_picture": self.author.picture.url,
            "author_username": self.author.user.username,
            "description": self.description,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }


@receiver(post_save, sender=User)
def create_user_profile(created, sender, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
