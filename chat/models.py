from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.author.username}: {self.content} on {self.timestamp}"


    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]