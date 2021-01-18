## begin license ##
#
# "Seecr Deps" to handle dependencies in python projects.
#
# Copyright (C) 2015, 2019-2021 Seecr (Seek You Too B.V.) https://seecr.nl
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

from os import getuid
assert getuid() != 0, "Do not run tests as 'root'"

from os.path import dirname, abspath                           #DO_NOT_DISTRIBUTE
parentdir = dirname(dirname(abspath(__file__)))                #DO_NOT_DISTRIBUTE
from os import system                                          #DO_NOT_DISTRIBUTE
from sys import path as sysPath                                #DO_NOT_DISTRIBUTE
system('find "%s" -name "*.pyc" | xargs rm -f' % parentdir)    #DO_NOT_DISTRIBUTE
sysPath.insert(0, parentdir)                                   #DO_NOT_DISTRIBUTE

from unittest import main

from depstest import DepsTest
from updatedepstest import UpdateDepsTest
from cleanuptest import CleanUpTest

if __name__ == '__main__':
    main()
