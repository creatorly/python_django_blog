from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('login/', views.login),
    path('register/', views.register),
    path('blogs/', views.blogs),
    path('blogs/create/', views.create),
    path('users/', views.users),
    path('comments/', views.comments),
    path('blog_img_upload/', views.blog_img_upload, name="blog_img_upload"),

]