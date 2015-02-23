from test.DemoTestCase import DemoTestCase


class ImageTest(DemoTestCase):
    def setUp(self):
        self.login('admin', 'admin')

    def tearDown(self):
        self.logout()

    def test_get_images(self):
        r = self.get('/api/image')
        rep = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual(5, len(rep))

    def test_get_image_info(self):
        r = self.get('/api/image/SUGAR')
        rep = self.rep_to_dict(r.text)
        self.assertEqual(200, r.status_code)