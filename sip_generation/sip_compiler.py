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
"""SIP compiler driver for PyKDE."""
from __future__ import print_function
import argparse
import errno
import gettext
import os
import inspect
import logging
import re
import shutil
import sipconfig
import subprocess
import sys
import traceback

from PyQt5.QtCore import PYQT_CONFIGURATION

import rules_engine
from sip_bulk_generator import INCLUDES_EXTRACT, feature_for_sip_module


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


logger = logging.getLogger(__name__)
gettext.install(__name__)

# Keep PyCharm happy.
_ = _


class CxxDriver(object):
    def __init__(self, project_rules, input_dir, output_dir, verbose):
        """
        Constructor.

        :param project_rules:       The rules for the project.
        :param input_dir:           The source SIP directory.
        :param output_dir:          The destination CXX directory.
        :param verbose:             Debug info.
        """
        self.rules = project_rules
        self.includes = self.rules.includes()
        self.sips = self.rules.sips()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.verbose = verbose
        #
        # Get the SIP configuration information.
        #
        self.sipconfig = sipconfig.Configuration()
        self.pyqt_sip_flags = PYQT_CONFIGURATION["sip_flags"].split()
        #
        # Set up the project output directory.
        #
        try:
            os.makedirs(self.output_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open(os.path.join(self.output_dir, "__init__.py"), "w") as f:
            pass

    def process_modules(self, selector):
        """
        Run a set of SIP files, but don't throw any errors. At the end, throw the first error.

        :param selector:            A regular expression which limits the files from project_root to be processed.
        """
        error = None
        for source in self.rules.modules():
            try:
                if selector.search(source):
                    self.process_one_module(source.strip())
            except Exception as e:
                if not error:
                    error = e
        if error:
            raise error

    def process_one_module(self, sip_file):
        """
        Run a SIP file.

        :param sip_file:                    A SIP file name.
        """
        source = os.path.join(self.input_dir, sip_file)
        sip_roots = self.sips + [self.input_dir]
        sip_roots = ["-I" + i for i in sip_roots]
        #
        # Generate a file header. We don't automatically use a .sip suffix because that could cause a clash with the
        # legacy header on filesystems with case-insensitive lookups (NTFS).
        #
        module_path = os.path.dirname(sip_file)
        #
        # Write the header and the body.
        #
        full_output = os.path.join(self.output_dir, "tmp", module_path)
        build_file = os.path.join(full_output, "module.sbf")
        make_file = os.path.join(full_output, "module.Makefile")
        module_includes = os.path.join(full_output, "module.includes")
        modified_source = os.path.join(full_output, os.path.basename(sip_file) + ".tmp")
        try:
            os.makedirs(full_output)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        #
        # Make sure any errors mention the file that was being processed.
        #
        try:
            logger.info(_("Creating {}").format(full_output))
            #
            # Suppress the feature that corresponds to the SIP file being processed to avoid feeding SIP %Import
            # clauses which recursively refer to module beng processed. we do this by cloaking each in a %Feature,
            # and then disabling the one for "this".
            #
            # To avoid defining the %Feature multiple time, we put them inline in the current module.
            #
            with open(modified_source, "w") as o:
                with open(source, "rU") as i:
                    for line in i:
                        o.write(line)
                        if line.startswith("%Module"):
                            feature_list = os.path.join(self.input_dir, "modules.features")
                            tmp = set()
                            with open(feature_list, "rU") as f:
                                for feature in f:
                                    if feature not in tmp:
                                        tmp.add(feature)
                                        o.write(feature)
            logger.debug(modified_source)
            feature = sip_file.replace(os.path.sep, "_").replace(".", "_")
            cmd = [self.sipconfig.sip_bin, "-c", full_output, "-b", build_file, "-x", feature, "-X",
                   INCLUDES_EXTRACT + ":" + module_includes] + self.pyqt_sip_flags + sip_roots + [modified_source]
            self._run_command(cmd)
            #
            # Create the Makefile.
            #
            module_includes = self.includes + open(module_includes, "rU").read().split("\n")
            self.sipconfig._macros["INCDIR"] = " ".join(module_includes)
            makefile = sipconfig.SIPModuleMakefile(self.sipconfig, build_file, makefile=make_file)
            #
            # Add the library we are wrapping.  The name doesn't include any platform
            # specific prefixes or extensions (e.g. the "lib" prefix on UNIX, or the
            # ".dll" extension on Windows).
            #
            # TODO: replace this hardcoded list of libraries with some more apposite.
            #
            makefile.extra_libs = ["KF5DBusAddons", "KF5QuickAddons", "KF5ItemModels", "KF5Parts", "KF5People","KF5UnitConversion", "KF5Wallet", "KF5SonnetCore"]
            #
            makefile.generate()
            self._run_command(["make", "-f", os.path.basename(make_file)], cwd=full_output)
            #
            # TODO: this is not portable.
            #
            cpython_module = os.path.join(full_output, module_path + ".so")
            #
            # Publish the module.
            #
            logger.info(_("Publishing {}.{}").format(self.output_dir, module_path))
            shutil.copy(cpython_module, self.output_dir)
        except Exception as e:
            logger.error("{} while processing {}".format(e, source))
            raise

    def _run_command(self, cmd, *args, **kwds):
        if self.verbose:
            logger.info(" ".join(cmd))
        sub = subprocess.Popen(cmd, *args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwds)
        stdout, stderr = sub.communicate()
        stdout = stdout.strip()
        if sub.returncode:
            raise RuntimeError(stdout)
        if self.verbose and stdout:
            print(stdout)


def main(argv=None):
    """
    Run the SIP compiler, and the "make" the generated code.

    Examples:

        sip_compiler.py cxx sip KParts/kparts/module.sip
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(epilog=inspect.getdoc(main),
                                     formatter_class=HelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help=_("Enable verbose output"))
    parser.add_argument("--includes", default="/usr/include/x86_64-linux-gnu/qt5,/usr/include/KF5",
                        help=_("Comma-separated C++ header directories to use"))
    parser.add_argument("--sips", default="/usr/share/sip/PyQt5",
                        help=_("Comma-separated SIP module directories to use"))
    parser.add_argument("--project-rules", default=os.path.join(os.path.dirname(__file__), "rules_PyKF5.py"),
                        help=_("Project rules"))
    parser.add_argument("--select", default=".*", type=lambda s: re.compile(s, re.I) if not s.startswith("@") else s[1:],
                        help=_("Regular expression of SIP modules from '--project-rules' to be processed, or a filename starting with '@'"))
    parser.add_argument("sip", help=_("Root of SIP modules to process"))
    parser.add_argument("cxx", nargs="?", help=_("C++ output directory, default is project name from '--project-rules'"))
    try:
        args = parser.parse_args(argv[1:])
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        #
        # Compile!
        #
        rules = rules_engine.rules(args.project_rules, args.includes, args.sips)
        if not args.cxx:
            args.cxx = rules.project_name()
        if args.cxx != rules.project_name():
            logger.warn(_("{} must be renamed to {} before use").format(args.cxx, rules.project_name()))
        d = CxxDriver(rules, args.sip, args.cxx, args.verbose)
        if isinstance(args.select, str):
            d.process_one_module(args.select)
        else:
            d.process_modules(args.select)
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
