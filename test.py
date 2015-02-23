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
    parser.add_argument('-u', help='url to test', default='http://127.0.0.1')
    args = parser.parse_args()

    DemoTestCase.config['demo_url'] = args.u
    run_unit_test()
    run_functional_test()
