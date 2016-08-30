# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import warnings
import unittest
import json
import os
import sys
from os.path import join
from os.path import exists

from setuptools.dist import Distribution
from pkg_resources import WorkingSet

from calmjs import cli
from calmjs import npm
from calmjs.utils import fork_exec

from calmjs.testing.utils import mkdtemp
from calmjs.testing.utils import make_dummy_dist
from calmjs.testing.utils import stub_dist_flatten_egginfo_json
from calmjs.testing.utils import stub_mod_call
from calmjs.testing.utils import stub_mod_check_interactive
from calmjs.testing.utils import stub_stdin
from calmjs.testing.utils import stub_stdouts

# suppressing warning as tests should be run within a context with no
# immediate availability of node_modules and/or bower
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    from calmjs.bower import Driver
    from calmjs.bower import bower as global_bower


class DistCommandTestCase(unittest.TestCase):
    """
    Test case for the commands within.
    """

    def setUp(self):
        self.cwd = os.getcwd()

        app = make_dummy_dist(self, (
            ('requires.txt', '\n'.join([])),
            ('bower.json', json.dumps({
                'dependencies': {'jquery': '~1.11.0'},
            })),
        ), 'foo', '1.9.0')

        working_set = WorkingSet()
        working_set.add(app, self._calmjs_testing_tmpdir)

        # Stub out the flatten_egginfo_json calls with one that uses our
        # custom working_set here.
        stub_dist_flatten_egginfo_json(self, [cli], working_set)
        # Quiet stdout from distutils logs
        stub_stdouts(self)
        # Force auto-detected interactive mode to True, because this is
        # typically executed within an interactive context.
        stub_mod_check_interactive(self, [cli], True)

    def tearDown(self):
        os.chdir(self.cwd)

    def test_no_args(self):
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()
        out = sys.stdout.getvalue()
        self.assertIn('\n        "jquery": "~1.11.0"', out)

    def test_interactive_only(self):
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower', '-i'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()
        out = sys.stdout.getvalue()
        self.assertIn('\n        "jquery": "~1.11.0"', out)

    def test_view(self):
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower', '--view'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()
        out = sys.stdout.getvalue()
        self.assertIn('\n        "jquery": "~1.11.0"', out)

    def test_init_no_overwrite_default_input_interactive(self):
        tmpdir = mkdtemp(self)
        stub_stdin(self, u'')  # default should be no

        with open(os.path.join(tmpdir, 'bower.json'), 'w') as fd:
            json.dump(
                {'dependencies': {}, 'devDependencies': {}}, fd, indent=None)

        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower', '--init', '--interactive'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()

        with open(os.path.join(tmpdir, 'bower.json')) as fd:
            # Should not have overwritten
            result = json.loads(fd.readline())

        self.assertEqual(result, {
            'dependencies': {},
            'devDependencies': {},
        })

        stdout = sys.stdout.getvalue()
        self.assertTrue(stdout.startswith("running bower\n"))

        target = join(tmpdir, 'bower.json')

        self.assertIn(
            "generating a flattened 'bower.json' for 'foo'\n"
            "Generated 'bower.json' differs with '%s'" % (target),
            stdout
        )

        # That the diff additional block is inside
        self.assertIn(
            '+     "dependencies": {\n'
            '+         "jquery": "~1.11.0"\n'
            '+     },',
            stdout,
        )

        self.assertIn(
            "not overwriting existing '%s'\n" % target,
            sys.stderr.getvalue(),
        )

    def test_init_overwrite(self):
        tmpdir = mkdtemp(self)

        with open(os.path.join(tmpdir, 'bower.json'), 'w') as fd:
            json.dump({'dependencies': {}, 'devDependencies': {}}, fd)

        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower', '--init', '--overwrite'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()

        with open(os.path.join(tmpdir, 'bower.json')) as fd:
            result = json.load(fd)

        # gets overwritten anyway.
        self.assertEqual(result, {
            'dependencies': {'jquery': '~1.11.0'},
            'devDependencies': {},
            'name': 'foo',
        })

    def test_init_merge(self):
        # --merge without --interactive implies overwrite
        tmpdir = mkdtemp(self)

        with open(os.path.join(tmpdir, 'bower.json'), 'w') as fd:
            json.dump({'dependencies': {
                'underscore': '~1.8.0',
            }, 'devDependencies': {
                'sinon': '~1.17.0',
            }}, fd)

        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower', '--init', '--merge'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()

        with open(os.path.join(tmpdir, 'bower.json')) as fd:
            result = json.load(fd)

        # gets overwritten as we explicitly asked
        self.assertEqual(result, {
            'dependencies': {'jquery': '~1.11.0', 'underscore': '~1.8.0'},
            'devDependencies': {'sinon': '~1.17.0'},
            'name': 'foo',
        })

    def test_init_merge_interactive_default(self):
        tmpdir = mkdtemp(self)
        stub_stdin(self, u'')

        with open(os.path.join(tmpdir, 'bower.json'), 'w') as fd:
            json.dump({'dependencies': {
                'underscore': '~1.8.0',
            }, 'devDependencies': {
                'sinon': '~1.17.0',
            }}, fd)

        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower', '--init', '--merge', '--interactive'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()

        stdout = sys.stdout.getvalue()
        self.assertIn('+         "jquery": "~1.11.0",', stdout)

        with open(os.path.join(tmpdir, 'bower.json')) as fd:
            result = json.load(fd)

        # Nothing happened.
        self.assertEqual(result, {
            'dependencies': {'underscore': '~1.8.0'},
            'devDependencies': {'sinon': '~1.17.0'},
        })

    def test_install_no_init(self):
        stub_mod_call(self, cli)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower', '--install'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()

        with open(os.path.join(tmpdir, 'bower.json')) as fd:
            result = json.load(fd)

        # The cli will still automatically write to that, as install
        # implies init.
        self.assertEqual(result, {
            'dependencies': {'jquery': '~1.11.0'},
            'devDependencies': {},
            'name': 'foo',
        })
        args, kwargs = self.call_args
        self.assertEqual(args, (['bower', 'install'],))

    def test_install_no_init_has_bower_json_interactive_default_input(self):
        stub_stdin(self, u'')
        stub_mod_call(self, cli)
        tmpdir = mkdtemp(self)

        with open(os.path.join(tmpdir, 'bower.json'), 'w') as fd:
            json.dump({
                'dependencies': {'jquery': '~3.0.0'},
                'devDependencies': {}
            }, fd)

        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower', '--install', '--interactive'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()

        with open(os.path.join(tmpdir, 'bower.json')) as fd:
            result = json.load(fd)

        # Existing bower.json will not be overwritten.
        self.assertEqual(result, {
            'dependencies': {'jquery': '~3.0.0'},
            'devDependencies': {},
        })
        # Ensure that install is NOT called.
        self.assertIsNone(self.call_args)

    def test_install_false(self):
        stub_mod_call(self, cli)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(
            script_name='setup.py',
            script_args=['bower', '--install', '--dry-run'],
            name='foo',
        ))
        dist.parse_command_line()
        dist.run_commands()

        self.assertFalse(exists(join(tmpdir, 'bower.json')))
        # Ensure that install is NOT called.
        self.assertIsNone(self.call_args)


