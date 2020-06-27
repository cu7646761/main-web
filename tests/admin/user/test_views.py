from app.model.auth import UserModel
from tests.test_client import FlaskClientTestCase


class UserAdminViewsTestCase(FlaskClientTestCase):

    def test_get_admin(self):
        with self.client:
            response = self.client.get('/admin', follow_redirects=True)
            self.assertIn(bytes('Tổng quan', 'utf-8'), response.data)

    def test_get_user(self):
        with self.client:
            response = self.client.get('/admin/user-management', follow_redirects=True)
            self.assertIn(bytes('phuongvuong1998', 'utf-8'), response.data)

    def test_getStatus(self):
        with self.client:
            user = UserModel()
            _user = user.find_by_email("phuongvuong1@gmail.com")[0]
            url = "/admin/user-management/set-status/" + str(_user.id) + "/0"
            _user = user.find_by_email("phuongvuong1@gmail.com")[0]
            self.client.get(url, follow_redirects=True)
            self.assertTrue(_user.active, 1)

    def test_list_user_api(self):
        with self.client:
            response = self.client.get("/admin/user-management/api/list?page=1", follow_redirects=True)
            self.assertIn(bytes('phuongvuong1', 'utf-8'), response.data)

    def test_delete_user(self):
        with self.client:
            user = UserModel()
            _user = user.find_by_email("phuongvuong1@gmail.com")[0]
            url = "/admin/user-management/delete/" + str(_user.id)
            self.client.get(url, follow_redirects=True)
            _user = user.find_by_email("phuongvuong1@gmail.com")
            self.assertTrue(str(len(_user)), "0")

    def test_get_district_by_city(self):
        with self.client:
            response = self.client.get("/profile/district?city_id=79", follow_redirects=True)
            self.assertIn(bytes("quan_1", 'utf-8'), response.data)

    def test_get_edit_user(self):
        with self.client:
            user = UserModel()
            _user = user.find_by_email("phuongvuong1@gmail.com")[0]
            url = "/admin/user-management/edit/" + str(_user.id)
            response = self.client.get(url, follow_redirects=True)
            self.assertIn(bytes("phuongvuong1@gmail.com", 'utf-8'), response.data)

    def test_post_edit_user(self):
        with self.client:
            user = UserModel()
            _user = user.find_by_email("phuongvuong1@gmail.com")[0]
            url = "/admin/user-management/edit/" + str(_user.id) + "/update-basic"
            response = self.client.post(url, data=dict(
                birthday="15/08/1998",
                gender=0,
                result_address="200 đường Hai Bà Trưng, Thành phố Quảng Ngãi, Tỉnh Quảng Ngãi",
                love_cate=['Sang Trọng', 'Buffet']
            ), follow_redirects=True)
            self.assertIn(bytes("thành công", 'utf-8'), response.data)
