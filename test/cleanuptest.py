## begin license ##
#
# "Seecr Deps" to handle dependencies in python projects.
#
# Copyright (C) 2019-2021 Seecr (Seek You Too B.V.) http://seecr.nl
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
from os.path import join, isfile
from seecrdeps import cleanup

class CleanUpTest(SeecrTestCase):

    def testCleanUp(self):
        makedirs(join(self.tempdir, "folder"))
        pycFile = join(self.tempdir, "folder", "blah.pyc")
        pyFile = join(self.tempdir, "folder", "blah.py")
        for f in [pyFile, pycFile]:
            with open(f,'w') as fp:
                fp.write("")
        self.assertTrue(isfile(pyFile))
        self.assertTrue(isfile(pycFile))

        cleanup(self.tempdir)
        self.assertTrue(isfile(pyFile))
        self.assertFalse(isfile(pycFile))

