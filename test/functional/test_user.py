from test.DemoTestCase import DemoTestCase


class UserTest(DemoTestCase):
    def test_access_secure_area(self):
        r = self.get('/api/user')
        self.assertEqual(401, r.status_code)

    def test_login_bad_password(self):
        r = self.post(
            '/api/connect',
            {'user': 'admin', 'password': 'badpassword'}
        )
        print r.text
        self.assertEqual(401, r.status_code)

    def test_login_bad_password(self):
        r = self.post(
            '/api/connect',
            {'user': 'admin', 'password': 'admin'}
        )
        self.assertEqual(200, r.status_code)
