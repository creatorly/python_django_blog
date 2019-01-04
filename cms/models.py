from django.db import models
from django.utils import timezone


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)


# 用户
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.EmailField(max_length=20, null=False)
    email = models.EmailField(max_length=20, null=False, unique=True)
    image = models.ImageField(null=True)
    password = models.CharField(max_length=100, null=False)
    admin = models.NullBooleanField()
    add_date = models.DateTimeField('保存日期', default=timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now=True)

    def __str__(self):
        return '{"id": "%s", "name": "%s", "email": "%s", "password": "%s", "admin": "%s", "add_date": "%s"}' % (self.id, self.name, self.email, self.password, self.admin, self.add_date)

    __repr__ = __str__


# 分类
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)  # 分类名称
    author = models.ForeignKey("Users", on_delete=models.CASCADE, null=False)  # 分类创建者
    add_date = models.DateTimeField('分类创建日期', default=timezone.now)


# 博客文章
class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False)
    category = models.ManyToManyField("Category")
    author = models.ForeignKey("Users", on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False)
    add_date = models.DateTimeField('保存日期', default=timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now=True)


# 评论
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    article_id = models.ForeignKey("Articles", on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False)
    add_date = models.DateTimeField('保存日期', default=timezone.now)

