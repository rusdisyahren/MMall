import json
from django.shortcuts import render
from ecommerce.forms import LoginForm, ProductForm
from django.http import HttpResponseRedirect, HttpResponse
from models import models, Cart, CartItem, Category, Product, User, STATUS_CHOICES


# Create your views here.
def index(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list
    }
    return render(request, 'ecommerce/cart.html', context)


def cart(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list
    }
    return render(request, 'ecommerce/cart.html', context)


def detail(request, id):
    product_list = Product.objects.filter(pk=id)
    context = {
        'product_list': product_list[0]
    }
    return render(request, 'ecommerce/detail.html', context)


def signin(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            return HttpResponseRedirect('/store')
    else:
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, 'ecommerce/login_form.html', context)


def product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect('/store')
    else:
        product_form = ProductForm()

    context = {'product_form': product_form}
    return render(request, 'ecommerce/product_form.html', context)


def tmpCart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        productId = request.POST.get('id')
        cart[productId] = request.POST
        request.session['cart'] = cart
        response_data = {}
        response_data['status'] = True
        response_data['data'] = cart

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"status": True, "data": "this isn't happening"}),
            content_type="application/json"
        )


def cartItem(request):
    cartlist = request.session.get('cart')

    total_quantity = 0
    total_price = 0
    if cartlist is not None:
        for k, v in cartlist.items():
            total_quantity += int(v['qty'])
            total_price += int(v['qty']) * int(v['price'])

    context = {
        'cartlist': cartlist,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }
    return render(request, 'ecommerce/cartitem.html', context)


def clearCart(request):
    if request.session.get('has_session'):
        del request.session['cart']
    context = {}
    return render(request, 'ecommerce/cartitem.html', context)


def checkout(request):
    cartlist = request.session.get('cart')

    total_quantity = 0
    total_price = 0
    sub_total = 0
    user = User.objects.get(id=1)
    # insert to db
    cart = Cart()
    cart.customer = user
    cart.status = 'PD'
    cart.save()
    cartId = cart.id

    for k, v in cartlist.items():
        total_quantity += int(v['qty'])
        total_price += int(v['qty']) * int(v['price'])
        sub_total = int(v['qty']) * int(v['price'])
        cartdata = Cart.objects.get(id=cartId)
        productdata = Product.objects.get(id=v['id'])
        # insert to db
        saveCartItem = CartItem(product=productdata, cart=cartdata, price_perunit=v['price'], quantity=v['qty'],
                                total_price=sub_total)
        last_id = saveCartItem.save()
        id = saveCartItem.id

    del request.session['cart']
    context = {}
    return render(request, 'ecommerce/checkout.html', context)
