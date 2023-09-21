from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from mysite import settings

User = get_user_model()


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_at"]


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="like_tweet")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "tweet"], name="unique_like")]
