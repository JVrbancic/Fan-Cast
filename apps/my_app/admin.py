from django.contrib import admin

from .models import User, Topic, Post

# Register your models here.
admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Post)
