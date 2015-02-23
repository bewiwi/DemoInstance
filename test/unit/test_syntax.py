import pep8
from test.DemoTestCase import DemoTestCase


class SyntaxTest(DemoTestCase):
    def test_pep8_syntax(self):
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files([
            './demo.py',
            './test.py',
            './Demo/',
            './test/'
        ])
        self.assertEqual(
            result.total_errors,
            0,
            "Found %s code style errors (and warnings)." % result.total_errors
        )
