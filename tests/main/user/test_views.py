from tests.test_client import FlaskClientTestCase


class ProfileViewsTestCase(FlaskClientTestCase):

    def test_get_profile(self):
        with self.client:
            response = self.client.get('/profile', follow_redirects=True)
        self.assertIn(bytes(str("Thông tin cá nhân"), 'utf-8'), response.data)

    def test_post_update_pass(self):
        with self.client:
            response = self.client.post('/profile/update_pass', data=dict(
                old_password="huhu",
                new_password_1="123",
                new_password_2="123"
            ), follow_redirects=True)
        self.assertIn(response.status, '200 OK')

    def test_post_update_basic(self):
        with self.client:
            response = self.client.post('/profile/update-basic',
                                        data=dict(
                                            birthday="15/08/1998",
                                            gender="0",
                                            result_address="18 Trần Ngọc Diện, P. Thảo Điền, Quận 2",
                                            love_cate="Sang Trọng"
                                        ), follow_redirects=True)
        self.assertIn(response.status, '200 OK')

    def test_post_update_basic_1(self):
        with self.client:
            response = self.client.post('/profile/update-basic',
                                        data=dict(
                                            birthday="24/06/1998",
                                            gender="0",
                                            result_address="18 Trần Ngọc Diện, P. Thảo Điền, Quận 2"
                                        ), follow_redirects=True)
        self.assertIn(response.status, '200 OK')

    def test_post_update_basic_2(self):
        with self.client:
            response = self.client.post('/profile/update-basic',
                                        data=dict(
                                            birthday="24/06/1998",
                                            result_address="18 Trần Ngọc Diện, P. Thảo Điền, Quận 2"
                                        ), follow_redirects=True)
        self.assertIn(response.status, '200 OK')
