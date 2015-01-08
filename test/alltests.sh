#!/bin/bash
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

set -o errexit
export LANG=en_US.UTF-8
export PYTHONPATH=.:"$PYTHONPATH"
option=$1
pyversions=""
if [ -f /usr/bin/python2.6 ]; then
    pyversions="python2.6"
fi
if [ -f /usr/bin/python2.7 ]; then
    pyversions="python2.7"
fi
if [ "${option:0:10}" == "--python2." ]; then
    shift
    pyversions="${option:2}"
fi
for pycmd in $pyversions; do
    echo "================ $pycmd _alltests.py $@ ================"
    $pycmd _alltests.py "$@"
done