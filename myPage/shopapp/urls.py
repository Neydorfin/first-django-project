from django.urls import path
from .views import (
    ShopIndex, 
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductArchivedView,

    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,

    upload_file,)

app_name = "shopapp"
urlpatterns = [
    path("", ShopIndex.as_view(), name="index_shop"),
    path("products", ProductListView.as_view(), name="product_list"),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archived", ProductArchivedView.as_view(), name="product_archived"),


    path("orders", OrderListView.as_view(), name="order_list"),
    path("orders/create", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/update", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete", OrderDeleteView.as_view(), name="order_delete"),

    path("upload", upload_file, name="upload"),

]
