import unittest


def make_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(
        'calmjs.bower.tests', pattern='test_*.py')
    return test_suite
