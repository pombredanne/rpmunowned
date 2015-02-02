#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 David Haller <davidhaller@outlook.com>
#
# rpmunowned is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rpmunowned is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

from os import walk
from os.path import join
from sys import exit

from setproctitle import setproctitle
import rpm


def absolute_file_list(root = "/", exclude = ("/home", "/dev", "/media", "/mnt",
                                              "/opt", "/proc", "/root", "/run",
                                              "/sys", "/tmp", "/var")) -> list:
    """
    Returns the absolute paths of all files in root,
    including sub directories.
    @param root: Directory where the search begins.
    @param exclude: Directories that won't be searched.
    """
    result = []

    for path, dirnames, filenames in walk(root):
        if not path.startswith(exclude):
            for dirname in dirnames:
                result.append(join(path, dirname))
            for filename in filenames:
                result.append(join(path, filename))
    return result


def owned_file_list() -> list:
    """
    Returns a list with the absolute paths
    of all installed files.
    """
    result = []
    ts = rpm.TransactionSet()

    for header in ts.dbMatch():
        for filename in header["FILENAMES"]:
            result.append(filename.decode(encoding = "UTF-8"))

    return result


def unowned_file_list() -> list:
    """
    Returns a list with the absolute paths
    of all files not owned by any package.
    """
    return sorted(set(absolute_file_list()) - set(owned_file_list()))


if __name__ == "__main__":
    setproctitle("rpmunowned")

    try:
        files = unowned_file_list()
        output = []

        for path in files:
            output.append(path)
            output.append("\n")

        print(str.strip("".join(output)))
        exit()

    except KeyboardInterrupt:
        exit()

