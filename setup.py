from setuptools import setup, find_packages

version = '1.0.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

classifiers = """
Development Status :: 5 - Production/Stable
Environment :: Console
Framework :: Setuptools Plugin
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)
Operating System :: OS Independent
Programming Language :: JavaScript
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
""".strip().splitlines()

setup(
    name='calmjs.bower',
    version=version,
    description="Bower support for the calmjs framework.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=classifiers,
    keywords='',
    author='Tommy Yu',
    author_email='tommy.yu@auckland.ac.nz',
    url='https://github.com/calmjs/calmjs.bower',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_json={
        'dependencies': {
            'bower': '~1.7.0',
        },
    },
    namespace_packages=['calmjs'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'calmjs>=1.0.2',
    ],
    entry_points={
        'calmjs.extras_keys': [
            'bower_components = enabled',
        ],
        'calmjs.runtime': [
            'bower = calmjs.bower:bower.runtime',
        ],
        'distutils.commands': [
            'bower = calmjs.bower:bower',
        ],
        'distutils.setup_keywords': [
            'bower_json = calmjs.dist:validate_json_field',
        ],
        'egg_info.writers': [
            'bower.json = calmjs.bower:write_bower_json',
        ],
    },
    test_suite="calmjs.bower.tests.make_suite",
    )
