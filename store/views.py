import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import requests
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
# Create your views here.


def products():
    return Product.objects.filter(active=True)


def brands():
    return Brand.objects.filter(active=True)


def LOCATION(lv_region, code_region):
    url = f'https://provinces.open-api.vn/api/{lv_region}/{code_region}'
    location = requests.get(url).json()
    return location


def index(request):
    list_asus = []
    list_acer = []
    list_dell = []
    list_msi = []
    for item in products().filter(brand=1):
        list_asus.append({'id': item.id, 'name': item.name, 'image': item.image,
                          'price': item.price, 'newprice': item.newprice,
                          'sale': round(100-(item.newprice/item.price*100), 1)})

    for item in products().filter(brand=2):
        list_acer.append({'id': item.id, 'name': item.name, 'image': item.image,
                          'price': item.price, 'newprice': item.newprice,
                          'sale': round(100-(item.newprice/item.price*100), 1)})

    for item in products().filter(brand=3):
        list_dell.append({'id': item.id, 'name': item.name, 'image': item.image,
                          'price': item.price, 'newprice': item.newprice,
                          'sale': round(100-(item.newprice/item.price*100), 1)})

    for item in products().filter(brand=4):
        list_msi.append({'id': item.id, 'name': item.name, 'image': item.image,
                         'price': item.price, 'newprice': item.newprice,
                         'sale': round(100-(item.newprice/item.price*100), 1)})

    context = {
        'list_brand': brands(), 'list_asus': list_asus[:8], 'list_acer': list_acer[:8],
        'list_msi': list_msi[:8], 'list_dell': list_dell[:8],
        'cart_number': len(getSession_coverList(request, 'products_cart'))
    }
    return render(request, 'index.html', context)


def cart(request):
    total_price = 0
    list_product_cart = []
    list_product_cart_session = getSession_coverList(request, 'products_cart')
    for x in list_product_cart_session:
        product = products().get(id=x['id'])
        total_price += x['price']
        quantity = x['quantity']
        list_product_cart.append({'id': product.id, 'name': product.name, 'image': product.image,
                                  'price': product.newprice*quantity, 'quantity': quantity})
    context = {
        'list_brand': brands(), 'list_product_cart': list_product_cart,
        'total_price': total_price, 'cart_number': len(list_product_cart_session)
    }
    return render(request, 'cart.html', context)


def product(request, id_product):
    product = products().get(id=id_product)
    context = {
        'list_brand': brands(), 'product': product,
        'price': product.price, 'newprice': product.newprice,
        'cart_number': len(getSession_coverList(request, 'products_cart'))
    }
    return render(request, 'product.html', context)


@csrf_exempt
def brand_filter(request, id_brand):
    list_product = []
    for item in products().filter(brand=id_brand).order_by('newprice'):
        list_product.append({'id': item.id, 'name': item.name, 'image': item.image,
                             'price': item.price, 'newprice': item.newprice,
                             'sale': round(100-(item.newprice/item.price*100), 1)})
    context = {
        'list_brand': brands(), 'data': id_brand,
        'list_product': list_product, 'name_view': 'brand_filter',
        'cart_number': len(getSession_coverList(request, 'products_cart'))
    }
    return render(request, 'product_filter.html', context)


def error(request, error_content):
    context = {
        'list_brand': brands(),
        'cart_number': len(getSession_coverList(request, 'products_cart')),
        'error_content': error_content
    }
    return render(request, 'error.html', context)


def search(request):
    if request.method == 'POST':
        search_value = request.POST.get('search_input')
        if len(search_value) != 0:
            product = products().filter(Q(name__icontains=search_value) |
                                        Q(brand__name__icontains=search_value)).order_by('newprice')
            list = []
            for item in product:
                list.append({'id': item.id, 'name': item.name, 'image': item.image,
                             'price': item.price, 'newprice': item.newprice,
                             'sale': round(100-(item.newprice/item.price*100), 1)})
            context = {
                'list_brand': brands(), 'list_product': list,
                'data': search_value, 'name_view': 'search',
                'cart_number': len(getSession_coverList(request, 'products_cart'))
            }
            return render(request, 'product_filter.html', context)
    return error(request, 'Bạn chưa nhập bất cứ gì vào tìm kiếm')


