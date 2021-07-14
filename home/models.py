from django.db import models
from django.db.models.fields import DateField, DateTimeField

# Create your models here.
class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    phone=models.CharField(max_length=10)
    issue=models.CharField(max_length=500)
    date=DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return 'Message No. '+str(self.sno)+' from '+str(self.email)
    
