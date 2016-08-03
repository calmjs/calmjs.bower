# -*- coding: utf-8 -*-
"""
Module for dealing with bower framework.

Provides some helper functions that deal with bower.json
"""

from functools import partial

from calmjs.cli import Driver
from calmjs.dist import write_json_file
from calmjs.command import GenericPackageManagerCommand

BOWER_FIELD = 'bower_json'
BOWER_JSON = 'bower.json'
BOWER = 'bower'

_inst = Driver(
    interactive=False, pkg_manager_bin=BOWER, pkgdef_filename=BOWER_JSON)
get_bower_version = _inst.get_pkg_manager_version
bower_init = _inst.pkg_manager_init
bower_install = _inst.pkg_manager_install
bower_json = _inst.pkgdef_filename

write_bower_json = partial(write_json_file, BOWER_FIELD)


class bower(GenericPackageManagerCommand):
    """
    The bower specific setuptools command.
    """

    cli_driver = _inst
    description = "bower compatibility helper"

bower._initialize_user_options()
