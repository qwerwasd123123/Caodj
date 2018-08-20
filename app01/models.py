from django.db import models

# Create your models here.
class Img(models.Model):

    src = models.FileField(max_length=32,verbose_name='图片路径',upload_to='static/upload')
    title = models.CharField(max_length=16,verbose_name='标题')
    summary = models.CharField(max_length=128,verbose_name='简介')

    class Meta:
        verbose_name_plural = '图片'
    def __str__(self):
        return self.title
class User(models.Model):
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    img = models.ImageField(upload_to='logo')
    class Meta:
        verbose_name_plural = '用户'
class Blog(models.Model):
    surfix = models.CharField(max_length=1000000)
    theme = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)
    key_user = models.ForeignKey('User',unique=True,on_delete=None)
    key_classify= models.ForeignKey('Blog',on_delete=None)
    key_label = models.ForeignKey('Label',on_delete=None)
    class Meta:
        verbose_name_plural="博客"
class Fanstoeach(models.Model):
    idol = models.ForeignKey('User',on_delete=None,related_name="idone")
    pm = models.ForeignKey('User',on_delete=None,related_name="idanthor")
    class Meta:
        verbose_name_plural="互粉"
class Suberror(models.Model):
    title  = models.CharField(max_length=100)
    detail  = models.CharField(max_length=100)
    user = models.ForeignKey('User',on_delete=None,related_name="subuser")
    processor = models.ForeignKey('User',on_delete=None,related_name="douser")
    status  = models.CharField(max_length=100)
    do_time  = models.CharField(max_length=100)
    do_what = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="保障单"
class Classify(models.Model):
    caption = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="分类"
class Label(models.Model):
    caption = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="标签"
class Word(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=100)
    ctime = models.TimeField()
    key_classify= models.ForeignKey('Classify',on_delete=None)
    class Meta:
        verbose_name_plural="文章"
class WordToLable(models.Model):
    wordid = models.ForeignKey('Word',on_delete=None)
    labelid = models.ForeignKey('Label',on_delete=None)
    class Meta:
        verbose_name_plural="文章分类"




