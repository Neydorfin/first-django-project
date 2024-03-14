import json
import logging

from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core import serializers
from django.core.cache import cache

from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from myauth.serializers import UserSerializer
from .models import Order, Product, ProductImage
from .forms import OrderForm, ProductForm
from .serializers import ProductSerializer, OrderSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

logger = logging.getLogger(__name__)


class UserOrdersListExport(View):
    def get(self, request: HttpRequest, user_id) -> JsonResponse:
        cache_key = f"order_export_user_{user_id}"
        order_export_data = cache.get(cache_key)
        if order_export_data is None:
            self.owner = get_object_or_404(User, pk=user_id)
            owner = UserSerializer(self.owner)
            queryset = Order.objects.select_related("user").prefetch_related("products").filter(
                user=self.owner).order_by("pk")
            orders = OrderSerializer(queryset, many=True)
            order_export_data = {
                "owner": owner.data,
                "orders": orders.data,
            }
            cache.set(cache_key, order_export_data, 300)
        return JsonResponse(order_export_data)


class UserOrdersListView(ListView):
    model = Order
    template_name = "shopapp/user_orders_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        self.owner = get_object_or_404(User, pk=self.kwargs["user_id"])
        queryset = Order.objects.select_related("user").prefetch_related("products").filter(user=self.owner)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = self.owner
        return context


class LatestProductsFeed(Feed):
    title = "Shop Products (Latest)"
    description = ""
    link = reverse_lazy("shopapp:product_list")

    def items(self):
        return (
            Product.objects.filter(archived=False).order_by("-created_at")[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:40]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("created_by").prefetch_related("images").all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["pk", "name", "price"]
    filterset_fields = ['name', 'description', 'price',
                        'discount', 'created_by_id', 'archived']


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related(
        "user").prefetch_related("products").all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    ordering_fields = ['created_at', 'user']


class ShopIndex(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'shopapp/shop_index.html')


class ProductListView(LoginRequiredMixin, ListView):
    queryset = Product.objects.select_related("created_by").prefetch_related("images").filter(archived=False)
    template_name = "shopapp/product_list.html"
    context_object_name = "products"


class ProductDetailView(LoginRequiredMixin, DetailView):
    queryset = Product.objects.prefetch_related("images").select_related("created_by")
    template_name = "shopapp/product_detail.html"
    context_object_name = "product"


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    model = Product
    template_name = "shopapp/product_create.html"
    form_class = ProductForm
    success_url = reverse_lazy("shopapp:product_list")

    # добавляем к продукту пользователя который создал его
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


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

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image
            )
        return response

    # проверяем разрешения пользователя
    def dispatch(self, request, *args, **kwargs):
        if not (request.user == self.get_object().created_by or request.user.is_staff or request.user.has_perm(
                "shopapp.change_product")):
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return super().dispatch(request, *args, **kwargs)


class ProductArchivedView(PermissionRequiredMixin, DeleteView):
    permission_required = "shopapp.change_product"
    queryset = Product.objects.prefetch_related("images")
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

    # проверяем разрешения пользователя
    def dispatch(self, request, *args, **kwargs):
        if not (request.user == self.get_object().created_by):
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return super().dispatch(request, *args, **kwargs)


class OrderListView(PermissionRequiredMixin, ListView):
    permission_required = "shopapp.view_order"
    model = Order
    template_name = "shopapp/order_list.html"
    context_object_name = "orders"


class OrderDetailView(DetailView):
    permission_required = "shopapp.view_order"
    model = Order
    template_name = "shopapp/order_detail.html"
    context_object_name = "order"


class OrderCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_order"
    model = Order
    template_name = "shopapp/order_create.html"
    form_class = OrderForm
    success_url = reverse_lazy("shopapp:order_list")


class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "shopapp.change_order"
    model = Order
    form_class = OrderForm
    template_name = "shopapp/order_update.html"

    def get_success_url(self) -> str:
        return reverse(
            "shopapp:order_detail",
            kwargs={"pk": self.object.pk}
        )


class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "shopapp.delete_order"
    model = Order
    template_name = "shopapp/order_delete.html"
    success_url = reverse_lazy("shopapp:order_list")


class OrderExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.select_related(
            "user").prefetch_related("products").all()
        response_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user.pk,
                "products": [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        return JsonResponse({"orders": response_data})

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return super().dispatch(request, *args, **kwargs)


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
