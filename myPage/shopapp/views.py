from typing import Any
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from shopapp.forms import OrderForm, ProductForm

from shopapp.models import Order, Product


class ShopIndex(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'shopapp/index.html')


class ProductListView(ListView):
    queryset = Product.objects.filter(archived=False)
    template_name = "shopapp/product_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "shopapp/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    template_name = "shopapp/product_create.html"
    form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "shopapp/product_update.html"
    form_class = ProductForm
    context_object_name = "product"

    def get_success_url(self) -> str:
        return reverse(
            "shopapp:product_detail",
            kwargs={"pk": self.object.pk}
        )


class ProductArchivedView(DeleteView):
    model = Product
    template_name = "shopapp/product_archived.html"
    context_object_name = "product"

    def get_success_url(self) -> str:
        return reverse(
            "shopapp:product_detail",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        success_url = self.get_success_url()
        if self.object.archived:
            self.object.archived = False
        else:
            self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    model = Order
    template_name = "shopapp/order_list.html"
    context_object_name = "orders"


class OrderDetailView(DetailView):
    model = Order
    template_name = "shopapp/order_detail.html"
    context_object_name = "order"


class OrderCreateView(CreateView):
    model = Order
    template_name = "shopapp/order_create.html"
    form_class = OrderForm
    success_url = reverse_lazy("shopapp:order_list")


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "shopapp/order_update.html"

    def get_success_url(self) -> str:
        return reverse(
            "shopapp:order_detail",
            kwargs={"pk": self.object.pk}
        )


class OrderDeleteView(DeleteView):
    model = Order
    template_name = "shopapp/order_delete.html"
    success_url = reverse_lazy("shopapp:order_list")


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

    return render(request, "shopapp/upload_file.html", context=context)
