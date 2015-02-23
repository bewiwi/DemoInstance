import unittest
import argparse
from test.DemoTestCase import DemoTestCase


def run_unit_test():
    test_suite = unittest.TestLoader().discover('test/unit')
    test_runner = unittest.runner.TextTestRunner()
    test_runner.run(test_suite)


def run_functional_test():
    test_suite = unittest.TestLoader().discover('test/functional')
    test_runner = unittest.runner.TextTestRunner()
    test_runner.run(test_suite)


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
    if args.unit:
        run_unit_test()
    if args.functional:
        run_functional_test()
