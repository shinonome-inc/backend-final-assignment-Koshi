from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Tweet(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    content = models.CharField(max_length=200)
    create_date = models.DateTimeField(default=timezone.now)
