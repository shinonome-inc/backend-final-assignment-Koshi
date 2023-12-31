# Generated by Django 4.1.10 on 2023-09-09 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_remove_friendship_unique_followuser_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="friendship",
            name="unique_follow_user",
        ),
        migrations.RemoveField(
            model_name="friendship",
            name="following",
        ),
        migrations.AddField(
            model_name="friendship",
            name="followee",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="friendships_as_followee",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="friendship",
            name="follower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="friendships_as_follower",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="friendship",
            constraint=models.UniqueConstraint(fields=("follower", "followee"), name="unique_follow_user"),
        ),
    ]
