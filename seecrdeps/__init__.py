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

from os.path import abspath, dirname, isdir, join, isfile, splitext, islink
from os import walk, remove
from glob import glob

def includeParentAndDeps(filename, systemPath=None, additionalPaths=None, scanForDeps=False, additionalPathsRelativeFromParent=False):
    if systemPath is None:
        from sys import path as systemPath

    parentDirectory = dirname(dirname(abspath(filename)))
    if scanForDeps:
        parentDirectory = _scanForDeps(parentDirectory) or parentDirectory

    depsDirectory = join(parentDirectory, "deps.d")
    if isdir(depsDirectory) or islink(depsDirectory):
        for path in glob(join(depsDirectory, "*")):
            systemPath.insert(0, path)
    systemPath.insert(0, parentDirectory)

    for path in reversed(additionalPaths or []):
        systemPath.insert(0, join(parentDirectory, path) if additionalPathsRelativeFromParent else path)

def _scanFor(path, condition):
    return None if path == '/' else path if condition(path) else _scanFor(dirname(path), condition)

def _scanForGit(path):
    return _scanFor(path, lambda path: isdir(join(path, ".git")))

def _scanForDeps(path):
    return _scanFor(path, lambda path: isfile(join(path, "deps.txt")) or isdir(join(path, "deps.d")))

def cleanup(filename, extentions=None):
    if not extentions:
        extentions = ['.pyc']
    directory = dirname(abspath(filename))
    startDirectory = _scanForGit(directory) or _scanForDeps(directory) or directory

    for curdir, _, filenames in walk(startDirectory):
        list(map(remove, [join(curdir, f) for f in filenames if splitext(f)[1] in extentions]))