def getSession_coverList(request, session_name):
    list = []
    if request.session.get(session_name) is None:
        request.session[session_name] = json.dumps(list)
    else:
        list = json.loads(request.session.get(session_name))
    return list


def del_session(request, session_name):
    if request.session.get(session_name) is not None:
        del request.session[session_name]
        return True
    else:
        return False


@csrf_exempt
def add_product(request):
    list = getSession_coverList(request, 'products_cart')
    id = request.POST.get('id_product')
    pd = products().get(id=id)
    temp = True
    for x in list:
        if x['id'] == id:
            if x['quantity'] < 10:
                x['quantity'] += 1
                x['price'] = pd.newprice*x['quantity']
                temp = False
                break
            else:
                return HttpResponse(json.dumps({'cart_number': len(list), 'max': True}))
    if temp:
        list.append({'id': id, 'price': pd.newprice, 'quantity': 1})
    request.session['products_cart'] = json.dumps(list)
    return HttpResponse(json.dumps({'cart_number': len(list), 'max': False}))


@ csrf_exempt
def del_product_cart(request):
    list = getSession_coverList(request, 'products_cart')
    id = request.POST.get('id')
    total_price = 0
    for item in list:
        if item['id'] != id:
            total_price += item['price']
    i = 0
    for i in range(len(list)):
        if list[i]['id'] == id:
            del list[i]
            break
        i += 1
    request.session['products_cart'] = json.dumps(list)
    return HttpResponse(json.dumps({'total_price': '{:,}'.format(total_price), 'cart_number': len(list)}))


@csrf_exempt
def changequantity_product(request):
    list = getSession_coverList(request, 'products_cart')
    total_price = 0
    id = request.POST.get('id')
    value = int(request.POST.get('value'))
    pd = products().get(id=id)
    if 0 < value <= 10:
        for x in list:
            if x['id'] == id:
                x['quantity'] = value
                x['price'] = value*pd.newprice
                break
        for item in list:
            print(item)
            total_price += item['price']
            print(total_price)
        request.session['products_cart'] = json.dumps(list)
        return HttpResponse(json.dumps({'total_price': total_price, 'price': pd.newprice*value, 'cart_number': len(list)}))
    else:
        return HttpResponse(0)


