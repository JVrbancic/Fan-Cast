# Generated by Django 2.2 on 2019-04-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0007_post_actor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='liked_by',
            field=models.ManyToManyField(related_name='post_liked', to='my_app.User'),
        ),
    ]