from django.db import models

class CartInfo(models.Model):
    #关联别的应用的模型类
    user = models.ForeignKey('df_user.UserInfo')
    goods = models.ForeignKey('df_goods.GoodInfo')
    #购买数量
    count = models.IntegerField()
