# Generated by Django 2.1.4 on 2018-12-14 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181210_0755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followers',
            name='user',
        ),
        migrations.DeleteModel(
            name='Followers',
        ),
    ]
