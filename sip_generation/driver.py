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
import datetime
import errno
import gettext
import os
import inspect
import logging
import re
import string
import sys
import traceback

from generator import Generator


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


logger = logging.getLogger(__name__)
gettext.install(__name__)

# Keep PyCharm happy.
_ = _


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
        self._walk_tree(self.root)

    def _walk_tree(self, root):
        """
        Walk over a directory tree and for each file or directory, apply a function.

        :param root:                Tree to be walked.
        """
        names = sorted(os.listdir(root))
        sip_files = []
        for name in names:
            srcname = os.path.join(root, name)
            if os.path.isfile(srcname):
                sip_file = self._process_one(srcname)
                if sip_file:
                    sip_files.append(sip_file)
            elif os.path.isdir(srcname):
                self._walk_tree(srcname)
        #
        # Create a SIP module including all the SIP files in this directory. We only want SIP files
        # generated from new-style header files.
        #
        # NOTE: this is really only best-effort; the output here might have to be edited, or indeed
        # module files may need to be created from scratch if the logic here is not good enough.
        #
        sip_files = [s for s in sip_files if s[0] in string.ascii_uppercase or not s.endswith(".sip")]
        if sip_files:
            h_dir = root[len(self.root) + len(os.path.sep):]
            output_file = os.path.join(h_dir, "module.sip")
            header = self.header(output_file, h_dir, h_dir)
            #
            # Write the header and the body.
            #
            full_output = os.path.join(self.output_dir, output_file)
            try:
                os.makedirs(os.path.dirname(full_output))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            logger.info(_("Creating {}").format(full_output))
            with open(full_output, "w") as f:
                f.write(header)
                f.write("""
%Module(name={})
%Include imports.sip
""".format(h_dir.replace(os.path.sep, ".")))
                for sip_file in sip_files:
                    f.write("%Include {}\n".format(sip_file))

    def _process_one(self, source):
        h_file = source[len(self.root) + len(os.path.sep):]
        if self.selector.search(h_file):
            #
            # Make sure any errors mention the file that was being processed.
            #
            try:
                result, includes = self.create_sip(self.root, h_file)
                if not result:
                    #
                    # Attempt to create a renaming header.
                    #
                    direct_includes = [i for i in includes if i.depth == 1]
                    if len(direct_includes) == 1:
                        included_h_file = direct_includes[0].include.name[len(self.root) + len(os.path.sep):]
                        sip_basename = os.path.basename(included_h_file)
                        sip_basename = os.path.splitext(sip_basename)[0] + ".sip"
                        module_path = os.path.dirname(h_file)
                        output_file = os.path.join(module_path, sip_basename)
                        result = """
%Include {}
""".format(output_file)
            except Exception as e:
                logger.error("{} while processing {}".format(e.message, source))
                raise
            if result:
                #
                # Generate a file header. We don't automatically use a .sip suffix because that could cause a clash with the
                # legacy header on filesystems with case-insensitive lookups (NTFS).
                #
                sip_basename = os.path.basename(h_file)
                if sip_basename.endswith(".h"):
                    sip_basename = os.path.splitext(sip_basename)[0] + ".sip"
                module_path = os.path.dirname(h_file)
                output_file = os.path.join(module_path, sip_basename)
                header = self.header(output_file, h_file, module_path)
                #
                # Write the header and the body.
                #
                full_output = os.path.join(self.output_dir, output_file)
                try:
                    os.makedirs(os.path.dirname(full_output))
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                logger.info(_("Creating {}").format(full_output))
                with open(full_output, "w") as f:
                    f.write(header)
                    f.write(result)
                return output_file
            else:
                logger.info(_("Not creating empty SIP for {}").format(source))
                return None

    def header(self, output_file, h_file, module_path):
        """
        Override this to get your own preferred file header.
        """
        header = """//
// This file, {}, is part of {}.
// It was derived from {}.
//
%Copying
// Copyright (c) {} by Shaheed Haque (srhaque@theiet.org)
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU Library General Public License as
// published by the Free Software Foundation; either version 2, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details
//
// You should have received a copy of the GNU Library General Public
// License along with this program; if not, write to the
// Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
%End
//
""".format(output_file, self.project_name, h_file, datetime.datetime.utcnow().year)
        return header


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
    parser.add_argument("--project-root", default="/usr/include/KF5", help=_("Root of header paths to process"))
    parser.add_argument("--selector", default=".*", type=lambda s: re.compile(s, re.I),
                        help=_("Regular expression of files under --project-root to process"))
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
        d = Driver(args.reference_includes, args.project_name, args.project_rules, args.project_root,
                   args.selector, args.output)
        d.process_tree()
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
