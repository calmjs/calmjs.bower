# -*- coding: utf-8 -*-
"""
Module for dealing with bower framework.

Provides some helper functions that deal with bower.json, and also the
setuptools integration for certain bower features.
"""

from functools import partial

from calmjs.cli import PackageManagerDriver
from calmjs.command import PackageManagerCommand
from calmjs.dist import write_json_file
from calmjs.runtime import PackageManagerRuntime

BOWER_FIELD = 'bower_json'
BOWER_JSON = bower_json = 'bower.json'
BOWER = 'bower'
write_bower_json = partial(write_json_file, BOWER_FIELD)


class Driver(PackageManagerDriver):

    def __init__(self, **kw):
        kw['pkg_manager_bin'] = BOWER
        kw['pkgdef_filename'] = BOWER_JSON
        kw['description'] = "bower compatibility helper"
        super(Driver, self).__init__(**kw)


class bower(PackageManagerCommand):
    """
    The bower specific setuptools command.
    """

    # modules globals will be populated with friendly exported names.
    cli_driver = Driver.create_for_module_vars(globals())
    runtime = PackageManagerRuntime(
        cli_driver, package_name='calmjs.bower',
        description='bower support for the calmjs framework',
    )
    description = cli_driver.description

bower._initialize_user_options()
