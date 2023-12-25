from django.urls import path
from .views import create_product, shop_index, product_page, order_page, upload_file, create_order

app_name = "shopapp"
urlpatterns = [
    path("", shop_index, name="index"),
    path("products", product_page, name="products"),
    path("orders", order_page, name="orders"),
    path("upload", upload_file, name="upload"),
    path("products/create", create_product, name="create_product"),
    path("orders/create", create_order, name="create_order"),
]
