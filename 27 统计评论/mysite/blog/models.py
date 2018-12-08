from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail



class BlogType(models.Model):
    type_name = models.CharField(verbose_name='博客类型',max_length=15)

    def count_blogs(self):
        return self.blog_set.count()
    #这个函数会在后台，我们看到的不是这个BlogType对象，而是显示name
    def __str__(self):
        return self.type_name

class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=50,verbose_name='标题')
    #博客类型和博客这里设置为多对一关系
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE,verbose_name='博客类型')
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户名')
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_updated_time = models.DateTimeField(auto_now=True,verbose_name='最后更新时间')
    #当创建一个新的博客之后，会显示博客标题
    def __str__(self):
        return "<Blog: %s>" % self.title
    class Meta:
        ordering = ['-created_time']


