from django.db import models

# Create your models here.

# for test html data save
class UserInfo(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
