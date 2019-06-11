#coding=utf-8
from django.shortcuts import render, HttpResponse
from django.db import transaction
from django.http import JsonResponse

from datetime import datetime
from decimal import Decimal

from models import *
from df_cart.models import CartInfo
from df_user.models import UserInfo
from df_user import user_decorator

@user_decorator.login
def order(request):
    uid = request.session['user_id']
    # user = UserInfo.objects.filter(id=uid)
    user = UserInfo.objects.get(id=uid)
    cart_ids = request.GET.getlist('cart_id')
    carts = []
    total_price = 0
    for goods_id in cart_ids:
        cart = CartInfo.objects.get(id=goods_id)
        carts.append(cart)
        total_price = total_price + float(cart.count) * float(cart.goods.gprice)

    total_price = float('%0.2f' % total_price)
    trans_cost = 10 #运费
    total_trans_price = trans_cost + total_price
    context = {
        'title': '提交订单',
        'page_name': 1,
        'user': user,
        'carts': carts,
        'total_price': total_price,
        'trans_cost': trans_cost,
        'total_trans_price': total_trans_price,
    }
    return render(request, 'df_order/place_order.html', context)

'''
事务提交：
这些步骤中，任何一环节一旦出错则全部退回1
1. 创建订单对象
2. 判断商品库存是否充足
3. 创建 订单 详情 ，多个
4，修改商品库存
5. 删除购物车
'''
@user_decorator.login
@transaction.atomic()           #事务
def order_handle(request):
    tran_id = transaction.savepoint()   #保存事务发生点
    cart_ids = request.POST.get('cart_ids')
    user_id = request.session['user_id']
    data = {}
    try:
        order_info = OrderInfo()    #创建一个订单对象
        now = datetime.now()
        # print(now)
        order_info.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), user_id),  #订单号为订单提交时间和用户id的拼接
        order_info.odate = now  #订单时间
        order_info.user_id = int(user_id)   #订单的用户id
        order_info.ototal = Decimal(request.POST.get('total'))  #从前端获取的订单总价
        order_info.save()

        for cart_id in cart_ids.split(','): #逐一对用户订单中每类商品即每一个小购物车
            cart = CartInfo.objects.get(pk=cart_id) #从CartInfo表中获取小购物车对象
            order_detail = OrderDetailInfo()
            order_detail.order = order_info     #外键关联，小订单与大订单绑定
            goods = cart.goods  #具体商品
            if cart.count<= goods.gkucun:   #判断库存是否满足订单
                goods.gkucun = goods.gkucun - cart.count
                goods.save()
                order_detail.goods = goods
                order_detail.price = goods.gprice
                order_detail.count = cart.count
                order_detail.save()
                cart.delete()   #删除当前购物车
            else:   #否则，事务回滚
                transaction.savepoint_rollback(tran_id)
                return  HttpResponse('库存不足')
        data['ok'] = 1
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print("%s" % e)
        print("未完成订单提交")
        transaction.savepoint_rollback(tran_id)     #任何一个环节出错，则事务全部取消
    return JsonResponse(data)

@user_decorator.login
def pay(request):
    pass






