from test.demo_test_case import DemoTestCase


class UserTest(DemoTestCase):
    def test_access_secure_area(self):
        r = self.get('/api/user')
        self.assertEqual(401, r.status_code)

    def test_login_bad_password(self):
        r = self.post(
            '/api/connect',
            {'user': 'admin', 'password': 'badpassword'}
        )
        self.assertEqual(401, r.status_code)

    def test_login_good_password(self):
        r = self.post(
            '/api/connect',
            {'user': 'admin', 'password': 'admin'}
        )
        self.assertEqual(200, r.status_code)

    def test_get_info(self):
        self.login('admin', 'admin')
        r = self.get('/api/user')
        rep = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual('admin', rep['login'])
