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
        self.assertEqual('Sugar', rep['name'])
        self.assertEqual('SugarCRM', rep['desc'])
        self.assertEqual('Les identifiants', rep['info'])
        self.assertEqual('/instance_image/sugar.jpg', rep['img'])

    def test_get_image_info2(self):
        r = self.get('/api/image/BI')
        rep = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual('BI2', rep['name'])
        self.assertEqual('Baam', rep['desc'])
        self.assertEqual(80, rep['max_time'])

    def test_default_value(self):
        r = self.get('/api/image/GITLAB')
        rep = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual('Gitlab', rep['name'])
        self.assertEqual('no desc', rep['desc'])
        self.assertEqual(2, rep['default_time'])
        self.assertEqual('\'image with no info\'', rep['info'])
