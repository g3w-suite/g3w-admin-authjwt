# Generated by Django 3.0.3 on 2020-03-02 21:13

from django.db import migrations
from django.contrib.auth import get_user_model

def create_user(apps, schema_editor):
    """
    Create Django superuser if it doesn't exist
    """

    User = get_user_model()  # get the currently active user model

    if ( False == User.objects.filter(username='admin').exists() ) :
        User.objects.create_superuser(
            username = "admin",
            password = "admin",
            email    = "admin@example.com"
        )


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_user)
    ]
