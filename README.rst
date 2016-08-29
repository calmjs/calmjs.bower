calmjs.bower
============

Bower support for calmjs.

.. image:: https://travis-ci.org/calmjs/calmjs.bower.svg?branch=master
    :target: https://travis-ci.org/calmjs/calmjs.bower
.. image:: https://coveralls.io/repos/github/calmjs/calmjs.bower/badge.svg?branch=master
    :target: https://coveralls.io/github/calmjs/calmjs.bower?branch=master


Introduction
------------

This package provides bower support through the |calmjs|_ framework for
extending JavaScript ecosystem support into Python.  Through the use of
this package it is possible to declare dependencies on |bower|_ packages
through a ``bower_json`` section within a |setuptools|_ compatible
``setup.py`` for the given Python package.

For details on how this works, please refer to |calmjs|_.

.. |setuptools| replace:: ``setuptools``
.. |bower| replace:: ``bower``
.. |calmjs| replace:: ``calmjs``
.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _calmjs: https://pypi.python.org/pypi/calmjs
.. _bower: https://bower.io/


Usage
-----

Much of the following is copied from the documentation relating the the
support of ``npm`` within ``calmjs``, though modified for ``bower``.

Declare a ``bower.json`` for a given Python package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a package wish to declare dependencies on packages available through
``bower``, it may do something like this in its ``setup.py``:

.. code:: python

    from setuptools import setup

    bower_json = {
        "dependencies": {
            "jquery": "~3.0.0",
            "underscore": "~1.8.0",
        }
    }

    setup(
        name='example.package',
        ...
        install_requires=[
            'calmjs',
            ...
        ],
        bower_json=bower_json,
        ...
    )

Declare explicit dependencies on paths inside ``bower_components``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given that the dependencies on specific versions of packages sourced
from ``bower`` is explicitly specified, build tools will benefit again
from explicit declarations on files needed from those packages.  Namely,
the compiled packages could be declared in the ``extras_calmjs`` section
in JSON string much like ``bower_json``, like so:

.. code:: python

    extras_calmjs = {
        'bower_components': {
            'jquery': 'jquery/dist/jquery.js',
            'underscore': 'underscore/underscore.js',
        },
    }

    setup(
        name='example.package',
        ...
        extras_calmjs=extras_calmjs,
        ...
    )

Since ``bower_components`` is declared to be an ``extras_key``,
conflicits with existing declarations in other packages within the
environment will be merged like how dependencies sections declared in
``bower_json``.

Please do note that complete paths must be declared (note that the
``.js`` filename suffix is included in the example); directories can
also be declared.  However, as these declarations are done from within
Python, explicit, full paths are required thus it is up to downstream
integration packages to properly handle and/or convert this into the
conventions that standard Node.js tools might expect (i.e. where the
``.js`` filename suffix is omitted).

As of now, the support of ``.bowerrc`` configuration settings is not
currently implemented.

Command line utility
~~~~~~~~~~~~~~~~~~~~

The ``calmjs.bower`` package will install the appropriate hooks into the
``calmjs`` console entry point and also ``setuptools`` to facilitate the
generation of ``bower.json`` from the ``bower_json`` declarations in the
current package or other packages installed in the current environment.

If no packages with conflicting declarations are installed, with the
``bower`` binary available through the ``PATH`` environment variable (or
in the current directory's ``node_modules``), running the utility will
result in something like this:

.. code:: sh

    $ calmjs
    usage: calmjs [-h] [-v] [-q] [-d] <command> ...

    positional arguments:
      <command>
        npm          npm compatibility helper
        bower        bower compatibility helper

If ``bower`` was not available, a warning will also be displayed,
however this should only affect operations that need the binary itself.
As for details with usage, please invoke ``calmjs bower --help``.


Contribute
----------

- Issue Tracker: https://github.com/calmjs/calmjs.bower/issues
- Source Code: https://github.com/calmjs/calmjs.bower


License
-------

The ``calmjs.bower`` package is part of the ``calmjs`` project, and it
is licensed under the GPLv2 or later.
