from app import db
from app.models import Product, Category
from tests.test_client import FlaskClientTestCase


class ProductTestCase(FlaskClientTestCase):

    # Ensure product is inited
    def test_create(self):
        prod = Product(name="Do dien tu loai 1", category_id="1")
        self.assertTrue(prod.name, "Do dien tu loai 1")

    # Ensure list product is showed
    def test_list_cate(self):
        with self.client:
            response = self.client.get('/product', follow_redirects=True)
            self.assertIn(b'Product Table', response.data)

    # Ensure product is created
    def test_create_prod(self):
        with self.client:
            new_category = Category(name="Samsung")
            db.session.add(new_category)
            db.session.commit()
            response = self.client.post('/product/create', data=dict(
                product_name="Do choi loai 2",
                category_id="1"
            ), follow_redirects=True)
            self.assertIn(response.status, '200 OK')

    # Ensure product is created with product_name is empty
    def test_create_prod_1(self):
        with self.client:
            new_category = Category(name="Do dien tu cao cap")
            db.session.add(new_category)
            db.session.commit()
            response = self.client.post('/product/create', data=dict(
                product_name="",
                category_id="1"
            ), follow_redirects=True)
            self.assertIn(b"Your product is error", response.data)

    # Ensure api list product is working correctly
    def test_api_list_cate(self):
        with self.client:
            response = self.client.get('/product/api/list?page=1', follow_redirects=True)
            self.assertIn(response.status, '200 OK')

    # Ensure product is edit
    def test_edit_prod(self):
        with self.client:
            response = self.client.post('/product/edit', data=dict(
                product_id="1",
                product_name="Do choi loai 200",
                category_id="1"
            ), follow_redirects=True)
            self.assertIn(response.status, '200 OK')
