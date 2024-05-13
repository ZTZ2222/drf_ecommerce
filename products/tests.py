from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from products.models import Category, Product
from users.models import User


class ProductCreateAPIViewTestCase(APITestCase):
    url = reverse("products:product-list")

    def setUp(self):
        self.email = "john"
        self.password = "you_know_nothing"
        self.user = User.objects.create_superuser(self.email, self.password)
        self.token = AccessToken.for_user(self.user)
        self.api_authentication()
        Category.objects.create(name="Test Category", slug="test-category", id=1)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_create_product(self):
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "base_price": 100,
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Product.objects.all().count())

    def test_create_product_with_same_slug(self):
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "base_price": 100,
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product",
        }
        self.client.post(self.url, data, format="json")
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, Product.objects.all().count())

    def test_create_product_without_name(self):
        data = {
            "description": "Test Description",
            "base_price": 100,
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Product.objects.all().count())

    def test_create_product_without_description(self):
        data = {
            "name": "Test Product",
            "base_price": 100,
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Product.objects.all().count())

    def test_create_product_without_base_price(self):
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Product.objects.all().count())

    def test_create_product_with_negative_base_price(self):
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "base_price": -100,
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Product.objects.all().count())

    def test_create_product_with_zero_base_price(self):
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "base_price": 0,
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Product.objects.all().count())


class ProductListAPIViewTestCase(APITestCase):
    url = reverse("products:product-list")

    def setUp(self):
        self.email = "john"
        self.password = "you_know_nothing"
        self.user = User.objects.create_superuser(self.email, self.password)
        self.token = AccessToken.for_user(self.user)
        self.api_authentication()
        Category.objects.create(name="Test Category", slug="test-category", id=1)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

    def test_list_products_with_one_item(self):
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "base_price": 100,
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product",
        }
        self.client.post(self.url, data, format="json")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(Product.objects.all()))

    def test_list_products_with_two_items(self):
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "base_price": 100,
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product",
        }
        data2 = {
            "name": "Test Product 2",
            "description": "Test Description",
            "base_price": 100,
            "sale_price": 80,
            "quantity": 10,
            "category": 1,
            "slug": "test-product-2",
        }
        self.client.post(self.url, data, format="json")
        self.client.post(self.url, data2, format="json")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(Product.objects.all()))

    def test_list_products_with_more_than_20_items(self):
        for i in range(25):
            self.client.post(
                self.url,
                {
                    "name": f"Test Product {i}",
                    "description": "Test Description",
                    "base_price": 100,
                    "sale_price": 80,
                    "quantity": 10,
                    "category": 1,
                    "slug": f"test-product-{i}",
                },
                format="json",
            )
        response = self.client.get(self.url + "?limit=20")
        self.assertEqual(200, response.status_code)
        self.assertEqual(25, len(Product.objects.all()))

    def test_list_products_with_pagination(self):
        for i in range(25):
            self.client.post(
                self.url,
                {
                    "name": f"Test Product {i}",
                    "description": "Test Description",
                    "base_price": 100,
                    "sale_price": 80,
                    "quantity": 10,
                    "category": 1,
                    "slug": f"test-product-{i}",
                },
                format="json",
            )
        response = self.client.get(self.url + "?limit=5")
        self.assertEqual(200, response.status_code)
        self.assertEqual(25, len(Product.objects.all()))

    def test_list_products_with_invalid_pagination(self):
        for i in range(25):
            self.client.post(
                self.url,
                {
                    "name": f"Test Product {i}",
                    "description": "Test Description",
                    "base_price": 100,
                    "sale_price": 80,
                    "quantity": 10,
                    "category": 1,
                    "slug": f"test-product-{i}",
                },
                format="json",
            )
        response = self.client.get(self.url + "?limit=5&offset=25")
        self.assertEqual(200, response.status_code)
        self.assertEqual(25, len(Product.objects.all()))


class ProductListAPIViewTestCase(TransactionTestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("products:product-list")
        self.email = "john"
        self.password = "you_know_nothing"
        self.user = User.objects.create_superuser(self.email, self.password)
        self.token = AccessToken.for_user(self.user)
        self.api_authentication()
        Category.objects.create(name="Test Category", slug="test-category", id=1)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_list_products_with_offset(self):
        for i in range(25):
            self.client.post(
                self.url,
                {
                    "name": f"Test Product {i}",
                    "description": "Test Description",
                    "base_price": 100,
                    "sale_price": 80,
                    "quantity": 10,
                    "category": 1,
                    "slug": f"test-product-{i}",
                },
                format="json",
            )
        response = self.client.get(self.url + "?limit=5&offset=5")
        self.assertEqual(200, response.status_code)
        self.assertEqual(25, len(Product.objects.all()))
        self.assertEqual(5, len(response.data["results"]))
        self.assertEqual(response.data["results"][0]["name"], "Test Product 19")

    def test_list_products_with_invalid_offset(self):
        for i in range(25):
            self.client.post(
                self.url,
                {
                    "name": f"Test Product {i}",
                    "description": "Test Description",
                    "base_price": 100,
                    "sale_price": 80,
                    "quantity": 10,
                    "category": 1,
                    "slug": f"test-product-{i}",
                },
                format="json",
            )
        response = self.client.get(self.url + "?limit=5&offset=25")
        self.assertEqual(200, response.status_code)
        self.assertEqual(25, len(Product.objects.all()))
        self.assertEqual(0, len(response.data["results"]))

    def test_list_products_with_offset_greater_than_number_of_items(self):
        for i in range(25):
            self.client.post(
                self.url,
                {
                    "name": f"Test Product {i}",
                    "description": "Test Description",
                    "base_price": 100,
                    "sale_price": 80,
                    "quantity": 10,
                    "category": 1,
                    "slug": f"test-product-{i}",
                },
                format="json",
            )
        response = self.client.get(self.url + "?limit=5&offset=30")
        self.assertEqual(200, response.status_code)
        self.assertEqual(25, len(Product.objects.all()))
        self.assertEqual(0, len(response.data["results"]))
