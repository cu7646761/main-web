import json
from app.model.store import StoreModel
from constants import LINK_IMG_AVATAR_DEF
from tests.test_client import FlaskClientTestCase


class StoreAdminViewsTestCase(FlaskClientTestCase):

    def test_store_admin_get(self):
        with self.client:
            response = self.client.get('/admin/store', follow_redirects=True)
            self.assertIn(bytes('cửa hàng', 'utf-8'), response.data)

    def test_store_admin_api_list(self):
        with self.client:
            store = StoreModel()
            _store = store.find_by_name("Cửa hàng 1")
            response = self.client.get('/admin/store/api/list?page=1', follow_redirects=True)
            self.assertIn(bytes(str(_store.id), 'utf-8'), response.data)

    def test_store_admin_get_add(self):
        with self.client:
            response = self.client.get('/admin/store/add', follow_redirects=True)
            self.assertIn(bytes("Thêm cửa hàng", 'utf-8'), response.data)

    def test_store_admin_post_add(self):
        with self.client:
            response = self.client.post('/admin/store/add',
                                        data=json.dumps(dict(
                                            name="Cửa hàng bán xe",
                                            description="<p>hihi</p>",
                                            image=LINK_IMG_AVATAR_DEF,
                                            categories=["Buffet"],
                                            address_detail="200 đường Hai Bà Trưng, Thành phố Quảng Ngãi, Tỉnh Quảng Ngãi",
                                            image_list=[])
                                        ), content_type='application/json', follow_redirects=True)
            self.assertTrue(response.status, 200)

    def test_store_admin_get_edit(self):
        with self.client:
            store = StoreModel()
            _store = store.find_by_name("Cửa hàng 1")
            response = self.client.get('/admin/store/edit/' + str(_store.id), follow_redirects=True)
            self.assertIn(bytes("Cửa hàng 1", 'utf-8'), response.data)

    def test_store_admin_post_edit(self):
        with self.client:
            store = StoreModel()
            _store = store.find_by_name("Cửa hàng 1")
            self.client.post('/admin/store/edit/' + str(_store.id),
                             data=json.dumps(dict(
                                 description="<p>hihi chinh r nha</p>",
                                 image=LINK_IMG_AVATAR_DEF,
                                 categories=["Sang Trọng"],
                                 address_detail="200 đường Hai Bà Trưng, Thành phố Quảng Ngãi, Tỉnh Quảng Ngãi",
                                 image_list=[])
                             ), content_type='application/json', follow_redirects=True)
            _store = store.find_by_name("Cửa hàng 1")
            self.assertTrue(_store.description, "<p>hihi chinh r nha</p>")
