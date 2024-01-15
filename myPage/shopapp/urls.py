from django.urls import path
from .views import (
    ShopIndex, 
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductArchivedView,
    order_page, 
    upload_file, 
    create_order)

app_name = "shopapp"
urlpatterns = [
    path("", ShopIndex.as_view(), name="index_shop"),
    path("products", ProductListView.as_view(), name="product_list"),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archived", ProductArchivedView.as_view(), name="product_archived"),


    path("orders", order_page, name="order_list"),
    path("orders/create", create_order, name="order_create"),

    path("upload", upload_file, name="upload"),

]
