# -*- coding: utf-8 -*-
"""
Module for dealing with bower framework.

Provides some helper functions that deal with bower.json
"""

from functools import partial
import warnings
import os
from os.path import join
from os.path import exists

from calmjs import cli
from calmjs.dist import write_json_file
from calmjs.command import GenericPackageManagerCommand

BOWER_FIELD = 'bower_json'
BOWER_JSON = 'bower.json'
BOWER = 'bower'


class Driver(cli.PackageManagerDriver):

    def __init__(self, **kw):
        kw['pkg_manager_bin'] = BOWER
        kw['pkgdef_filename'] = BOWER_JSON
        super(Driver, self).__init__(**kw)


def _make_default_driver():
    inst = Driver()
    if inst.get_bower_version() is None:
        # Trying to work with NODE_PATH in not npm bin way.
        node_path = os.environ.get(
            'NODE_PATH', join(os.getcwd(), 'node_modules'))
        env_path = join(node_path, '.bin')
        if exists(join(env_path, BOWER)):
            inst.env_path = env_path

    if inst.get_bower_version() is None:
        inst.env_path = None
        warnings.warn(
            "'bower' binary not found; default module level functions will "
            "not work. Please either provide PATH and/or update "
            "os.environ['PATH'] to include one that provides, specify "
            "os.environ['NODE_PATH'] to the node_modules directory that has "
            "bower installed, or have npm install bower into the current "
            "working directory (%s) either directly through npm or using the "
            "calmjs framework. Once that is done, reload this module. "
            "Alternatively, create a manual bower Driver instance with "
            "manually defined arguments to required locations." % (
                os.getcwd(),
            ),
            RuntimeWarning,
        )

    return inst

_inst = _make_default_driver()

get_bower_version = _inst.get_bower_version
bower_init = _inst.bower_init
bower_install = _inst.bower_install
bower_json = _inst.pkgdef_filename

write_bower_json = partial(write_json_file, BOWER_FIELD)


class bower(GenericPackageManagerCommand):
    """
    The bower specific setuptools command.
    """

    cli_driver = _inst
    description = "bower compatibility helper"

bower._initialize_user_options()
