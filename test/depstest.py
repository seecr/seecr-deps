## begin license ##
#
# "Seecr Deps" to handle dependencies in python projects.
#
# Copyright (C) 2015-2016, 2019 Seecr (Seek You Too B.V.) http://seecr.nl
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
from os.path import join, isdir
from seecrdeps import includeParentAndDeps


def _ensureDir(*args):
    path = join(*args)
    if not isdir(path):
        makedirs(path)
    return path


class DepsTest(SeecrTestCase):
    def testIncludeParentAndDeps(self):
        bindir = _ensureDir(self.tempdir, "bin")

        systemPath = []
        includeParentAndDeps(join(bindir, "thefile.py"), systemPath=systemPath)
        self.assertEqual([self.tempdir], systemPath)
        depOne = _ensureDir(self.tempdir, "deps.d", "dep_one")
        depTwo = _ensureDir(self.tempdir, "deps.d", "dep_two")
        systemPath = []
        includeParentAndDeps(join(bindir, "thefile.py"), systemPath=systemPath)
        self.assertEqual(set([self.tempdir, depOne, depTwo]), set(systemPath))

    def testIncludeParentAndDepsScanForParent(self):
        bindir = _ensureDir(self.tempdir, "level1", "level2", "bin")
        depOne = _ensureDir(self.tempdir, "deps.d", "dep_one")
        systemPath = []
        includeParentAndDeps(join(bindir, "thefile.py"), systemPath=systemPath, scanForDeps=True)
        self.assertEqual(set([self.tempdir, depOne]), set(systemPath))

    def testAdditionalPaths(self):
        bindir = _ensureDir(self.tempdir, "bin")

        systemPath = []
        includeParentAndDeps(
            join(bindir, "thefile.py"),
            systemPath=systemPath,
            additionalPaths=['1', '2'])
        self.assertEqual(set(['1', '2', self.tempdir]), set(systemPath))

    def testAdditionalPathsRelativeFromParent(self):
        bindir = _ensureDir(self.tempdir, "bin")

        systemPath = []
        includeParentAndDeps(
            join(bindir, "thefile.py"),
            systemPath=systemPath,
            additionalPaths=['1', '2'],
            additionalPathsRelativeFromParent=True)
        self.assertEqual(set([join(self.tempdir, '1'), join(self.tempdir, '2'), self.tempdir]), set(systemPath))
