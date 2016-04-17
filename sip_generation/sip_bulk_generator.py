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

from sip_generator import SipGenerator


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


logger = logging.getLogger(__name__)
gettext.install(__name__)

# Keep PyCharm happy.
_ = _


MODULE_SIP = "mod.sip"
INCLUDES_EXTRACT = "includes"

class SipBulkGenerator(SipGenerator):
    def __init__(self, project_rules, includes, sips, omitter, selector, project_root, output_dir):
        """
        Constructor.

        :param project_rules:       The rules file for the project.
        :param includes:            A list of roots of includes file, typically including the root for all Qt and
                                    the root for all KDE include files as well as any project-specific include files.
        :param omitter:             A regular expression which sets the files from project_root NOT to be processed.
        :param selector:            A regular expression which limits the files from project_root to be processed.
        :param project_root:        The root of files for which to generate SIP.
        :param output_dir:          The destination directory.
        """
        super(SipBulkGenerator, self).__init__(project_rules, includes, sips)
        self.includes = self.rule_set.includes()
        self.sips = self.rule_set.sips()
        self.root = project_root
        self.omitter = omitter
        self.selector = selector
        self.output_dir = output_dir
        self.include_to_sip_cache = {}

    def process_tree(self):
        self._walk_tree(self.root)

    def _walk_tree(self, root):
        """
        Walk over a directory tree and for each file or directory, apply a function.

        :param root:                Tree to be walked.
        """
        all_sip_imports = set()
        all_include_roots = set()
        names = sorted(os.listdir(root))
        sip_files = []
        for name in names:
            srcname = os.path.join(root, name)
            if os.path.isfile(srcname):
                sip_file, direct_includes, direct_sips = self._process_one(srcname)
                if sip_file:
                    sip_files.append(sip_file)
                    #
                    # Create something which the SIP compiler can process that includes what appears to be the
                    # immediate fanout from this module.
                    #
                    for include in direct_includes:
                        all_include_roots.add(os.path.dirname(include))
                    all_sip_imports.update(direct_sips)
            elif os.path.isdir(srcname):
                self._walk_tree(srcname)
        #
        # Create a SIP module including all the SIP files in this directory.
        #
        # NOTE: this is really only best-effort; the output here might have to be edited, or indeed
        # module files may need to be created from scratch if the logic here is not good enough.
        #
        if sip_files:
            h_dir = root[len(self.root) + len(os.path.sep):]
            output_file = os.path.join(h_dir, os.path.basename(h_dir) + MODULE_SIP)
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
                f.write("%Module(name={}.{})\n".format(self.rule_set.project_name(), h_dir.replace(os.path.sep, ".")))
                #
                # Create something which the SIP compiler can process that includes what appears to be the
                # immediate fanout from this module.
                #
                for sip_import in sorted(all_sip_imports):
                    if sip_import != output_file:
                        f.write("%Import {}\n".format(sip_import))
                f.write("%Extract(id={})\n".format(INCLUDES_EXTRACT))
                for include in sorted(all_include_roots):
                    f.write("{}\n".format(include))
                f.write("%End\n")
                #
                # Add all peer .sip files.
                #
                for sip_file in sip_files:
                    f.write("%Include {}\n".format(sip_file))

    def _map_include_to_sip(self, include):
        """
        For a given include file, return the corresponding SIP module.

        :param include:                 The name of a header file.
        :return: The name of a SIP module which represents the header file.
        """
        sip = self.include_to_sip_cache.get(include, None)
        if sip:
            return sip
        for include_root in self.includes:
            #
            # Assume only EXACTLY one root matches.
            #
            if include.startswith(include_root):
                i = include[len(include_root) + len(os.path.sep):]
                parent = os.path.dirname(i)
                sip = os.path.join(parent, os.path.basename(parent) + MODULE_SIP)
                return sip
        logger.debug(_("Cannot find SIP for {}").format(include))
        return None

    def _process_one(self, source):
        """
        Walk over a directory tree and for each file or directory, apply a function.

        :param source:              Source to be processed.
        :return:                    (output_file, set(direct includes from this file))
        """
        h_file = source[len(self.root) + len(os.path.sep):]
        if self.selector.search(h_file) and not self.omitter.search(h_file):
            #
            # Make sure any errors mention the file that was being processed.
            #
            try:
                if h_file.endswith("_export.h"):
                    result, includes = "", lambda : []
                elif h_file.endswith("_version.h"):
                    result, includes = "", lambda : []
                    version_defines = re.compile("^#define\s+(?P<name>\S+_VERSION\S*)\s+(?P<value>.+)")
                    with open(source, "rU") as f:
                        for line in f:
                            match = version_defines.match(line)
                            if match:
                                result += "{} = {}\n".format(match.group("name"), match.group("value"))
                else:
                    result, includes = self.create_sip(self.root, h_file)
                direct_includes = [i.include.name for i in includes() if i.depth == 1]
                if result:
                    pass
                elif len(direct_includes) == 1:
                    #
                    # A non-empty SIP file could not be created from the header file. That would be fine except that a
                    # common pattern is to use a single #include to create a "renaming header" to map a legacy header
                    # (usually lower case, and ending in .h) into a CamelCase header. Attempt to create a renaming
                    # SIP header.
                    #
                    included_h_file = direct_includes[0][len(self.root) + len(os.path.sep):]
                    sip_basename = os.path.basename(included_h_file)
                    sip_basename = os.path.splitext(sip_basename)[0] + ".sip"
                    module_path = os.path.dirname(included_h_file)
                    output_file = os.path.join(module_path, sip_basename)
                    result = "\n%Include {}\n".format(output_file)
                    direct_includes = [i.include.name for i in includes() if i.depth == 2]
                else:
                    direct_includes = []
                #
                # For each include, add the corresponding SIP module to the set to be %Import'd.
                #
                direct_sips = set()
                for include in direct_includes:
                    if self.omitter.search(include):
                        continue
                    if include.endswith("_version.h"):
                        continue
                    sip = self._map_include_to_sip(include)
                    if sip:
                        direct_sips.add(sip)
                #
                # Trim the includes to omit ones from paths we did not explicity add. This should get rid of compiler
                # added files and the like.
                #
                direct_includes = [i for i in direct_includes if i.startswith(tuple(self.includes))]
            except Exception as e:
                logger.error("{} while processing {}".format(e, source))
                raise
            if result:
                #
                # Generate a file header. We don't automatically use a .sip suffix because that could cause a clash
                # with the legacy header on filesystems with case-insensitive lookups (NTFS).
                #
                sip_basename = os.path.basename(h_file)
                if sip_basename.endswith(".h"):
                    sip_basename = os.path.splitext(sip_basename)[0] + ".sip"
                module_path = os.path.dirname(h_file)
                #
                # The SIP compiler ges very confused if you have a filename that matches a search path. Decollide...
                #
                if sip_basename == os.path.basename(module_path):
                    sip_basename += "_"
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
                return output_file, set(direct_includes), direct_sips
            else:
                logger.info(_("Not creating empty SIP for {}").format(source))
                return None, None, None
        else:
            logger.debug(_("Selector discarded {}").format(source))
            return None, None, None

    def header(self, output_file, h_file, module_path):
        """
        Override this to get your own preferred file header.

        :param output_file:                 The name of the output file.
        :param h_file:                      The name of the input file.
        :param module_path:                 The delta from the root.
        :return:
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
""".format(output_file, self.rule_set.project_name(), h_file, datetime.datetime.utcnow().year)
        return header


