import unittest
import argparse
from test.demo_test_case import DemoTestCase


def get_unit_test():
    return unittest.TestLoader().discover('test/unit')


def get_functional_test():
    return unittest.TestLoader().discover('test/functional')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-U', '--url', help='url to test',
        default='http://127.0.0.1:8080'
    )
    parser.add_argument(
        '-u', '--unit', help='run untit test',
        action='store_true'
    )
    parser.add_argument(
        '-f', '--functional', help='run functional test',
        action='store_true'
    )
    args = parser.parse_args()

    DemoTestCase.config['demo_url'] = args.url
    test_suite = unittest.TestSuite()
    if args.unit:
        test_suite.addTest(get_unit_test())
    if args.functional:
        test_suite.addTest(get_functional_test())

    runner = unittest.runner.TextTestRunner(verbosity=3)
    result = runner.run(test_suite)
    if not result.wasSuccessful():
        exit(1)
