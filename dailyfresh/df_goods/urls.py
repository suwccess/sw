from django.conf.urls import url
from . import views
app_name = 'df_goods'

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.goods_list, name='goods_list'),
    url(r'^(\d+)/$', views.detail, name='detail'),
]