def main(argv=None):
    """
    Convert a whole set of KDE header files and generate the corresponding SIP
    files. Beyond simple generation of the SIP files from the corresponding C++
    header files:

        - A set of rules can be used to customise the generated SIP files.

        - For each set of SIP files in a directory, if at least one SIP file
          is named like a new-style header (i.e. starts with an upper case
          letter, or has no .h suffix), the a "module.sip" is created which
          facilitates running the SIP compiler on a set of related files.

    Examples:

        sip_bulk_generator.py /tmp /usr/include/KF5
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(epilog=inspect.getdoc(main),
                                     formatter_class=HelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help=_("Enable verbose output"))
    parser.add_argument("--includes", default="/usr/include/x86_64-linux-gnu/qt5",
                        help=_("Comma-separated C++ header directories to use"))
    parser.add_argument("--sips", default="/usr/share/sip/PyQt5",
                        help=_("Comma-separated SIP module directories to use"))
    parser.add_argument("--project-rules", default=os.path.join(os.path.dirname(__file__), "rules_PyKF5.py"),
                        help=_("Project rules"))
    parser.add_argument("--select", default=".*", type=lambda s: re.compile(s, re.I),
                        help=_("Regular expression of C++ headers under sources to be processed"))
    parser.add_argument("--omit", default="KDELibs4Support", type=lambda s: re.compile(s, re.I),
                        help=_("Regular expression of C++ headers under sources NOT to be processed"))
    parser.add_argument("sip", help=_("SIP output directory"))
    parser.add_argument("sources", default="/usr/include/KF5", nargs="?", help=_("C++ header directory to process"))
    try:
        args = parser.parse_args(argv[1:])
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        #
        # Generate!
        #
        d = SipBulkGenerator(args.project_rules, args.includes + "," + args.sources, args.sips, args.omit,
                             args.select, args.sources, args.sip)
        d.process_tree()
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
