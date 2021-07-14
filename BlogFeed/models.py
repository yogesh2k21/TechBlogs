from typing import DefaultDict
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    content=models.CharField(max_length=100000)
    author=models.CharField(max_length=50)
    slug=models.CharField(max_length=150)
    views= models.IntegerField(default=0)
    date=DateTimeField(blank=True)
    image = models.ImageField(upload_to="", default="")
    category=models.CharField(max_length=20)
    def __str__(self):
        return self.title+' by '+self.author

class BlogComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username