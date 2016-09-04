calmjs.bower
============

`Bower`_ support for the `calmjs`_ framework.

.. image:: https://travis-ci.org/calmjs/calmjs.bower.svg?branch=1.0.x
    :target: https://travis-ci.org/calmjs/calmjs.bower
.. image:: https://coveralls.io/repos/github/calmjs/calmjs.bower/badge.svg?branch=1.0.x
    :target: https://coveralls.io/github/calmjs/calmjs.bower?branch=1.0.x


Introduction
------------

This package provides the support for Bower into Python through the
|calmjs|_ framework.  Through the use of this package it is possible to
declare dependencies on |bower| packages through a ``bower_json``
section within a |setuptools|_ compatible ``setup.py`` for the given
Python package, to generate a ``bower.json`` file metadata which can be
referenced and reused by other Python packages that make use of the
|calmjs| framework.

For details on how this works, please refer to the documentation for the
|calmjs|_ package.

.. |bower| replace:: ``bower``
.. |calmjs| replace:: ``calmjs``
.. |calmjs.bower| replace:: ``calmjs.bower``
.. |npm| replace:: ``npm``
.. |setuptools| replace:: ``setuptools``
.. _calmjs: https://pypi.python.org/pypi/calmjs
.. _Bower: https://bower.io/
.. _Node.js: https://nodejs.org/
.. _setuptools: https://pypi.python.org/pypi/setuptools


Installation
------------

While the goal of |calmjs.bower| is to bring in the support of Bower
into |calmjs|, this library can function without Bower already installed
beforehand, as |calmjs| can be leveraged to bring Bower into the current
Python environment.  However, `Node.js`_ and |npm| must be installed and
available for this to be realized; if they are not installed please
follow the installation steps for Node.js appropriate for the running
environment/platform.

To install |calmjs.bower| into a given Python environment, it may be
installed directly from PyPI with the following command:

.. code:: sh

    $ pip install calmjs.bower

If a local installation of Bower into the current directory is desired,
it can be done through |calmjs| with the following command:

.. code:: sh

    $ calmjs npm --install calmjs.bower

Which does the equivalent of ``npm install bower``; while this does not
seem immediately advantageous, other Python packages that declared their
dependencies for specific sets of tool can be invoked like so, and to
follow through on that.  As an example, ``example.package`` may declare
dependencies on Bower through |npm| plus a number of other packages
available through |bower|, the process then simply become this:

.. code:: sh

    $ calmjs npm --install example.package
    $ calmjs bower --install example.package

All standard JavaScript and Node.js dependencies for ``example.package``
will now be installed into the current directory through the relevant
tools.  This process will also install all the other dependencies
through |npm| or |bower| that other Python packages depended on by
``example.package`` have declared.  For more usage please refer to
further down this document or the documentation for |calmjs|_.

Alternative installation methods (advanced users)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Development is still ongoing with |calmjs.bower|, for the latest
features and bug fixes, the development version can be installed through
git like so:

.. code:: sh

    $ pip install calmjs
    $ pip install git+https://github.com/calmjs/calmjs.bower.git#egg=calmjs.bower

Alternatively, the git repository can be cloned directly and execute
``python setup.py develop`` while inside the root of the source
directory.

Keep in mind that |calmjs| MUST be available before the ``setup.py``
within the |calmjs.bower| source tree is executed, for it needs the
``package_json`` writing capabilities in |calmjs|.  Please refer to the
base package for further information.

As |calmjs| is declared as both a namespace and a package, mixing
installation methods as described above when installing with other
|calmjs| packages may result in the module importer being unable to look
up the target module.  While this normally will not affect end users,
provided they use the same, standard installation method (i.e. wheel),
for developers it can be troublesome.  To resolve this, either stick to
the same installation method for all packages (i.e. ``python setup.py
develop``), or import a module from the main |calmjs| package.  Here
is an example run:

.. code:: python

    >>> import calmjs.bower
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ImportError: No module named 'calmjs.bower'
    >>> import calmjs.base
    >>> import calmjs.bower
    >>> 

If this behavior (and workaround) is undesirable, please ensure the
installation of all |calmjs| related packages follow the same method
(i.e. either ``python setup.py develop`` for all packages, or using the
wheels acquired through ``pip``).

Testing the installation
~~~~~~~~~~~~~~~~~~~~~~~~

To ensure that the |calmjs| installation is functioning correctly, the
built-in testsuite can be executed by the following command:

.. code:: sh

    $ python -m unittest calmjs.bower.tests.make_suite

If there are failures, please file an issue on the issue tracker with
the full traceback, and/or the method of installation.  Please also
remember to include platform specific information, such as Python
version, operating system environments and version, and other related
information related to the issue at hand.


Usage
-----

The |calmjs.bower| package will install the appropriate hooks into the
|calmjs| console entry point and also |setuptools| to facilitate the
generation of ``bower.json`` from the ``bower_json`` declarations in the
current package or other packages installed in the current environment.

If no packages with conflicting declarations are installed, with the
|bower| binary available through the ``PATH`` environment variable (or
in the current directory's ``node_modules``), running the utility will
result in something like this:

.. code:: sh

    $ calmjs
    usage: calmjs [-h] [-d] [-q] [-v] [-V] <command> ...

    positional arguments:
      <command>
        npm          npm compatibility helper
        bower        bower compatibility helper

If |bower| was not available, a warning will also be displayed,
however this should only affect operations that need the binary itself.
As for details with usage, please invoke ``calmjs bower --help``.

The following help outlines typical usage of |bower| with declarations
by supporting Python packages through |calmjs|, so much of the help is
copied and shared from that package, modified from its support for
|npm|.

Declare a ``bower.json`` for a given Python package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a package wish to declare dependencies on packages available through
|bower|, it may do something like this in its ``setup.py``:

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
            'calmjs.bower',
            ...
        ],
        bower_json=bower_json,
        ...
    )

This will let users of this package install all the dependencies through
the appropriate package managers as outlined above in the installation
section.

Declare explicit dependencies on paths inside ``bower_components``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given that the dependencies on specific versions of packages sourced
from |bower| is explicitly specified, build tools will benefit again
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
conflicts with existing declarations in other packages within the
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
currently implemented, so behavior of usage of |bower| through calmjs
will not account for locations that may be specified in that file.  For
the standard use case where dependencies are installed to some separate
directory as part of a typical |calmjs| workflow it should not pose a
problem.


Troubleshooting
---------------

Here are some common issues that may be encountered with typical usage
of |calmjs.bower|.

RuntimeWarning: Unable to locate the 'bower' binary;
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If this message appears, this simply means the default module setup
(i.e. ``from calmjs import bower``) could not find a usable |bower|
binary/runtime when it was imported.  As the default runtime does
various setup it only means that the helper methods may not be usable
out of the box.  This can always be rectified by having |bower| already
installed in the current directory (through |npm|) or have it be
available through the ``PATH`` environment variable.  Full details on
what can be done is written in the error message.


Contribute
----------

- Issue Tracker: https://github.com/calmjs/calmjs.bower/issues
- Source Code: https://github.com/calmjs/calmjs.bower


Legal
-----

The |calmjs.bower| package is part of the calmjs project.

The calmjs project is copyright (c) 2016 Auckland Bioengineering
Institute, University of Auckland.  |calmjs.bower| is licensed under the
terms of the GPLv2 or later.
