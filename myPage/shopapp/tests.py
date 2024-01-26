import json
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from shopapp.models import Order, Product


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username="User", password="1111")
        view_order = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(view_order)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            user=self.user,
            delivery_address="not adress 123",
            promocode="ABOBA")

    def tearDown(self):
        self.client.logout()
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_detail", kwargs={"pk": self.order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["order"], self.order)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'shopapp/fixtures/order_fixture.json',
        'shopapp/fixtures/product_fixture.json', 
        'shopapp/fixtures/user_fixture.json',
        ]

    @classmethod
    def setUpClass(cls):
        super(OrdersExportTestCase, cls).setUpClass() # нужно было для loaddata из fixtures
        cls.user = User.objects.create(
            username="User", password="1111", is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def tearDown(self):
        self.client.logout()

    def test_order_export(self):
        response = self.client.get(reverse("shopapp:order_export"))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.select_related(
            "user").prefetch_related("products").all()

        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user.pk,
                "products": [product.pk for product in order.products.all()],
            }
            for order in orders
        ]
        response_data = response.json()
        orders = response_data["orders"]
        self.assertEqual(expected_data, orders)
