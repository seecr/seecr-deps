#!/usr/bin/env python3
## begin license ##
#
# "Seecr Deps" to handle dependencies in python projects.
#
# Copyright (C) 2011-2015, 2019 Seecr (Seek You Too B.V.) http://seecr.nl
#
# This file is part of "Seecr Deps"
#
# "Seecr Deps" is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# "Seecr Deps" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with "Seecr Deps"; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
## end license ##

from distutils.core import setup

version = '$Version: 1.4.x$'[9:-1].strip()

from os import walk
from os.path import join
scripts = []
for path, dirs, files in walk('bin'):
    for file in files:
        if file == 'sitecustomize.py':
            continue
        scripts.append(join(path, file))

setup(
    name='seecrdeps',
    packages=['seecrdeps'],
    scripts=scripts,
    version=version,
    url='http://www.seecr.nl',
    author='Seecr',
    author_email='info@seecr.nl',
    description='Tools for dependencies',
    long_description='Tools to handle dependencies in python projects.',
    platforms=['linux'],
)
