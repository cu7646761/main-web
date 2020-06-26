from app.model.auth import UserModel
from tests.test_client import FlaskClientTestCase
from utils import Utils


class UserTestCase(FlaskClientTestCase):

    def test_find_by_email(self):
        user = UserModel()
        _user = user.find_by_email("phuongvuong1998@gmail.com")[0]
        self.assertTrue(_user.email, "phuongvuong1998@gmail.com")

    def test_turn_on_acc(self):
        user = UserModel()
        user.turn_on_acc("phuongvuong1998@gmail.com")
        _user = user.find_by_email("phuongvuong1998@gmail.com")[0]
        self.assertTrue(_user.active, 1)

    def test_delete(self):
        user = UserModel()
        _user = user.find_by_email("phuongvuong1998@gmail.com")[0]
        user.delete(_user.id)
        self.assertTrue(str(len(user.find_by_email("phuongvuong1998@gmail.com"))), "0")

    def test_update_link_image(self):
        user = UserModel()
        user.update_link_image("phuongvuong1998@gmail.com", "test")
        _user = user.find_by_email("phuongvuong1998@gmail.com")[0]
        self.assertTrue(_user.link_image, "test")

    def test_update_psw(self):
        user = UserModel()
        hashed_passwd = Utils.hash_password("123")
        password_old = user.find_by_email("phuongvuong1998@gmail.com")[0].password
        _user = user.update_psw("phuongvuong1998@gmail.com", str(hashed_passwd))
        password_new = user.find_by_email("phuongvuong1998@gmail.com")[0].password
        self.assertNotEqual(str(password_new), str(password_old))
