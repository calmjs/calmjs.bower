# -*- coding: utf-8 -*-
"""
Module for dealing with bower framework.

Provides some helper functions that deal with bower.json, and also the
setuptools integration for certain bower features.
"""

from functools import partial

from calmjs import cli
from calmjs.dist import write_json_file
from calmjs.command import GenericPackageManagerCommand

BOWER_FIELD = 'bower_json'
BOWER_JSON = bower_json = 'bower.json'
BOWER = 'bower'
write_bower_json = partial(write_json_file, BOWER_FIELD)


class Driver(cli.PackageManagerDriver):

    def __init__(self, **kw):
        kw['pkg_manager_bin'] = BOWER
        kw['pkgdef_filename'] = BOWER_JSON
        super(Driver, self).__init__(**kw)


class bower(GenericPackageManagerCommand):
    """
    The bower specific setuptools command.
    """

    # modules globals will be populated with friendly exported names.
    cli_driver = Driver.create(globals())
    description = "bower compatibility helper"

bower._initialize_user_options()
