# rpmunowned

This application finds all files and directories that are not part of any installed RPM package. Those files can be part of manually installed software, or can be created by applications at runtime like caches or logs. Another cause can be broken packages which do not declare their contents correctly, which leads to files being kept on disk after the package is removed.

`rpmunowned` was created to help you to keep your system tidy by creating a list of the absolute paths of all unowned files. You can then decide which files to keep and which to delete. Deletion of important files can break your system, so don't use this program unless you exactly know what you are doing.

I tested the script on Fedora, but it should work on any distribution using RPM as its package manager. For Debian-based distributions using APT, take a look at [apt-ext](https://github.com/davidhaller/apt-ext#unmanged) which works analogous.

## Usage

It's really straightforward:

    $ rpmunowned > unowned.txt

Per default, things like home directories or files on external hard drives are ignored. This command may run quite long, depending on your machine.

## Dependencies

`rpmunowned` is written in Python. You will need a Python interpreter (>= 3.0) and the additional modules `rpm` and `setproctitle`.
