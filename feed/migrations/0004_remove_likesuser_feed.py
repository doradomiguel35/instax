# Generated by Django 2.1.4 on 2018-12-26 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20181226_0141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likesuser',
            name='feed',
        ),
    ]