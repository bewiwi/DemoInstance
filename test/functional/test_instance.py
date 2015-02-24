from test.DemoTestCase import DemoTestCase


class InstanceTest(DemoTestCase):
    def setUp(self):
        self.login('admin', 'admin')

    def tearDown(self):
        self.remove_all()
        self.logout()

    def remove_all(self):
        r = self.get(
            '/api/myinstance'
        )
        rep = self.rep_to_dict(r.text)
        for instance in rep:
            if instance['status'] == 'DELETED':
                continue
            r = self.delete(
                '/api/instance/'+instance['id']
            )

    def create_instance(self, name, time):
        r = self.put(
            '/api/instance/' + name,
            {'image_name': name, 'time': time}
        )
        return self.rep_to_dict(r.text)

    def test_create_instances(self):
        r = self.put(
            '/api/instance/CIRROS3',
            {'image_name': 'CIRROS3', 'time': '2'}
        )
        self.assertEqual(201, r.status_code)

    def test_list_instances(self):
        instance = self.create_instance('CIRROS3', 2)

        r = self.get(
            '/api/instance/' + instance['id']
        )
        rep_get = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual(2, rep_get['ask_time'])

    def test_create_instance_overtime(self):
        instance = self.create_instance('CIRROS3', 9999)
        r = self.get(
            '/api/instance/' + instance['id']
        )
        rep_get = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual(22, rep_get['ask_time'])
