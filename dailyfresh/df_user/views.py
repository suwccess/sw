#coding=utf-8
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from models import *
from hashlib import sha1
from . import user_decorator
from df_goods.models import *
from df_order.models import *
#注册
def register(request):
    return render(request, 'df_user/register.html')
#注册逻辑处理
def register_handle(request):
    #接收用户输入
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')
    # upwd=post.get('allow')
    #判断两次密码
    if upwd!=upwd2:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    #创建对象
    user=UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功，转到登陆页
    return redirect('/user/login/')
#验证用户名是否存在
def register_exist(request):
    username=request.GET.get('uname')
    # count = UserInfo.objects.filter(uname=username).count()
    count = UserInfo.objects.filter(uname=username).count()
    # context = {'count': count}
    # return render(request, context)
    return JsonResponse({'count': count})

#登录
def login(request):
    uname=request.COOKIES.get('uname', '')
    context={'title': '用户登录', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'df_user/login.html', context)
#登录，接收请求信息
def login_handle(request):
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu', 0)
    users=UserInfo.objects.filter(uname=uname)
    # print uname

    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            if jizhu!=0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            # print uname
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name':0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)
#用户中心
@user_decorator.login
def user_info(request):
    username = request.session.get('user_name')
    # print username
    user = UserInfo.objects.filter(uname=username).first()
    goods_ids=request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    if goods_ids != '':
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    else:
        goods_list = []
    # explain = '无最近浏览'
    context = {'title': '用户中心', 'page_name': 1,
        'user_phone': user.uphone, 'user_address': user.uaddress,
        'user_name': username, 'goods_list': goods_list}
    # print context
    # context = explain
    return render(request, 'df_user/user_center_info.html', context)
#退出登录
def logout(request):
    request.session.flush() #清空当前用户的所有session
    return HttpResponseRedirect('/user/login')
#全部订单
@user_decorator.login
def order(request, index):
    user_id = request.session['user_id']
    orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by('-odate')
    paginator = Paginator(orders_list, 2)
    page = paginator.page(int(index))
    context = {
        'paginator': paginator,
        'page': page,
        # 'orders_list':orders_list,
        'title': "用户中心",
        'page_name': 1,
    }
    return render(request, 'df_user/user_center_order.html', context)

#收货地址
@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        user.ushou = request.POST.get('ushou')
        user.uaddress = request.POST.get('uaddress')
        user.uyoubian = request.POST.get('uyoubian')
        user.uphone = request.POST.get('uphone')
        user.save()
    context = {
        'page_name': 1,
        'title': '用户中心',
        'user': user,
    }
    return render(request, 'df_user/user_center_site.html', context)