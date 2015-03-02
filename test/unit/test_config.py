from test.demo_test_case import DemoTestCase
from Demo.demo_config import DemoConfig
from Demo.demo_exception import DemoExceptionConfigNotFound


class ConfigTest(DemoTestCase):
    def test_config_missing(self):
        DemoConfig.config_file = 'test/samples/config/config-notfound.ini'
        self.assertRaises(DemoExceptionConfigNotFound, DemoConfig)

    def test_config_ok(self):
        DemoConfig.config_file = 'test/samples/config/config-fake.ini'
        DemoConfig()
