# -*- coding: utf-8 -*-
import unittest
import json
import os
import sys
from os.path import join

import pkg_resources

from calmjs import cli
from calmjs import runtime

from calmjs.testing import mocks
from calmjs.testing.utils import make_dummy_dist
from calmjs.testing.utils import mkdtemp
from calmjs.testing.utils import remember_cwd
from calmjs.testing.utils import stub_dist_flatten_egginfo_json
from calmjs.testing.utils import stub_mod_call
from calmjs.testing.utils import stub_mod_check_interactive
from calmjs.testing.utils import stub_stdouts


class IntegrationTestCase(unittest.TestCase):

    def test_calmjs_main_console_entry_point(self):
        stub_stdouts(self)
        with self.assertRaises(SystemExit):
            runtime.main(['-h'])
        # ensure our base action module/class is registered.
        self.assertIn('bower', sys.stdout.getvalue())

    def setup_runtime(self):
        make_dummy_dist(self, (
            ('bower.json', json.dumps({
                'name': 'site',
                'dependencies': {
                    'jquery': '~3.1.0',
                },
            })),
        ), 'example.package1', '1.0')

        make_dummy_dist(self, (
            ('bower.json', json.dumps({
                'name': 'site',
                'dependencies': {
                    'underscore': '~1.8.3',
                },
            })),
        ), 'example.package2', '2.0')

        working_set = pkg_resources.WorkingSet([self._calmjs_testing_tmpdir])

        # Stub out the underlying data needed for the cli for the tests
        # to test against our custom data for reproducibility.
        stub_dist_flatten_egginfo_json(self, [cli], working_set)
        stub_mod_check_interactive(self, [cli], True)

        # Of course, apply a mock working set for the runtime instance
        # so it can use the bower runtime.
        working_set = mocks.WorkingSet({
            'calmjs.runtime': [
                'bower = calmjs.bower:bower.runtime',
            ],
        })
        return runtime.Runtime(working_set=working_set)

    def test_bower_init_integration(self):
        remember_cwd(self)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)

        rt = self.setup_runtime()
        rt(['bower', '--init', 'example.package1'])

        with open(join(tmpdir, 'bower.json')) as fd:
            result = json.load(fd)

        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')

    def test_bower_install_integration(self):
        remember_cwd(self)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        stub_mod_call(self, cli)
        rt = self.setup_runtime()
        rt(['bower', '--install', 'example.package1', 'example.package2'])

        with open(join(tmpdir, 'bower.json')) as fd:
            result = json.load(fd)

        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')
        # not foo install, but bower install since entry point specified
        # the actual runtime instance.
        self.assertEqual(self.call_args, ((['bower', 'install'],), {}))

    def test_bower_view(self):
        remember_cwd(self)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        stub_stdouts(self)
        rt = self.setup_runtime()
        rt(['bower', '--view', 'example.package1', 'example.package2'])
        result = json.loads(sys.stdout.getvalue())
        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')

        stub_stdouts(self)
        rt(['bower', 'example.package1', 'example.package2'])
        result = json.loads(sys.stdout.getvalue())
        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')

    def test_bower_all_the_actions(self):
        remember_cwd(self)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        stub_stdouts(self)
        stub_mod_call(self, cli)
        rt = self.setup_runtime()
        rt(['bower', '--install', '--view', '--init',
            'example.package1', 'example.package2'])

        # inside stdout
        result = json.loads(sys.stdout.getvalue())
        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')

        with open(join(tmpdir, 'bower.json')) as fd:
            result = json.load(fd)

        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')
        self.assertEqual(self.call_args, ((['bower', 'install'],), {}))