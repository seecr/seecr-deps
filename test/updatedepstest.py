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

from seecr.test import SeecrTestCase
from seecr.test.io import stdout_replaced, stderr_replaced
from os import makedirs
from os.path import join
from seecrdeps.deps import Deps, nextMajorVersion

class UpdateDepsTest(SeecrTestCase):

    def testWrittenToOutput(self):
        filename = join(self.tempdir, "deps.txt")
        with open(filename, "w") as fp:
            fp.write("""# This is a comment
python
seecr-deps (>= 1.0)
seecr-deps (<< 1.1)
#jessie:python3-weightless-core (>= 1.0)
# Another comment line just to be annoying
#jessie:python3-weightless-core (<< 1.1)
#centos7:python-weightless-core (>= 0.1)
#centos7:python-weightless-core (<< 0.2)
#wheezy:python-weightless-core""")

        deps = Deps(filename=filename)
        deps._myDistro = 'jessie'
        versions = {'python': '3.4', 'seecr-deps': '1.2.3.4', 'python3-weightless-core': '2.0'}
        deps.packageVersionFind = lambda packageName: versions[packageName] if packageName in versions else None
        with stdout_replaced() as strm:
            deps.update(inline=False)

        self.assertEqual("""# This is a comment
python
seecr-deps (>= 1.2.3.4)
seecr-deps (<< 1.3)
#jessie:python3-weightless-core (>= 2.0)
#jessie:python3-weightless-core (<< 2.1)
# Another comment line just to be annoying
#centos7:python-weightless-core (>= 0.1)
#centos7:python-weightless-core (<< 0.2)
#wheezy:python-weightless-core
""", strm.getvalue())

    def testInline(self):
        filename = join(self.tempdir, "deps.txt")
        with open(filename, "w") as fp:
            fp.write("""# This is a comment
python
seecr-deps (>= 1.0)
seecr-deps (<< 1.1)
#jessie:python3-weightless-core (>= 1.0)
# Another comment line just to be annoying
#jessie:python3-weightless-core (<< 1.1)
#centos7:python-weightless-core (>= 0.1)
#centos7:python-weightless-core (<< 0.2)
#wheezy:python-weightless-core
""")

        deps = Deps(filename=filename)
        deps._myDistro = 'jessie'
        versions = {'python': '3.4', 'seecr-deps': '1.2.3.4', 'python3-weightless-core': '2.0'}
        deps.packageVersionFind = lambda packageName: versions[packageName] if packageName in versions else None
        deps.update(inline=True)
        with open(filename, 'r') as fp:
            self.assertEqual("""# This is a comment
python
seecr-deps (>= 1.2.3.4)
seecr-deps (<< 1.3)
#jessie:python3-weightless-core (>= 2.0)
#jessie:python3-weightless-core (<< 2.1)
# Another comment line just to be annoying
#centos7:python-weightless-core (>= 0.1)
#centos7:python-weightless-core (<< 0.2)
#wheezy:python-weightless-core""", fp.read())

    def testPackageListedButNotInstalled(self):
        filename = join(self.tempdir, "deps.txt")
        with open(filename, "w") as fp:
            fp.write("""packageName""")
        deps = Deps(filename=filename)
        deps.packageVersionFind = lambda packageName: None
        with stderr_replaced() as errStrm:
            deps.update(inline=True)
            self.assertEqual("Package 'packageName' listed but not installed.\n", errStrm.getvalue())
        with open(filename, "r") as fp:
            self.assertEqual("packageName", fp.read())

    def testLeaveVERSIONKeywordAlone(self):
        filename = join(self.tempdir, "deps.txt")
        with open(filename, "w") as fp:
            fp.write("""package (= VERSION)""")
        deps = Deps(filename=filename)
        deps.packageVersionFind = lambda packageName: '1.0'
        deps.update(inline=True)
        with open(filename, "r") as fp:
            self.assertEqual("package (= VERSION)", fp.read())

    def testNextMajorVersion(self):
        self.assertEqual('1.1', nextMajorVersion('1.0'))
        self.assertEqual('1.1', nextMajorVersion('1.0.1.2'))
        self.assertEqual('1.1', nextMajorVersion('1'))
        self.assertEqual('', nextMajorVersion(None))

