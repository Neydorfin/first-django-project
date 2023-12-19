from django.urls import path
from .views import shop_index, product_page, order_page, upload_file

app_name = "shopapp"
urlpatterns = [
    path("", shop_index, name="index"),
    path("products", product_page, name="products"),
    path("orders", order_page, name="orders"),
    path("upload", upload_file, name="upload"),
]
