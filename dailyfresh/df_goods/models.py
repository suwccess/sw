#coding=utf-8
from django.db import models
from tinymce.models import HTMLField
#商品分类
class TypeInfo(models.Model):
    ttitle=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)
    def __str__(self):
        return "%s" % self.ttitle.encode('utf-8')

class GoodsInfo(models.Model):
    gtitle=models.CharField(max_length=20)
    gpic=models.ImageField(upload_to='df_goods')
    gprice=models.DecimalField(max_digits=5, decimal_places=2)
    isDelete=models.BooleanField(default=False)
    gunit=models.CharField(max_length=20, default='500g')
    gjianjie=models.CharField(max_length=200)
    gclick=models.IntegerField()
    gkucun=models.IntegerField()
    gcontent=HTMLField()
    gtype=models.ForeignKey(TypeInfo)
    # gadv=models.BooleanField(default=False)