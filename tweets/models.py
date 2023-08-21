from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-create_date"]
