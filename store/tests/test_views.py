from importlib import import_module
from unittest import skip

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import shop

User = get_user_model()


@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_example(self):
        pass


class TestViewResponses(TestCase):
    def setUp(self):

        self.c = Client()
        User.objects.create(user_name='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        # response = self.c.get('/', HTTP_HOST='noaddress.com')
        # self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test product response status
        """
        response = self.c.get(reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test category response status
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Test homepage html
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = shop(request)
        html = response.content.decode('utf8')
        self.assertIn('<h2 class="h2 text-success border-bottom pb-3 border-light logo">Zay Shop</h2>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    # def test_view_function(self):
    #     request = self.factory.get('/item/django-beginners')
    #     response = shop(request)
    #     html = response.content.decode('utf8')
    #     self.assertIn('<h2 class="h2 text-success border-bottom pb-3 border-light logo">Zay Shop</h2>', html)
    #     self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
    #     self.assertEqual(response.status_code, 200)
