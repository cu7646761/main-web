
from app.models import Brand
from tests.test_client import FlaskClientTestCase
from app import db

import unittest


class BrandTestCase(FlaskClientTestCase):

    # Ensure brand is inited
    def test_create(self):
        brand = Brand(name="Samsung")
        self.assertTrue(brand.name, "Samsung")

    # Ensure list brand is showed
    def test_list_cate(self):
        with self.client:
            response = self.client.get('/brand', follow_redirects=True)
            self.assertIn(b'Brand Table', response.data)

    # Ensure brand is created
    def test_create_brand(self):
        with self.client:
            response = self.client.post('/brand/create', data=dict(
                brandName="Honda"
            ), follow_redirects=True)
            self.assertIn(response.status, '200 OK')

    # Ensure brand is created with brand_name is empty
    def test_create_brand_1(self):
        with self.client:
            response = self.client.post('/brand/create', data=dict(
                brandName=""
            ), follow_redirects=True)
            self.assertIn(b"Your brand is error", response.data)

    # Ensure api list brand is working correctly
    def test_api_list_cate(self):
        with self.client:
            response = self.client.get(
                '/brand/api/list?page=1', follow_redirects=True)
            self.assertIn(response.status, '200 OK')

    # Ensure brand is edit
    def test_edit_brand(self):
        with self.client:
            response = self.client.post('/brand/edit', data=dict(
                brand_id="1",
                brand_name="LG"
            ), follow_redirects=True)
            self.assertIn(response.status, '200 OK')
