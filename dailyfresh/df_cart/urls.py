from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.cart, name='cart'),
    url(r'^add(\d+)_(\d+)', views.add, name='add'),
    url(r'^edit(\d+)_(\d+)', views.edit, name='edit'),
    url(r'^delete(\d+)', views.delete, name='delete'),
]