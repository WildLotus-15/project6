from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=64)
    picture = models.ImageField(null=True, default="messenger.png")
    users = models.ManyToManyField(User, related_name="joined_groups", blank=True)


class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.author.username}: {self.content} in {self.group.name} on {self.timestamp}."


    def last_10_messages(group):
        return Message.objects.filter(group=group).all()
