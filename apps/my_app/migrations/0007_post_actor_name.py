# Generated by Django 2.2 on 2019-04-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0006_auto_20190411_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='actor_name',
            field=models.CharField(default='jon doe', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
