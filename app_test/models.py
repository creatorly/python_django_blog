from django.db import models


# for test html data save
class UserInfo(models.Model):
    user = models.CharField(max_length=32, null=False)
    pwd = models.CharField(max_length=32, null=False)
