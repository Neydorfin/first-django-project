from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Product, Order


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        make_archived,
        make_unarchived,
    ]
    inlines = [OrderInline]
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
                "fields": ("archived","created_by",),
                "classes": ("collapse",),
            },
        ),
    )

    def description_short(self, obj: Product) -> str:
        if len(obj.description) > 48:
            return obj.description[:48] + "..."
        return obj.description


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = [
        make_done,
        make_undone,
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
