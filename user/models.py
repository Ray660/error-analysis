from django.db import models
from master.models import *

# Create your models here.
class UserInformation(models.Model):
    username = models.CharField('用户名', max_length=11, unique=True)
    password = models.CharField('密码', max_length=32)
    phonenum = models.CharField('手机号', max_length=11)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    edited_time = models.DateTimeField('最近修改时间', auto_now=True)
    is_active = models.BooleanField('是否活跃', default=True)

    def __str__(self):
        return self.username


class WrongQuestion(models.Model):
    wrong_pointid = models.IntegerField('错误知识点id', default=0, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    edited_time = models.DateTimeField('最近修改时间', auto_now=True)
    is_active = models.BooleanField('是否活跃', default=True)
    level_mastery = models.IntegerField('掌握程度', default=1)

    user = models.ForeignKey('UserInformation', on_delete=models.CASCADE)
    point = models.OneToOneField(KnowledgePoints, on_delete=models.CASCADE)
