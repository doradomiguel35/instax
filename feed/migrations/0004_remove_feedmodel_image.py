# Generated by Django 2.1.3 on 2018-12-04 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20181203_0830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedmodel',
            name='image',
        ),
    ]
