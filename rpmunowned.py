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

import rpm


def all_files(root="/", exclude=("/home", "/boot", "/dev", "/media",
                                          "/mnt", "/proc", "/root", "/run",
                                          "/sys", "/tmp", "/var")):
    """
    Returns the absolute paths of all files in root,
    including subdirectories.
    @param root: Directory where the search begins.
    @param exclude: Directories that won't be searched.
    """

    for path, dirnames, filenames in walk(root):
        if not path.startswith(exclude):
            for dirname in dirnames:
                yield join(path, dirname)
            for filename in filenames:
                yield join(path, filename)


def owned_files():
    """
    Returns the absolute paths of all installed files.
    """
    ts = rpm.TransactionSet()

    for header in ts.dbMatch():
        for filename in header["FILENAMES"]:
            yield filename.decode(encoding="UTF-8")


def unowned_files() -> list:
    """
    Returns a list with the absolute paths
    of all files not owned by any package.
    """
    return sorted(set(all_files()) - set(owned_files()))


if __name__ == "__main__":
    try:
        for path in unowned_files():
            print(path)
        exit()
    except KeyboardInterrupt:
        exit("\nProgram aborted by user.")
