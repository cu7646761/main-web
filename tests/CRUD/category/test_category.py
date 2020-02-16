from app import db
from app.models import Category, Brand
from tests.test_client import FlaskClientTestCase


class CategoryTestCase(FlaskClientTestCase):

    # Ensure category is inited
    def test_create(self):
        cate = Category(name="Do dien tu", brand_id="1")
        self.assertTrue(cate.name, "Do dien tu")

    # Ensure list category is showed
    def test_list_cate(self):
        with self.client:
            response = self.client.get('/category', follow_redirects=True)
            self.assertIn(b'Category Table', response.data)

    # Ensure category is created
    def test_create_cate(self):
        with self.client:
            new_brand = Brand(name="Samsung")
            db.session.add(new_brand)
            db.session.commit()
            response = self.client.post('/category/create', data=dict(
                category_name="Do choi",
                brand_id="1"
            ), follow_redirects=True)
            self.assertIn(response.status, '200 OK')

    # Ensure category is created with category_name is empty
    def test_create_cate_1(self):
        with self.client:
            new_brand = Brand(name="Samsung")
            db.session.add(new_brand)
            db.session.commit()
            response = self.client.post('/category/create', data=dict(
                category_name="",
                brand_id="1"
            ), follow_redirects=True)
            self.assertIn(b"Your category is error", response.data)

    # Ensure api list category is working correctly
    def test_api_list_cate(self):
        with self.client:
            response = self.client.get('/category/api/list?page=1', follow_redirects=True)
            self.assertIn(response.status, '200 OK')

    # Ensure category is edit
    def test_edit_cate(self):
        with self.client:
            response = self.client.post('/category/edit', data=dict(
                category_id="1",
                category_name="Do choi loai 1",
                brand_id="1"
            ), follow_redirects=True)
            self.assertIn(response.status, '200 OK')
