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
        :param project_name:        The name of the project.
        :param project_rules:       The rules file for the project.
        :param project_root:        The root of files for which to generate SIP.
        :param selector:            A regular expression which limits the files from project_root to be processed.
        :param output_dir:          The destination directory.
        """
        self.includes = includes
        self.sips = sips
        self.output_dir = output_dir
        self.verbose = verbose
        #
        # Get the SIP configuration information.
        #
        # g++ -I/usr/include/python2.7 -I/usr/include/x86_64-linux-gnu/qt5/QtCore -I/usr/include/x86_64-linux-gnu/qt5 -fPIC -shared -o t.so cxx/KParts/sipKPartscmodule.cpp /usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0
        #
        self.sipconfig = sipconfig.Configuration()
        self.sipconfig._macros["INCDIR"]="/usr/include/x86_64-linux-gnu/qt5/QtCore /usr/include/x86_64-linux-gnu/qt5"
        self.pyqt_sip_flags = PYQT_CONFIGURATION["sip_flags"].split()

    def process_modules(self, root, sip_file):
        error = None
        if sip_file.startswith("@"):
            sources = open(sip_file[1:], "rU")
        else:
            sources = [sip_file]
        for source in sources:
            try:
                self._process_one_module(root, source)
            except Exception as e:
                if not error:
                    error = e
        if isinstance(sources, file):
            sources.close()
        if error:
            raise e

    def _process_one_module(self, root, sip_file):
        source = os.path.join(root, sip_file)
        includes = self.sips + [root]
        includes = ["-I" + i for i in includes]
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
        try:
            os.makedirs(full_output)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        logger.info(_("Creating {}").format(full_output))
        #
        # Make sure any errors mention the file that was being processed.
        #
        try:
            self._run_command([self.sipconfig.sip_bin, "-c", full_output, "-b", build_file] + self.pyqt_sip_flags +
                                   includes + [source])
            #
            # Create the Makefile.
            #
            makefile = sipconfig.SIPModuleMakefile(self.sipconfig, build_file, makefile=make_file)
            #
            # Add the library we are wrapping.  The name doesn't include any platform
            # specific prefixes or extensions (e.g. the "lib" prefix on UNIX, or the
            # ".dll" extension on Windows).
            #makefile.extra_libs = ["KParts"]
            #
            makefile.generate()
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
    Convert a whole set of KDE header files and generate the corresponding SIP
    files. Beyond simple generation of the SIP files from the corresponding C++
    header files:

        - A set of rules can be used to customise the generated SIP files.

        - For each set of SIP files in a directory, if at least one SIP file
          is named like a new-style header (i.e. starts with an upper case
          letter, or has no .h suffix), the a "module.sip" is created which
          facilitates running the SIP compiler on a set of related files.

    Examples:

        driver.py /tmp /usr/include/KF5
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(epilog=inspect.getdoc(main),
                                     formatter_class=HelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help=_("Enable verbose output"))
    parser.add_argument("--includes", default=["/usr/include/x86_64-linux-gnu/qt5", "/usr/include/KF5"],
                        action="append", help=_("Roots of C++ headers to include"))
    parser.add_argument("--sips", default=["/usr/share/sip/PyQt5"],
                        action="append", help=_("Roots of SIP modules to include"))
    parser.add_argument("cxx", help=_("C++ output directory"))
    parser.add_argument("sip", default="sip", help=_("Root of SIP modules to process"))
    parser.add_argument("source", help=_("SIP module to process, relative to project-root; a leading '@' signifies a file listing SIP modules"))
    try:
        args = parser.parse_args(argv[1:])
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        #
        # Generate!
        #
        d = CxxDriver(args.includes, args.sips, args.cxx, args.verbose)
        d.process_modules(args.sip, args.source)
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
