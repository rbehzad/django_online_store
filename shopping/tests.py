from rest_framework import status
from accounts.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from model_mommy import mommy
from shop_managing.models import *
from shopping.models import *

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "email": "test2@example.com",
            "phone_number": "09333456789",
            "first_name": "Dave",
            "last_name": "Elder",
            "password": "some_str_passwd",
            "password2": "some_str_passwd",
        }
        return super().setUp()

    def test_registration(self):
        response = self.client.post("/accounts/register/", self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        self.client.post("/accounts/register/", self.data)
        response = self.client.post(
        "/accounts/login/", {"email": self.data["email"], "password": self.data["password"]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class Test(APITestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.user2 = mommy.make(User)
        self.shoptype1 = mommy.make(ShopType, title='Dd')
        self.shoptype2 = mommy.make(ShopType, title='Ss')
        self.tag1 = mommy.make(Tag, title='tag1')
        self.shop1 = mommy.make(Shop, user=self.user,
                   shop_type=self.shoptype1, title='didary')
        mommy.make(Shop, user=self.user,
                   shop_type=self.shoptype2, title='jj')
        mommy.make(Shop, user=self.user,
                   shop_type=self.shoptype2, title='hh')
        mommy.make(Cart, user=self.user,
                   shop=self.shop1, title='cart')
        self.product1 = Product.objects.create(shop=self.shop1,
                   title='cart', description='create cart test', price=22, amount=3)
        # self.product1 = mommy.make(Product, shop=self.shop1,
        #            title='cart', description='create cart test', price=22, amount=3)
        self.product1.tag.add(self.tag1)
        self.product1.save()
        mommy.make(Cart, user=self.user,
                   shop=self.shop1, title='cart', status='Paid')
        self.cart = mommy.make(Cart, user=self.user,
                   shop=self.shop1, title='cart', status='Pending')


    def test_shoptype_list(self):
        self.client.force_authenticate(self.user)
        url = reverse('shopping_shoptypes')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_list(self):
        self.client.force_authenticate(self.user)
        url = reverse('shopping_shops')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_products(self):
        self.client.force_authenticate(self.user)
        url = reverse('shopping_shop_product', kwargs={'pk': self.shop1.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_create_cart(self):
        self.client.force_authenticate(self.user2)
        url = reverse('shopping_create_cart', kwargs={'pk': self.product1.id})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 201)
        

    def test_paid(self):
        self.client.force_authenticate(self.user)
        url = reverse('shopping_paid')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_pending(self):
        self.client.force_authenticate(self.user)
        url = reverse('shopping_pending')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # def test_pay(self):
    #     self.client.force_authenticate(self.user)
    #     url = reverse('shopping_pay', kwargs={'cart_pk': self.cart})
    #     resp = self.client.put(url)
    #     self.assertEqual(resp.status_code, 200)