# Generated by Django 2.1.3 on 2018-12-03 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_auto_20181203_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likesmodel',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.AccountsModel'),
        ),
    ]