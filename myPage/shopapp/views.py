import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage

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


def upload_file(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST" and request.FILES.get('isFile'):
        file = request.FILES.get('isFile')
        context["name"] = file.name
        if file.size < 1_000_000:
            context["size"] = file.size
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
        else:
            context["size"] = "error"
    
    return render(request, "shopapp/upload-file.html", context=context)