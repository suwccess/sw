#coding=utf-8
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
from models import *
from hashlib import sha1
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

def user_info(request):
    username = request.session.get('user_name')
    # print username
    user = UserInfo.objects.filter(uname=username).first()
    explain = '无最近浏览'
    context = {'title': '用户中心', 'page_name': 1,
        'user_phone': user.uphone, 'user_address': user.uaddress,
        'user_name': username, 'explain': explain}
    # print context
    # context = explain
    return render(request, 'df_user/user_center_info.html', context)
#退出登录
def logout(request):
    request.session.flush() #清空当前用户的所有session
    return HttpResponseRedirect('/user/login')