@unittest.skipIf(npm.get_npm_version() is None, 'npm not available')
class BowerTestCase(unittest.TestCase):
    """
    Test actual integration with node.
    """

    def setUp(self):
        self.cwd = os.getcwd()

    def tearDown(self):
        os.chdir(self.cwd)

    def test_integration(self):
        """
        Actually calling the real npm through the calmjs npm_install
        method on this package and then executing the result.
        """

        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        npm.npm_install('calmjs.bower')
        # Use the version that will set the environment.
        bower = Driver.create()
        self.assertTrue(exists(join(tmpdir, 'node_modules', '.bin', 'bower')))
        # should have the actual version declared in package_json
        self.assertEqual(bower.get_bower_version(), (1, 7, 9))


class BowerRuntimeTestCase(unittest.TestCase):

    def test_standalone_main(self):
        stub_stdouts(self)
        with self.assertRaises(SystemExit):
            global_bower.runtime(['-h'])
        # Have the help work
        self.assertIn('bower support for the calmjs', sys.stdout.getvalue())

    def test_standalone_main_version(self):
        stub_stdouts(self)
        # the default call method does NOT call sys.exit.
        with self.assertRaises(SystemExit):
            global_bower.runtime(['-V'])
        self.assertIn('calmjs.bower', sys.stdout.getvalue())
        self.assertIn('from', sys.stdout.getvalue())

    def test_standalone_reuse_main(self):
        stub_stdouts(self)
        # the default call method does NOT call sys.exit.
        global_bower.runtime(['calmjs', '-vv'])
        # Have the help work
        result = json.loads(sys.stdout.getvalue())
        self.assertEqual(result['dependencies'], {})
        err = sys.stderr.getvalue()
        self.assertIn('DEBUG', err)

    def test_standalone_subprocess(self):
        # Invoke __main__
        stdout, stderr = fork_exec(
            [sys.executable, '-m', 'calmjs.bower', 'calmjs.bower', '-vv'])
        result = json.loads(stdout)
        self.assertEqual(result['dependencies'], {})
        self.assertIn('DEBUG', stderr)
