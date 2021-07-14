from django.contrib import admin
from django.urls import path,include
from . import views
admin.site.site_header="TechBlog"
admin.site.site_title="TechBlog"
admin.site.index_title="Welcome to TechBlog Admin Panel"
#use "/" after urls's keyword
urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('postComment/',views.postComment,name='postcomment'),
    path('<str:slug>/', views.blogPost, name='blogPost'),
]
 