def bill(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        province = int(request.POST.get('province_select'))
        dicstrict = int(request.POST.get('dicstricts_select'))
        ward = int(request.POST.get('wards_select'))
        address = request.POST.get('address')

        payment_id = int(request.POST.get('payment_method'))
        payment = {
            0: 'Thanh toán bằng tiền mặt.',
            1: 'Thanh toán bằng thẻ ATM.',
            2: 'Thanh toán bằng Visa.',
            3: 'Thanh toán bằng Mastercard.',
        }
        list = getSession_coverList(request, 'products_cart')
        list_cart = []
        for item in list:
            pd = products().get(id=item['id'])
            list_cart.append({'name': pd.name, 'image': pd.image,
                             'price': item['price'], 'quantity': item['quantity']})
        total_price = 0
        for item in list:
            total_price += int(item['price'])
        if len(list_cart) > 0:
            if len(name) > 0 and len(phone) == 10 and len(email) >= 6 and province != 0 and dicstrict != 0 and ward != 0 and len(address) > 0 and payment[payment_id] is not None:
                province = LOCATION('p', province)['name']
                dicstrict = LOCATION('d', dicstrict)['name']
                ward = LOCATION('w', ward)['name']
                address = f'{province}, {dicstrict}, {ward}, {address}'
                check_order1 = Order.objects.filter(phone=phone).count()
                Order.objects.create(name=name, phone=phone, email=email, address=address, payment=payment_id,
                                     list_order=getSession_coverList(request, 'products_cart'))
                check_order2 = Order.objects.filter(phone=phone).count()
                order_status = False
                if check_order2 > check_order1:
                    order_status = True
                    for item in list:
                        pd = products().get(id=item['id'])
                        pd.quantity = pd.quantity-item['quantity']
                        pd.save()
                    del request.session['products_cart']
                order = Order.objects.filter(phone=phone).last()
                context = {
                    'name': name, 'phone': phone, 'email': email, 'address': address, 'price': total_price,
                    'payment': payment[payment_id], 'list_cart': list_cart, 'order_status': order_status,
                    'cart_number': 0, 'order_day': order.created_at, 'list_brand': brands()
                }
                return render(request, 'bill.html', context)
            else:
                return error(request, 'Thông tin mua hàng chưa đầy đủ')
        else:
            return error(request, 'Chưa có sản phẩm trong giỏ hàng')


@csrf_exempt
def order_by(request):
    key = int(request.POST.get('key'))
    data = request.POST.get('data')
    view_name = request.POST.get('view_name')
    id_price_range = int(request.POST.get('price_range'))
    list_price_range = [
        {'start_price': 0, 'end_price': 999999999999},
        {'start_price': 0, 'end_price': 15000000},
        {'start_price': 15000000, 'end_price': 30000000},
        {'start_price': 30000000, 'end_price': 50000000},
        {'start_price': 50000000, 'end_price': 80000000},
        {'start_price': 80000000, 'end_price': 100000000},
        {'start_price': 100000000, 'end_price': 999999999999},
    ]
    list = []
    if view_name == 'search':
        if key == 0:
            for item in products().filter(Q(name__icontains=data) | Q(brand__name__icontains=data)).filter(newprice__range=(list_price_range[id_price_range]['start_price'],
                                                                                                                            list_price_range[id_price_range]['end_price'])).order_by('newprice'):
                list.append({'id': item.id, 'name': item.name, 'image': f'/{item.image}',
                             'price': '{:,}'.format(item.price), 'newprice': '{:,}'.format(item.newprice),
                             'sale': round(100-(item.newprice/item.price*100), 1)})
        else:
            for item in products().filter(Q(name__icontains=data) | Q(brand__name__icontains=data)).filter(newprice__range=(list_price_range[id_price_range]['start_price'],
                                                                                                                            list_price_range[id_price_range]['end_price'])).order_by('-newprice'):
                list.append({'id': item.id, 'name': item.name, 'image': f'/{item.image}',
                             'price': '{:,}'.format(item.price), 'newprice': '{:,}'.format(item.newprice),
                             'sale': round(100-(item.newprice/item.price*100), 1)})
    if view_name == 'brand_filter':
        if key == 0:
            for item in products().filter(brand=data).filter(newprice__range=(list_price_range[id_price_range]['start_price'],
                                                                              list_price_range[id_price_range]['end_price'])).order_by('newprice'):
                list.append({'id': item.id, 'name': item.name, 'image': f'/{item.image}',
                             'price': '{:,}'.format(item.price), 'newprice': '{:,}'.format(item.newprice),
                             'sale': round(100-(item.newprice/item.price*100), 1)})
        else:
            for item in products().filter(brand=data).filter(newprice__range=(list_price_range[id_price_range]['start_price'],
                                                                              list_price_range[id_price_range]['end_price'])).order_by('-newprice'):
                list.append({'id': item.id, 'name': item.name, 'image': f'/{item.image}',
                             'price': '{:,}'.format(item.price), 'newprice': '{:,}'.format(item.newprice),
                             'sale': round(100-(item.newprice/item.price*100), 1)})
                             
    return HttpResponse(json.dumps(list))
