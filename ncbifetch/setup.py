# -*- coding: utf-8 -*-

import os, sys
import ncbifetch as project

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = ['ncbifetch']

requires = []

with open('requirements.txt') as fin:
    lines = fin.readlines()
for l in lines:
    requires.append(l.strip())

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name=project.__name__,
    version=project.__version__,
    description=project.__description__,
    long_description=readme,
    author=project.__author__,
    author_email=project.__author_email__,
    url=project.__url__,
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    license=license
)

