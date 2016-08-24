from setuptools import setup, find_packages

version = '0.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
    name='calmjs.bower',
    version=version,
    description="Bower support through calmjs.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      "Programming Language :: Python",
      ],
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
        'calmjs',
    ],
    entry_points={
        'calmjs.extras_keys': [
            'bower_components = enabled',
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
