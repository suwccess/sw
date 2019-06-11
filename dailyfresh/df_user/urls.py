from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, 'register_handle'),
    url(r'^login/', views.login, name='login'),
    url(r'^login_handle/', views.login_handle, name='login_handle'),
    url(r'^register_exist/', views.register_exist, name='register_exist'),
    url(r'^info/', views.user_info, name='user_info'),
    url(r'^site/', views.site, name='site'),
    url(r'^order/(\d+)', views.order, name='order'),
    url(r'^logout/', views.logout, name='logout')
]