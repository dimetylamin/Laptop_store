from django.contrib import admin

from .models import *

# Register your models here.
class Brand_display(admin.ModelAdmin):
    list_display=['name']
    search_fields=['name']
admin.site.register(Brand,Brand_display)

class Product_display(admin.ModelAdmin):
    list_display=['name','brand','price','newprice','quantity','active']
    search_fields=['name','brand__name']
    list_filter=['brand__name']
admin.site.register(Product, Product_display)

class Order_display(admin.ModelAdmin):
    list_display=['name','phone','email','created_at','order_status']
    search_fields=['name','phone','email']
admin.site.register(Order,Order_display)