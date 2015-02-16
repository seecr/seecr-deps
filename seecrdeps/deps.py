## begin license ##
#
# "Seecr Deps" to handle dependencies in python projects.
#
# Copyright (C) 2014-2015 Seecr (Seek You Too B.V.) http://seecr.nl
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

from platform import dist
from subprocess import Popen, PIPE
from StringIO import StringIO
from functools import partial
from os import rename
import sys

class Deps(object):
    def __init__(self, filename):
        self._filename = filename
        self.packageVersionFind = packageVersionFind()
        self._myDistro = myDistro()

    def update(self, inline=True):
        output = StringIO()
        packagesSeen = []
        with open(self._filename, 'r') as fp:
            for line in (l.strip() for l in fp):
                if line == '' or line.startswith("# "):
                    output.write("%s\n" % line)
                    continue
                
                name, version = line.split(' ', 1) if ' ' in line else (line, None)
                distro, name = name.split(':', 1) if ':' in name else (None, name)
                if not distro is None:
                    distro = distro[1:]

                # skip if already done, this gets rid of the 2nd line with the << line for packages
                if (distro, name) in packagesSeen:
                    continue
               
                # if a distro is set but its not my distro, print and skip
                if not distro is None and distro != self._myDistro:
                    output.write("%s\n" % line)
                    continue

                # find installed version, write lines with distro added if needed
                installedVersion = self.packageVersionFind(name)
                if installedVersion is None:
                    sys.stderr.write("Package '%s' listed but not installed.\n" % name)
                    sys.stderr.flush()
                    output.write("%s\n" % line)
                    continue
                
                # 'VERSION' is reserved and will be replaced at package build time
                if version is None or 'VERSION' in version:
                    output.write("%s\n" % line)
                    continue

                if not distro is None:
                    output.write("#%s:" % distro)
                output.write("%s (>= %s)\n" % (name, installedVersion))
                if not distro is None:
                    output.write("#%s:" % distro)
                output.write("%s (<< %s)\n" % (name, nextMajorVersion(installedVersion)))
                packagesSeen.append((distro, name))

        result = output.getvalue().strip()
        if inline is True:
            with open("%s.tmp" % self._filename, "w") as fp:
                fp.write(result)
            rename("%s.tmp" % self._filename, self._filename)
        elif inline is False:
            print(result)

def nextMajorVersion(version):
    if version is None:
        return ''
    parts = version.split('.')[:2] if '.' in version else (version, '0')
    return '%s.%s' % (parts[0], int(parts[1])+1)

def myDistro():
    distro, version, codename = dist()
    majorVersion = version[0]
    if distro == 'debian':
        proc = Popen(["lsb_release", "-sc"], stdout=PIPE)
        try:
            codename, _ = proc.communicate()
        finally:
            proc.wait()
            codename = codename.decode().strip()
        return codename
    return "%s%s" % (distro, majorVersion)

def packageVersionFind():
    distro = dist()[0]
    if distro == 'debian':
        from apt import Cache
        return partial(debian_find_version, Cache())
    elif distro in ['centos', 'redhat']:
        from yum import YumBase
        return partial(redhat_find_version, YumBase())
    else:
        raise RuntimeError("Unsupported distro")

def debian_find_version(cache, packageName):
    if packageName not in cache or cache[packageName].installed is None:
        return None

    installedVersion = cache[packageName].installed.version
    if '-' in installedVersion:
        installedVersion = installedVersion.split('-', 1)[0]
    return installedVersion

def redhat_find_version(cache, packageName):
    result = cache.rpmdb.searchNevra(name=packageName)
    return result[0].version if result else None
