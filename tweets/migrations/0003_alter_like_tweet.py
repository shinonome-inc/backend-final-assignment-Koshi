# Generated by Django 4.1.10 on 2023-09-21 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tweets", "0002_like_like_unique_like"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="tweet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="like_tweet", to="tweets.tweet"
            ),
        ),
    ]
