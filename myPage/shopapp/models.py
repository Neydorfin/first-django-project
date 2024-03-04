from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy


class Product(models.Model):
    class Meta:
        verbose_name = gettext_lazy("Product")
        verbose_name_plural = gettext_lazy("Products")

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1)

    def __str__(self) -> str:
        return f"{self.pk}. {self.name}"


def product_images_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


def get_absolute_url(self):
    return reverse("shopapp:product_detail", kwargs={"pk": self.pk})


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_path)
    description = models.CharField(max_length=150, null=True, blank=True)


class Order(models.Model):
    class Meta:
        verbose_name = gettext_lazy("Order")
        verbose_name_plural = gettext_lazy("Orders")

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    delivery_address = models.TextField(blank=True)
    promocode = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name="orders")
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.pk}. {self.user}: {self.delivery_address}"
