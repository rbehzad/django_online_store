from rest_framework import status
from accounts.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from model_mommy import mommy
from shop_managing.models import *
from shopping.models import *

# class RegisterTestCase(APITestCase):
#     def test_register(self):
#         data = {"username": "testcase@gmail.com", "password": "hellotest123",}
#         response = self.client.post('/api/v1/register/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class Test(APITestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.shoptype1 = mommy.make(ShopType, title='Dd')
        self.shoptype2 = mommy.make(ShopType, title='Ss')
        # self.tag1 = mommy.make(Tag, title='tag1')
        self.shop1 = mommy.make(Shop, user=self.user,
                   shop_type=self.shoptype1, title='didary')
        mommy.make(Shop, user=self.user,
                   shop_type=self.shoptype2, title='jj')
        mommy.make(Shop, user=self.user,
                   shop_type=self.shoptype2, title='hh')
        mommy.make(Cart, user=self.user,
                   shop=self.shop1, title='cart')
        self.product1 = mommy.make(Product, shop=self.shop1,
                   title='cart', description='dscrp', price=22, amount=3)
        # self.product1.tag.add(self.tag1)

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
        url = reverse('shopping_shop_product', args=['1'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # def test_cart(self):
    #     self.client.force_authenticate(self.user)
    #     url = reverse('shopping_create_cart', args=[1])
    #     resp = self.client.get(url)
    #     self.assertEqual(resp.status_code, 200)