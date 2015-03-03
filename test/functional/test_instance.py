from test.demo_test_case import DemoTestCase


class InstanceTest(DemoTestCase):
    def setUp(self):
        self.login('admin', 'admin')

    def tearDown(self):
        self.login('admin', 'admin')
        self.remove_all()
        self.login('test', 'test')
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

    def create_instance(self, name, time=None):
        data = {'name': name}
        if time is not None:
            data['time'] = time
        r = self.put(
            '/api/instance/' + name,
            data
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
        self.assertEqual(2, rep_get['life_time'])

    def test_create_instance_overtime(self):
        instance = self.create_instance('CIRROS3', 9999)
        r = self.get(
            '/api/instance/' + instance['id']
        )
        rep_get = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual(22, rep_get['life_time'])

    def test_get_instance_from_other_user(self):
        instance = self.create_instance('CIRROS3', 9999)
        self.login('test', 'test')
        r = self.get(
            '/api/instance/' + instance['id']
        )

        self.assertEqual(401, r.status_code)

    def test_delete_instance_from_other_user_non_admin(self):
        instance = self.create_instance('CIRROS3', 9999)
        self.login('test', 'test')

        r_del = self.delete(
            '/api/instance/' + instance['id']
        )
        self.assertEqual(401, r_del.status_code)

        self.login('admin', 'admin')
        r = self.get(
            '/api/instance/' + instance['id']
        )
        self.assertEqual(200, r.status_code)

    def test_delete_instance_from_other_user_admin(self):
        self.login('test', 'test')
        instance = self.create_instance('CIRROS3', 9999)

        self.login('admin', 'admin')
        r_del = self.delete(
            '/api/instance/' + instance['id']
        )
        self.assertEqual(200, r_del.status_code)

        r = self.get(
            '/api/instance/' + instance['id']
        )
        self.assertEqual(404, r.status_code)

    def test_update_time_instance(self):
        instance = self.create_instance('BI', 10)
        r = self.post(
            '/api/instance/' + instance['id'],
            {'id': instance['id'], 'add_time': 8}
        )
        self.assertEqual(200, r.status_code)

        r = self.get(
            '/api/instance/' + instance['id']
        )
        rep_get = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual(18, rep_get['life_time'])

    def test_update_time_from_other_user_instance(self):
        instance = self.create_instance('BI', 10)
        self.login('test', 'test')
        r = self.post(
            '/api/instance/' + instance['id'],
            {'id': instance['id'], 'add_time': 8}
        )
        self.assertEqual(401, r.status_code)
        self.login('admin', 'admin')
        r = self.get(
            '/api/instance/' + instance['id']
        )
        rep_get = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual(10, rep_get['life_time'])

    def test_update_time_of_nonupdatable_instance(self):
        instance = self.create_instance('CIRROS2')

        # Check time
        r = self.get(
            '/api/instance/' + instance['id']
        )
        rep_get = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual(20, rep_get['life_time'])

        # Try Update
        r = self.post(
            '/api/instance/' + instance['id'],
            {'id': instance['id'], 'add_time': 99999}
        )
        self.assertEqual(400, r.status_code)

        # Recheck Time
        r = self.get(
            '/api/instance/' + instance['id']
        )
        rep_get = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual(20, rep_get['life_time'])

    def test_get_all_instance_from_non_admin(self):
        self.login('test', 'test')
        r = self.get(
            '/api/allinstance'
        )

        self.assertEqual(404, r.status_code)

    def test_get_all_instance_from_admin(self):
        self.login('test', 'test')
        instance = self.create_instance('CIRROS2', 30)
        self.login('admin', 'admin')
        r = self.get(
            '/api/allinstance'
        )

        self.assertEqual(200, r.status_code)

    def test_set_instance_time_from_admin(self):
        instance = self.create_instance('CIRROS2', 30)
        r = self.post(
            '/api/instance/' + instance['id'],
            {'id': instance['id'], 'time': 600}
        )
        r = self.get(
            '/api/instance/' + instance['id']
        )
        rep_get = self.rep_to_dict(r.text)

        self.assertEqual(200, r.status_code)
        self.assertEqual(600, rep_get['life_time'])
