# Generated by Django 4.1.10 on 2023-08-21 04:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tweets", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tweet",
            old_name="user",
            new_name="username",
        ),
    ]
