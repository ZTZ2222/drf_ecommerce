from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse

from orders.models import Order, OrderItem
from products.models import Category, Product
from users.models import User


class OrderListAPIViewTestCase(TransactionTestCase):
    product = {
        "name": "Test Product 1",
        "description": "Test Description",
        "base_price": 100,
        "sale_price": 80,
        "quantity": 10,
        "slug": "test-product-1",
    }

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("orders:order-list")
        self.email = "john"
        self.password = "you_know_nothing"
        self.user = User.objects.create_superuser(self.email, self.password)
        self.token = AccessToken.for_user(self.user)
        self.api_authentication()
        self.product = Product.objects.create(**self.product)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    # def test_create_order(self):
    #     data = {
    #         "order_items": [{"quantity": 1, "product": self.product.id}],
    #         "shipping_address": 1,
    #         "billing_address": 1,
    #     }
    #     response = self.client.post(self.url, data, format="json")
    #     self.assertEqual(201, response.status_code)
    #     self.assertEqual(1, Order.objects.all().count())

    # def test_get_order(self):
    #     order = Order.objects.create(buyer=self.user, status="P", total_cost=80)
    #     response = self.client.get(reverse("orders:order-detail", args=[order.id]))
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(order.id, response.data["id"])

    # def test_patch_order(self):
    #     order = Order.objects.create(user=self.user)
    #     data = {"order_items": [{"quantity": 1, "product": self.product.id}]}
    #     response = self.client.patch(
    #         reverse("orders:order-detail", args=[order.id]), data, format="json"
    #     )
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(1, OrderItem.objects.all().count())

    # def test_delete_order(self):
    #     order = Order.objects.create(user=self.user)
    #     response = self.client.delete(reverse("orders:order-detail", args=[order.id]))
    #     self.assertEqual(204, response.status_code)
    #     self.assertEqual(0, Order.objects.all().count())

    # def test_list_orders(self):
    #     order = Order.objects.create(user=self.user)
    #     response = self.client.get(self.url)
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(1, len(response.data))
    #     self.assertEqual(order.id, response.data[0]["id"])
