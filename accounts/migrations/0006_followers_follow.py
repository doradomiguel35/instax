# Generated by Django 2.1.4 on 2018-12-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_followers_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='followers',
            name='follow',
            field=models.BooleanField(default=False),
        ),
    ]
