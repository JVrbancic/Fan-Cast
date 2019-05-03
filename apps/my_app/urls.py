from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('main', views.main),
    path('register', views.register),
    path('login', views.login),
    path('add', views.add),
    path('adder', views.adder),
    path('adder_post', views.adder_post),
    path('add-like', views.add_like),
    path('post-remove/<int:topic_id>/<int:post_id>', views.post_remove),
    path('like-remove/<int:topic_id>/<int:post_id>', views.like_remove),
    path('logout', views.logout),
    path('topic/<int:topic_id>', views.topic),
    path('post/<int:topic_id>', views.post),
    path('myaccount/<int:user_id>', views.myaccount),
    path('update', views.update),
    path('genre-com', views.genre_com),
    path('genre-vg', views.genre_vg),
    path('genre-book', views.genre_book),    
]