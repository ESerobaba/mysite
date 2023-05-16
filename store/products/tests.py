from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()

    def _common_test(self, responce):
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.context['title'], 'Store - Каталог')
        self.assertTemplateUsed(responce, 'products/products.html')

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id)[:3]))
