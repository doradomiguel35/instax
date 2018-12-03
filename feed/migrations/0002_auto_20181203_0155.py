# Generated by Django 2.1.3 on 2018-12-03 01:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default=None, max_length=255)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.FeedModel')),
            ],
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='commented_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
