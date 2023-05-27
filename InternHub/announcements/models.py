from django.db import models
from users.models import User
from datetime import datetime


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # User model is imported

    def __str__(self):
        return self.title


class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)  # User model is imported
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def create_notification(cls, title, content, receiver):
        notification = cls.objects.create(
            title=title,
            content=content,
            receiver=receiver
        )
        notification.save()
        return notification
