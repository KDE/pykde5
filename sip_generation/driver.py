#!/usr/bin/env python
#
# Copyright 2016 by Shaheed Haque (srhaque@theiet.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA.
#
"""SIP file generator driver for PyKDE."""
from __future__ import print_function
import argparse
import errno
import gettext
import os
import inspect
import logging
import re
import sys
import traceback

from generator import Generator


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


logger = logging.getLogger(__name__)
gettext.install(__name__)

# Keep PyCharm happy.
_ = _


def walk_tree(root, fn, filter):
    """
    Walk over a directory tree and for each file passed by a filter, apply a function.

    :param root:                Tree to be walked.
    :param fn:                  Function to apply.
    :param filter:              Filter to use.
    """
    names = os.listdir(root)
    for name in names:
        srcname = os.path.join(root, name)
        if filter(srcname):
            fn(srcname)
        if os.path.isdir(srcname):
            walk_tree(srcname, fn, filter)


class Driver(Generator):
    def __init__(self, include_roots, project_name, project_rules, project_root, selector, output_dir):
        """
        Constructor.

        :param include_roots:       A list of roots of includes file, typically including the root for all Qt and
                                    the root for all KDE include files as well as any project-specific include files.
        :param project_name:        The name of the project.
        :param project_rules:       The rules file for the project.
        :param project_root:        The root of files for which to generate SIP.
        :param selector:            A regular expression which limits the files from project_root to be processed.
        :param output_dir:          The destination directory.
        """
        super(Driver, self).__init__(include_roots, project_name, project_rules)
        self.root = project_root
        self.selector = selector
        self.output_dir = output_dir

    def process_tree(self):
        walk_tree(self.root, self._process_one, os.path.isfile)

    def _process_one(self, file):
        if self.selector.search(os.path.basename(file)):
            result, copyright, sip_file = self.create_sip(file)
            if result:
                output_file = os.path.join(os.path.dirname(file), sip_file)
                output_file = output_file[len(self.root) + len(os.path.sep):]
                output_file = os.path.join(self.output_dir, output_file)
                try:
                    os.makedirs(os.path.dirname(output_file))
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                logger.info(_("Creating {}").format(output_file))
                with open(output_file, "w") as f:
                    f.write(copyright)
                    for r in result:
                        f.write(r)
            else:
                logger.info(_("Not creating empty SIP for {}").format(file))


def main(argv=None):
    """
    Convert a whole set of KDE header files and generate the corresponding SIP files.

    Examples:

        driver.py /tmp
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(epilog=inspect.getdoc(main),
                                     formatter_class=HelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help=_("Enable verbose output"))
    parser.add_argument("--reference-includes", default=["/usr/include/x86_64-linux-gnu/qt5", "/usr/include/KF5"],
                        action="append", help=_("Roots of header paths"))
    parser.add_argument("--project-name", default="PyKF5", help=_("Project name"))
    parser.add_argument("--project-rules", default=os.path.join(os.path.dirname(__file__), "rules_PyKF5.py"),
                        help=_("Project rules"))
    parser.add_argument("--project-includes", default="/usr/include/KF5", help=_("Root of header paths to process"))
    parser.add_argument("--selector", default=".*", type=re.compile, help=_("Regular expression of files under --project-includes to process"))
    parser.add_argument("output", help=_("Output directory"))
    try:
        args = parser.parse_args(argv[1:])
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        #
        # Generate!
        #
        d = Driver(args.reference_includes, args.project_name, args.project_rules, args.project_includes,
                   args.selector, args.output)
        d.process_tree()
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
