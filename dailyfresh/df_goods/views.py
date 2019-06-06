#coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator

from df_user.models import UserInfo
from .models import *
# @user_decorator.login
def index(request):
    #查询各个分类的最新，最热的四条数据
    typelist = TypeInfo.objects.all()
    #_set连表操作
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]      #按照上传顺序
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4] #按照点击量顺序
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    cart_num = 0

    context = {
        'title': '首页',
        'cart_num': cart_num,
        'guest_cart': 1,
        'type0': type0, 'type01': type01,
        'type1': type1, 'type11': type11,
        'type2': type2, 'type21': type21,
        'type3': type3, 'type31': type31,
        'type4': type4, 'type41': type41,
        'type5': type5, 'type51': type51,
    }

    return render(request, 'df_goods/index.html', context)

#商品列表
#商品分类id    pindex:商品页码    sort:商品分类显示方式
def goods_list(request, tid, pindex, sort):
    #根据主键查找当前的商品分类
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    #左侧最新商品推荐
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    #list中间栏商品显示
    goods_list = []
    cart_num, guest_cart =0, 0

    # try:
    #     user_id = request.session['user_id']
    # except:
    #     user_id = None
    # if user_id:
    #     guest_cart = 1
    #     cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    if sort=='1': #最新
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort=='2': #按照价格
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort=='3': #按照人气点击量
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    #创建Paginator一个分页对象
    paginator = Paginator(goods_list, 4)
    #返回page对象，包含商品信息
    page = paginator.page(int(pindex))
    context = {
        'title': '商品列表',
        'guest_cart': guest_cart,
        'cart_num': cart_num,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,  # 排序方式
        'news': news,
    }
    return render(request, 'df_goods/list.html', context)

def detail(request, gid):
    goods_id = gid
    goods = GoodsInfo.objects.get(pk=int(goods_id))
    goods.gclick = goods.gclick + 1 #商品点击量加1
    goods.save()
    # print(goods.gtype)

    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    content = {
        'title': goods.gtype,
        'guest_cart': 1,
        # 'cart_num': cart_count(request)
        'goods': goods,
        'news': news,
        'id': goods_id
    }
    response = render(request, 'df_goods/detail.html', content)

    #记录最近浏览的商品，在用户中心使用
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%s' % goods_id
    if goods_ids != '':     #判断是否有浏览记录，若有则继续判断
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id) >= 1: #如果商品已经被记录，则删除
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)
        if len(goods_ids1) >= 6: #如果超过6个，就删除最后一个
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1) #拼接为字符串
    else:
        goods_ids = goods_id    #如果没有浏览记录则直接加
    response.set_cookie('goods_ids', goods_ids)
    return response


