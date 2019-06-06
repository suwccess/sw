from django.contrib import admin
from models import *

class GoodsInfoInline(admin.StackedInline):
    model = GoodsInfo
    extra = 2

class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']
    list_per_page = 10
    search_fields = ['ttitle']
    list_display_links = ['ttitle']
    inlines = [GoodsInfoInline]
# class GoodsInfoAdmin(admin.ModelAdmin):
#     list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gkucun', 'gjianjie', 'gpic', 'gtype']
#     list_per_page = 20
#     list_editable = ['gkucun',]
#     # readonly_fields = ['gclick']
#     search_fields = ['gtitle', 'gcontent', 'gjianjie']
#     list_display_links = ['gtitle']

admin.site.register(TypeInfo, TypeInfoAdmin)
# admin.site.register(GoodsInfo, GoodsInfoAdmin)



