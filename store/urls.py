from django.urls import path
from .views import *
app_name='store'

urlpatterns = [
    path('', index, name='home'),
    path('cart', cart, name='cart'),
    path('products/<id_product>', product, name='product'),
    path('error', error, name='error'),
    path('brands/<id_brand>', brand_filter, name='brand_filter'),
    path('add_product', add_product, name='add_product'),
    path('search', search, name='search'),
    path('del_product_cart', del_product_cart, name='del_product_cart'),
    path('changequantity_product', changequantity_product, name='changequantity_product'),
    path('bill', bill, name='bill'),
    path('order_by', order_by, name='order_by')
]
