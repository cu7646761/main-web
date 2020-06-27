from app.model.store import StoreModel
from tests.test_client import FlaskClientTestCase


class StoreViewsTestCase(FlaskClientTestCase):

    def test_store_get(self):
        with self.client:
            response = self.client.get('/stores', follow_redirects=True)
            self.assertIn(bytes('LỌC KẾT QUẢ', 'utf-8'), response.data)

    def test_store_detail_get(self):
        with self.client:
            store = StoreModel()
            _store = store.find_by_name('Cửa hàng 1')
            response = self.client.get('/stores/' + str(_store.id), follow_redirects=True)
            self.assertIn(bytes('Cửa hàng 1', 'utf-8'), response.data)

    def test_store_detail_post_cmt(self):
        with self.client:
            store = StoreModel()
            _store = store.find_by_name('Cửa hàng 1')
            response = self.client.post('/stores/' + str(_store.id), data=dict(
                comment="Ngon lắm đấy nha hihi!",
                star="5"
            ), follow_redirects=True)
            self.assertIn(bytes('Ngon lắm đấy nha hihi!', 'utf-8'), response.data)

    def test_store_get_api(self):
        with self.client:
            store = StoreModel()
            _store = store.find_by_name('Cửa hàng 1')
            response = self.client.post('/store', data=dict(
                name="Cửa hàng 1"
            ), follow_redirects=True)
            self.assertIn(bytes(str(_store.id), 'utf-8'), response.data)