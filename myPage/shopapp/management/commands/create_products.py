from typing import Any
from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    """
    Create Product
    """

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Create Product")

        products = [
            ("milk", 100, 15),
            ("eggs", 300, 0),
            ("coffee", 450, 25),
            ("bread", 50, 6),
            ("butter", 120, 20),
            ("chesse", 300, 40),
            ("banana", 200, 10),
        ]
        for product_name, price, discount in products:
            product, created = Product.objects.get_or_create(
                name=product_name, price=price, discount=discount
            )
            if created:
                self.stdout.write(f"Product {product.name} created")

        self.stdout.write(self.style.SUCCESS("Product created"))
