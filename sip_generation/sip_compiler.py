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
import sipconfig
import subprocess
import sys
import traceback

from PyQt5.QtCore import PYQT_CONFIGURATION

from sip_bulk_generator import INCLUDES_EXTRACT


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


logger = logging.getLogger(__name__)
gettext.install(__name__)

# Keep PyCharm happy.
_ = _


class CxxDriver(object):
    def __init__(self, includes, sips, output_dir, verbose):
        """
        Constructor.

        :param includes:            A list of roots of includes file, typically including the root for all Qt and
                                    the root for all KDE include files as well as any project-specific include files.
        :param sips:                A list of roots of SIP file, typically including the root for all Qt and
                                    the root for all KDE SIP files as well as any project-specific SIP files.
        :param output_dir:          The destination directory.
        :param verbose:             Debug info.
        """
        self.includes = includes
        self.sips = sips
        self.output_dir = output_dir
        self.verbose = verbose
        #
        # Get the SIP configuration information.
        #
        self.sipconfig = sipconfig.Configuration()
        self.pyqt_sip_flags = PYQT_CONFIGURATION["sip_flags"].split()

    def process_modules(self, root, sip_file):
        """
        Run a set of SIP files, but don't throw any errors. At the end, throw the first error.

        :param root:                        The prefix for all SIP files.
        :param sip_file:                    A SIP file name, or the name of a list of SIP files.
        """
        error = None
        if sip_file.startswith("@"):
            sources = open(sip_file[1:], "rU")
        else:
            sources = [sip_file]
        for source in sources:
            try:
                self._process_one_module(root, source.strip())
            except Exception as e:
                if not error:
                    error = e
        if isinstance(sources, file):
            sources.close()
        if error:
            raise error

    def _process_one_module(self, root, sip_file):
        """
        Run a SIP file.

        :param root:                        The prefix for the SIP files.
        :param sip_file:                    A SIP file name.
        """
        source = os.path.join(root, sip_file)
        sip_roots = self.sips + [root]
        sip_roots = ["-I" + i for i in sip_roots]
        #
        # Generate a file header. We don't automatically use a .sip suffix because that could cause a clash with the
        # legacy header on filesystems with case-insensitive lookups (NTFS).
        #
        module_path = os.path.dirname(sip_file)
        #
        # Write the header and the body.
        #
        full_output = os.path.join(self.output_dir, module_path)
        build_file = os.path.join(full_output, "module.sbf")
        make_file = os.path.join(full_output, "module.Makefile")
        module_includes = os.path.join(full_output, "module.includes")
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
            self._run_command([self.sipconfig.sip_bin, "-c", full_output, "-b", build_file, "-X",
                               INCLUDES_EXTRACT + ":" + module_includes] + self.pyqt_sip_flags + sip_roots + [source])
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
            #makefile.extra_libs = ["KParts"]
            #
            makefile.generate()
            logger.info(_("Compiling {}").format(full_output))
            self._run_command(["make", "-f", os.path.basename(make_file)], cwd=full_output)
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
                        help=_("Roots of C++ headers to include"))
    parser.add_argument("--sips", default="/usr/share/sip/PyQt5",
                        help=_("Roots of SIP modules to include"))
    parser.add_argument("cxx", help=_("C++ output directory"))
    parser.add_argument("sip", default="sip", help=_("Root of SIP modules to process"))
    parser.add_argument("source", help=_("SIP module to process, relative to project-root; a leading '@' signifies a file listing SIP modules"))
    try:
        args = parser.parse_args(argv[1:])
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        includes = args.includes.split(",")
        for path in includes:
            if not os.path.isdir(path):
                raise RuntimeError(_("--includes path '{}' is not a directory").format(path))
        sips = args.sips.split(",")
        for path in sips:
            if not os.path.isdir(path):
                raise RuntimeError(_("--sips path '{}' is not a directory").format(path))
        #
        # Generate!
        #
        d = CxxDriver(includes, sips, args.cxx, args.verbose)
        d.process_modules(args.sip, args.source)
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
