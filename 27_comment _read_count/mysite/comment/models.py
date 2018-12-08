from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()  #不限字数
    comment_time = models.DateTimeField(auto_now_add=True)  #创建时间

    user = models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)  #关联内置用户表 指向谁写的评论

    root = models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.CASCADE)  #用于表示一级评论
    parent = models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.CASCADE)  #用于表示回复的评论
    reply_to = models.ForeignKey(User,related_name="replies",null=True,on_delete=models.CASCADE)  #回复谁 related_name 用于反向解析属性

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
