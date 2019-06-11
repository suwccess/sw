#coding=utf-8
from django.db import models

#订单信息
class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('df_user.UserInfo')
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    oaddress = models.CharField(max_length=150)
    oisdel = models.BooleanField(default=False)

#无法实现：真实支付，物流信息

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo')
    order = models.ForeignKey('df_order.OrderInfo')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()