from django.db import models

# Create your models here.

class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)
    user = models.ForeignKey(User,related_name='topic_written', on_delete=models.CASCADE)
    poster = models.ManyToManyField(User, through='Post')
    image = models.ImageField(upload_to='topic_image', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
    user = models.ForeignKey(User,related_name='post_written', on_delete=models.CASCADE)
    actor_name = models.CharField(max_length=255, unique=True)
    topic = models.ForeignKey(Topic,related_name='topics', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='post_liked')
    image = models.ImageField(upload_to='post_image', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


