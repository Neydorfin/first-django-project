from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndex, 
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductArchivedView,
    LatestProductsFeed,

    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    OrderExportView,

    ProductViewSet,
    OrderViewSet,
    UserOrdersListView,
    upload_file,)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)


urlpatterns = [
    path("", ShopIndex.as_view(), name="index_shop"),
    path("api/", include(routers.urls)),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders_list"),

    path("products", ProductListView.as_view(), name="product_list"),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archived", ProductArchivedView.as_view(), name="product_archived"),
    path("products/latest/feed/", LatestProductsFeed(), name="product_feed"),

    path("orders", OrderListView.as_view(), name="order_list"),
    path("orders/create", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/update", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/export", OrderExportView.as_view(), name="order_export"),

    path("upload", upload_file, name="upload"),

]
