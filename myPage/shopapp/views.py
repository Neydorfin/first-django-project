import random
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from shopapp.forms import OrderForm, ProductForm

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


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:products")
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        "form": form
    }
    return render(request, "shopapp/create-product.html", context=context)


def create_order(request: HttpRequest) -> HttpResponse:
    print(request.user)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:orders")
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        "form": form
    }
    return render(request, "shopapp/create-order.html", context=context)