from django.contrib.auth.models import AbstractUser
from django.db import models

from mysite import settings


class User(AbstractUser):
    email = models.EmailField()


class FriendShip(models.Model):
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE)
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="follower", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "following"], name="unique_FollowUser"),
        ]
