from io import TextIOWrapper
import json
from typing import Any
from django.contrib import admin
from django.core import serializers
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.urls import path

from .models import Order, Product, ProductImage
from .admin_mixins import ExportMixin
from .forms import JSONImportForm


@admin.action(description="Archive products")
def make_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def make_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(archived=False)


@admin.action(description="Mark order as done")
def make_done(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(done=True)


@admin.action(description="Unmark order as done")
def make_undone(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(done=False)


class OrderInline(admin.StackedInline):
    model = Product.orders.through


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportMixin):
    change_list_template = "shopapp/products_changelist.html"
    actions = [
        make_archived,
        make_unarchived,
        "export_as_csv",
        "export_as_json",
    ]
    inlines = [
        OrderInline,
        ProductImageInline,
    ]
    list_display = (
        "pk",
        "name",
        "description_short",
        "price",
        "discount",
        "archived",
    )
    list_display_links = (
        "pk",
        "name",
    )
    ordering = ("pk",)
    search_fields = (
        "pk",
        "name",
        "description",
    )
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "description"),
            },
        ),
        (
            "Price Options",
            {
                "fields": ("price", "discount"),
            },
        ),
        (
            "Extra Options",
            {
                "fields": ("archived", "created_by",),
                "classes": ("collapse",),
            },
        ),
    )

    def description_short(self, obj: Product) -> str:
        if len(obj.description) > 48:
            return obj.description[:48] + "..."
        return obj.description

    def import_json(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = JSONImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/json_form.html", context=context)

        form = JSONImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/json_form.html", context=context, status=400)

        json_file = TextIOWrapper(
            form.files["json_file"].file,
            encoding=request.encoding
        )
        data = json.load(json_file)
        products = [
            Product(**obj.get("fields")) for obj in data
        ]
        Product.objects.bulk_create(products)
        self.message_user(request, "Data from Json was successful imported!")
        return redirect(".")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-json",
                self.import_json,
                name="import_json",
            )
        ]
        return new_urls + urls


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportMixin):
    actions = [
        make_done,
        make_undone,
        "export_as_csv",
        "export_as_json",
    ]
    inlines = [ProductInline]
    list_display = (
        "pk",
        "user_name",
        "delivery_address",
        "promocode",
        "created_at",
        "done",
    )
    list_display_links = (
        "pk",
        "user_name",
        "delivery_address",
    )
    ordering = ("pk",)
    search_fields = (
        "pk",
        "user_name",
        "delivery_address",
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return Order.objects.select_related("user").prefetch_related("products")

    def user_name(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
