from itertools import product
import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from shopapp.models import Order, Product


def shop_index(request: HttpRequest) -> HttpResponse:
    context = {
        'list': [random.randint(x, 50) for x in range(9)],
        'name': 'blanditiis',
    }
    return render(request, 'shopapp/index.html', context=context)


def product_page(request: HttpRequest) -> HttpResponse:
    context = {
        "products" : Product.objects.all()
    }
    return render(request, 'shopapp/product-list.html', context=context)


def order_page(request: HttpRequest) -> HttpResponse:
    context = {
        "orders" : Order.objects.select_related("user").prefetch_related("products").all()
    }
    return render(request, 'shopapp/order-list.html', context=context)