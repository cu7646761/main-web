import unittest
from mongoengine import disconnect
from app import create_app


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        disconnect()
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
