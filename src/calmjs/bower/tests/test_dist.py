# -*- coding: utf-8 -*-
import unittest
import json
import sys
import textwrap
from os.path import join
from pkg_resources import WorkingSet

from calmjs import dist
from calmjs.utils import fork_exec

from calmjs.testing.utils import mkdtemp
from calmjs.testing.utils import make_dummy_dist


class DistTestCase(unittest.TestCase):

    # While it really is for node/npm, the declaration is almost generic
    # enough that the particular method should be used here.
    def test_node_modules_registry_flattening(self):
        lib = make_dummy_dist(self, (
            ('requires.txt', '\n'.join([])),
            ('bower.json', json.dumps({
                'dependencies': {
                    'jquery': '~1.8.3',
                    'underscore': '1.8.3',
                },
            })),
            ('extras_calmjs.json', json.dumps({
                'bower_components': {
                    'jquery': 'jquery/dist/jquery.js',
                    'underscore': 'underscore/underscore-min.js',
                },
                'something_else': {'parent': 'lib'},
            })),
        ), 'lib', '1.0.0')

        app = make_dummy_dist(self, (
            ('requires.txt', '\n'.join([
                'lib>=1.0.0',
            ])),
            ('bower.json', json.dumps({
                'dependencies': {
                    'jquery': '~3.0.0',
                },
            })),
            ('extras_calmjs.json', json.dumps({
                'bower_components': {
                    'jquery': 'jquery/dist/jquery.min.js',
                },
                'something_else': {'child': 'named'},
            })),
        ), 'app', '2.0')

        working_set = WorkingSet()
        working_set.add(lib, self._calmjs_testing_tmpdir)
        working_set.add(app, self._calmjs_testing_tmpdir)

        results = dist.flatten_extras_calmjs(['app'], working_set=working_set)
        self.assertEqual(results['bower_components'], {
            'jquery': 'jquery/dist/jquery.min.js',
            'underscore': 'underscore/underscore-min.js',
        })
        # child takes precedences as this was not specified to be merged
        self.assertEqual(results['something_else'], {'child': 'named'})


class DistIntegrationTestCase(unittest.TestCase):
    """
    Testing integration of dist with the rest of calmjs and setuptools.
    """

    def setUp(self):
        """
        Set up the dummy test files.
        """

        self.pkg_root = mkdtemp(self)
        setup_py = join(self.pkg_root, 'setup.py')
        dummy_pkg = join(self.pkg_root, 'dummy_pkg.py')

        contents = (
            (setup_py, '''
                from setuptools import setup
                setup(
                    py_modules=['dummy_pkg'],
                    name='dummy_pkg',
                    bower_json={
                        'dependencies': {
                            'jquery': '~3.0.0',
                        },
                    },
                    extras_calmjs={
                        'bower_components': {
                            'jquery': 'jquery/dist/jquery.js',
                        },
                    },
                    zip_safe=False,
                )
            '''),
            (dummy_pkg, '''
            foo = 'bar'
            '''),
        )

        for fn, content in contents:
            with open(fn, 'w') as fd:
                fd.write(textwrap.dedent(content).lstrip())

    def test_setup_egg_info(self):
        """
        Emulate the execution of ``python setup.py egg_info``.

        Ensure everything is covered.
        """

        # naturally, run it like we mean it.
        stdout, stderr = fork_exec(
            [sys.executable, 'setup.py', 'egg_info'], cwd=self.pkg_root,)
        self.assertIn('writing bower_json', stdout)
        self.assertIn('writing extras_calmjs', stdout)

        egg_root = join(self.pkg_root, 'dummy_pkg.egg-info')

        with open(join(egg_root, 'bower.json')) as fd:
            self.assertEqual(json.load(fd), {
                'dependencies': {
                    'jquery': '~3.0.0',
                },
            })

        with open(join(egg_root, 'extras_calmjs.json')) as fd:
            self.assertEqual(json.load(fd), {
                'bower_components': {
                    'jquery': 'jquery/dist/jquery.js',
                },
            })
