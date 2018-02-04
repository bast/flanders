#!/usr/bin/env python

import os
import sys

from distutils.core import setup
from distutils import spawn
import distutils.command.build as _build
from distutils.sysconfig import get_python_lib


def extend_build(package_name):
    class build(_build.build):
        def run(self):
            cwd = os.getcwd()
            if spawn.find_executable('cmake') is None:
                sys.stderr.write("CMake is required to build this package.\n")
                sys.exit(-1)
            _source_dir = os.path.split(__file__)[0]
            _build_dir = os.path.join(_source_dir, 'build_setup_py')
            _prefix = os.path.join(get_python_lib(), package_name)
            try:
                spawn.spawn(['cmake',
                             '-H{0}'.format(_source_dir),
                             '-B{0}'.format(_build_dir),
                             '-DENABLE_OPENMP=True',
                             '-DCMAKE_INSTALL_PREFIX={0}'.format(_prefix),
                             ])
                spawn.spawn(['cmake',
                             '--build', _build_dir,
                             '--target', 'install'])
                os.chdir(cwd)
            except spawn.DistutilsExecError:
                sys.stderr.write("Error while building with CMake\n")
                sys.exit(-1)
            _build.build.run(self)
    return build

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.rst')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'flanders', 'version.py')) as f:
    exec(f.read(), version)


setup(
    name='flanders',
    version=version['__version__'],
    description=('Fast 2D nearest neighbor search with an angle.'),
    long_description=long_description,
    author='Radovan Bast',
    author_email='radovan.bast@uit.no',
    url='https://github.com/bast/flanders',
    license='MPL-2.0',
    packages=['flanders'],
    install_requires=[
        'cffi',
        'numpy',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
    cmdclass={'build': extend_build('flanders')},
    )
