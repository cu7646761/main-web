from app.model.store import StoreModel
from tests.test_client import FlaskClientTestCase


class StoreTestCase(FlaskClientTestCase):

    def test_find_by_name(self):
        store = StoreModel()
        _store = store.find_lst_by_name("Cửa hàng 1")[0]
        self.assertTrue(_store.name, "Cửa hàng 1")
