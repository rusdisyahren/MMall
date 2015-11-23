from django.shortcuts import render
from ecommerce.forms import LoginForm,ProductForm
from django.http import HttpResponseRedirect
import models

# Create your views here.
def index(request):
    product_list = models.Product.objects.all()
    context = {
        'product_list' :product_list
    }
    return render(request, 'ecommerce/index.html', context)

def cart(request):
    product_list = models.Product.objects.all()
    context = {
        'product_list' :product_list
    }
    return render(request, 'ecommerce/cart.html', context)

def detail(request,id):
    product_list = models.Product.objects.filter(pk=id)
    context = {
        'product_list' :product_list[0]
    }
    return render(request, 'ecommerce/detail.html',context)

def signin(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            return HttpResponseRedirect('/store')
    else:
        login_form = LoginForm()

    context = {'login_form':login_form}
    return render(request, 'ecommerce/login_form.html', context)


def product(request):

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect('/store')
    else:
        product_form = ProductForm()

    context = {'product_form':product_form}
    return render(request, 'ecommerce/product_form.html', context)



