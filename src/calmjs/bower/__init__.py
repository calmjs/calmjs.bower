# -*- coding: utf-8 -*-
"""
Module for dealing with bower framework.

Provides some helper functions that deal with bower.json
"""

from functools import partial

from calmjs import cli
from calmjs.npm import npm_bin
from calmjs.dist import write_json_file
from calmjs.command import GenericPackageManagerCommand

BOWER_FIELD = 'bower_json'
BOWER_JSON = 'bower.json'
BOWER = 'bower'


def Driver(interactive=False):
    return cli.Driver(
        interactive=interactive,
        pkg_manager_bin=BOWER, pkgdef_filename=BOWER_JSON)


_inst = Driver()
get_bower_version = _inst.get_pkg_manager_version
bower_init = _inst.bower_init
bower_install = _inst.bower_install
bower_json = _inst.pkgdef_filename
set_paths = _inst.set_paths

write_bower_json = partial(write_json_file, BOWER_FIELD)

# This next line could be very controversal.
#
# Reasoning is that the default instance is for the lazy/easy execution
# from the current directory.  Since node in general relies heavily on
# whatever is in the current directory, this assumption seems to make
# sense even though it can be really problematic if someone else
# executes the same Python script from a different directory using the
# same Python virtual environment.  In those case the script writer
# should create an explicit driver and have the directories pinned
# properly.
#
# I wish there is a better way to address this madness, although under
# the most typical use case (which is through setuptools, or the stand-
# alone entry points) this shouldn't matter much.  As for user specific
# scripts that import this module, they are better off to create their
# own Driver instance and do stuff with that.

set_paths(npm_bin())


class bower(GenericPackageManagerCommand):
    """
    The bower specific setuptools command.
    """

    cli_driver = _inst
    description = "bower compatibility helper"

bower._initialize_user_options()
