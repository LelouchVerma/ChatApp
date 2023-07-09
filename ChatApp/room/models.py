from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sent_by = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    time_added = models.TimeField(auto_now_add=True)

    class Meta:
        ordering = ('time_added',)


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message, blank=True)
    psswd = models.CharField(max_length=32)