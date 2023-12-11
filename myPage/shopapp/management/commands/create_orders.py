from typing import Any
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Order, Product


class Command(BaseCommand):
    """
    Create Order
    """

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Create Order")
        user = User.objects.get(username="admin")
        order, created = Order.objects.get_or_create(
            delicery_adress="St.Stefan 25", promocode="1984ADMIN", user=user
        )
        if created:
            self.stdout.write(f"Order {order} created")

        products = Product.objects.all()

        for product in products:
            if product.price < 200:
                order.products.add(product)
                self.stdout.write(f"{product.name} added to order {order}")

        order.save()

        self.stdout.write(self.style.SUCCESS(f"Order {order.id} successefully added"))
