from django.db import models
from tkinter import CASCADE
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
# class User(models.Model):
#     fullname = models.CharField(max_length=50)
#     username = models.CharField(max_length=30)
#     email = models.EmailField()
#     password = models.CharField

class Posts(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
    date = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by ' + self.user_id.username

# class Pict(models.Model):
#     pict = models.ImageField(upload_to='images', null=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)