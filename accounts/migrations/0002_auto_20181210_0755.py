# Generated by Django 2.1.4 on 2018-12-10 07:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FollowersModel',
            new_name='Followers',
        ),
    ]
