import unittest
from os.path import dirname


def make_suite():
    import calmjs.bower
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(
        'calmjs.bower.tests', pattern='test_*.py',
        # namespace packages are actually going to interfere if not
        # very explicit here.
        top_level_dir=dirname(calmjs.bower.__file__)
    )
    return test_suite
