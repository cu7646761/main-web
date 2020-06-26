from tests.test_client import FlaskClientTestCase
from utils import Utils


class AuthViewsTestCase(FlaskClientTestCase):

    def test_get_login(self):
        with self.client:
            response = self.client.get('/login', follow_redirects=True)
            self.assertIn(b'Login', response.data)

    def test_home(self):
        hashed_passwd = Utils.hash_password("huhu")
        with self.client:
            response = self.client.get('/', follow_redirects=True)
            self.assertIn(b'phuongvuong1998', response.data)

    def test_logout(self):
        with self.client:
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'Login', response.data)

    def test_get_signup(self):
        with self.client:
            response = self.client.get('/signup', follow_redirects=True)
            self.assertIn(b'Sign Up', response.data)

    def test_post_signup(self):
        with self.client:
            hashed_passwd = Utils.hash_password("123")
            response = self.client.post('/signup', data=dict(
                email="phuongvuong2@gmail.com",
                passwpord=hashed_passwd,
                password_confirm=hashed_passwd
            ), follow_redirects=True)
        self.assertIn(response.status, '200 OK')

    def test_about_us(self):
        with self.client:
            response = self.client.get('/about-us', follow_redirects=True)
            self.assertIn(b'Britcat', response.data)

    def test_contact_us(self):
        with self.client:
            response = self.client.get('/contact-us', follow_redirects=True)
            self.assertIn(b'Form', response.data)