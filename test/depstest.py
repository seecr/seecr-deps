## begin license ##
#
# "Seecr Deps" to handle dependencies in python projects.
#
# Copyright (C) 2015 Seecr (Seek You Too B.V.) http://seecr.nl
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

from seecr.test import SeecrTestCase
from os import makedirs
from os.path import join
from seecr.deps import includeParentAndDeps

class DepsTest(SeecrTestCase):

    def testIncludeParentAndDeps(self):
        makedirs(join(self.tempdir, "bin"))

        systemPath = []
        includeParentAndDeps(join(self.tempdir, "bin", "thefile.py"), systemPath=systemPath)
        self.assertEqual([self.tempdir], systemPath)

        makedirs(join(self.tempdir, "deps.d", "dep_one"))
        makedirs(join(self.tempdir, "deps.d", "dep_two"))
        systemPath = []
        includeParentAndDeps(join(self.tempdir, "bin", "thefile.py"), systemPath=systemPath)
        self.assertEqual(set([self.tempdir, join(self.tempdir, "deps.d", "dep_two"), join(self.tempdir, "deps.d", "dep_one")]), set(systemPath))
