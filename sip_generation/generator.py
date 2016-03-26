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
"""SIP file generator for PyKDE."""
from __future__ import print_function
import argparse
import datetime
import gettext
import inspect
import logging
import os
import subprocess
import sys
import traceback
from clang import cindex
from clang.cindex import CursorKind, SourceRange, TokenKind, AccessSpecifier

import rules
from rules import apply_function_rules, apply_param_rules


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


logger = logging.getLogger(__name__)
gettext.install(__name__)

# Keep PyCharm happy.
_ = _


def walk_directories(root, fn):
    """
    Walk over a directory tree and for each directory, apply a function.

    :param root:                Tree to be walked.
    :param fn:                  Function to apply.
    :return: None
    """
    names = os.listdir(root)
    for name in names:
        srcname = os.path.join(root, name)
        if os.path.isdir(srcname):
            fn(srcname)
        if os.path.isdir(srcname):
            walk_directories(srcname, fn)


class Generator(object):
    _libclang = None

    def __init__(self, qt_includes, kde_includes, dump_includes=False):
        """
        Constructor.

        :param qt_includes:         The root for all Qt include files.
        :param kde_includes:        The root for all KDE include files.
        :param dump_includes:       Turn on diagnostics for include files.
        """
        Generator._find_libclang()
        self.includes = set()
        self.includes.add(qt_includes)
        self.includes.add(kde_includes)
        walk_directories(qt_includes, lambda d: self.includes.add(d))
        walk_directories(kde_includes, lambda d: self.includes.add(d))
        if dump_includes:
            for include in sorted(self.includes):
                logger.debug(_("Using includes from {}").format(include))
        self.dump_includes = dump_includes
        self.diagnostics = set()
        self.tu = None
        self.unpreprocessed_source = None

    def create_sip(self, source):
        """
        Actually convert the given source header file into its SIP equivalent.

        :param source:             The source (header) file of interest.
        """
        #
        # Read in the original file.
        #
        self.unpreprocessed_source = []
        with open(source, "rU") as f:
            for line in f:
                self.unpreprocessed_source.append(line)
        #
        # Create and populate the index.
        #
        includes = ["-I" + i for i in self.includes]
        index = cindex.Index.create()
        self.tu = index.parse(source, includes + ["-x", "c++", "-std=c++11", "-ferror-limit=0", "-D__CODE_GENERATOR__"])
        for diag in self.tu.diagnostics:
            #
            # We expect to be run over hundreds of files. Any parsing issues are likely to be very repetitive.
            # So, to avoid bothering the user, we suppress duplicates.
            #
            loc = diag.location
            msg = "{}:{}[{}] {}".format(loc.file, loc.line, loc.column, diag.spelling)
            if msg in self.diagnostics:
                continue
            self.diagnostics.add(msg)
            #
            # Downgrade severities a little to avoid scaring the user.
            #
            severity = 10 + diag.severity * 10
            severity -= 10
            if severity < 0:
                severity = 0
            logger.log(severity, "Parse error {}".format(msg))
        if self.dump_includes:
            for include in includes:
                logger.debug(_("Using includes from {}").format(include))
            for include in sorted(set(self.tu.get_includes())):
                logger.debug(_("Used includes {}").format(include.include.name))
        #
        # Run through the top level children in the translation unit.
        #
        h_file = os.path.basename(self.tu.spelling)
        sip_file = os.path.splitext(h_file)[0] + ".sip"
        body = []
        for child in self.tu.cursor.get_children():
            if child.location.file.name != source:
                continue
            #
            # Add entries we know about.
            #
            if child.kind in [CursorKind.CLASS_DECL, CursorKind.NAMESPACE]:
                body.append(self._process_container(child, h_file))
            else:
                logger.debug("Ignoring child {} {}".format(child.kind.name, child.displayname or child.spelling))
                continue
        #
        # Generate a file header.
        #
        now = datetime.datetime.utcnow()
        header = """//
// Copyright (c) {} by Shaheed Haque (srhaque@theiet.org)
//
// This file, {}, derived from {}, is part of PyKDE5.
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
//
""".format(now.year, sip_file, self.tu.spelling)
        return body, header, sip_file

    def _process_container(self, container, h_file="", level=0):
        """
        Recursive walk of a class or namespace.
        
        :param container:           A class or namespace.
        :param h_file:              Name of header file being processed.
        :param level:               Recursion level controls indentation.
        :return:                    A string.
        """
        name = container.spelling
        if container.access_specifier == AccessSpecifier.PRIVATE:
            logger.debug("Ignoring private {} {}".format(container.kind, name))
            return ""
        body = ""
        for member in container.get_children():
            if member.access_specifier == AccessSpecifier.PRIVATE:
                logger.debug("Ignoring private {} {}::{}".format(member.kind, name, member.displayname))
                continue
            if member.kind in [CursorKind.CXX_METHOD, CursorKind.FUNCTION_DECL]:
                keywords = self._fn_get_keywords(member)
                parameters = self._fn_get_parameters(container, member)
                decl = "{} {}({}){}".format(member.result_type.spelling, member.spelling, parameters, keywords)
                decl = rules.apply_function_rules(container, member, decl)
                if decl:
                    body += "    {};\n".format(decl)
            elif member.kind in [CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR]:
                parameters = self._fn_get_parameters(container, member)
                decl = "{}({})".format(member.spelling, parameters)
                decl = rules.apply_function_rules(container, member, decl)
                if decl:
                    body += "    {};\n".format(decl)
            elif member.kind == CursorKind.ENUM_DECL:
                body += "    enum {}\n{{\n".format(member.displayname)
                enumerations = []
                for enum in member.get_children():
                    enumerations.append("        {}".format(enum.displayname))
                    assert enum.kind == CursorKind.ENUM_CONSTANT_DECL
                body += ",\n".join(enumerations)
                body += "\n    };\n"
            elif member.kind == CursorKind.CXX_ACCESS_SPEC_DECL:
                access_specifier = self._get_access_specifier(member)
                if access_specifier:
                    body += "{}\n".format(access_specifier)
            elif member.kind == CursorKind.TYPEDEF_DECL:
                alias, definition = self._typedef_get(container, member)
                body += "    typedef {} {}:\n".format(definition, alias)
            elif member.kind == CursorKind.CLASS_DECL:
                body += self._process_container(member, level=level + 1)
            else:
                logger.debug("Ignorning unsupported {} {}::{}".format(member.kind, name, member.displayname))
        if body:
            bases = [m.type.spelling for m in container.get_children() if m.kind == CursorKind.CXX_BASE_SPECIFIER]
            if bases:
                bases = ": " + (", ".join(bases))
            else:
                bases = ""
            if h_file:
                h_file = """%TypeHeaderCode
#include <{}>
%End
""".format(h_file)
            body = """class {}{}
{{
{}{}}};
""".format(name, bases, h_file, body)
            #
            # Apply indentation.
            #
            if level:
                pad = " " * (level * 4)
                lines = body.split("\n")
                lines = [pad + line for line in lines]
                body = "\n".join(lines)
        return body

    def _get_access_specifier(self, member):
        """
        In principle, we just want member.access_specifier.name.lower(), except that we need to handle:

          Q_OBJECT
          Q_SIGNALS:|signals:
          public|private|protected Q_SLOTS:|slots:

        which are converted by the preprocessor...so read the original text.

        :param member:                  The access_specifier.
        :return:
        """
        access_specifier = self._read_source(member.extent)
        assert len(access_specifier) == 1
        access_specifier = access_specifier[0]
        if access_specifier == "Q_OBJECT":
            access_specifier = "public:"
        elif access_specifier == "Q_SIGNALS:":
            access_specifier = "signals:"
        elif access_specifier.endswith("slots:") or access_specifier.endswith("Q_SLOTS:"):
            access_specifier = access_specifier.split()[0] + ":"
        return access_specifier

    def _typedef_get(self, container, typedef):
        alias = typedef.displayname
        template = ""
        args = []
        for child in typedef.get_children():
            if child.kind == CursorKind.TEMPLATE_REF:
                template = child.displayname
            elif child.kind == CursorKind.TYPE_REF:
                args.append(child.displayname)
            else:
                logger.debug("Ignorning unsupported {} {}".format(child.kind, child.spelling))
        body = "{}<{}>".format(template, ", ".join(args))
        return alias, body

    def _fn_get_keywords(self, function):
        """
        The parser does not seem to provide access to the complete keywords (const, static, etc) of a function.
        """
        text = ""
        bracket_level = 0
        found_end = False
        was_punctuated = True
        for token in self.tu.get_tokens(extent=function.extent):
            if bracket_level <= 0 and token.spelling == ";":
                found_end = True
                break
            elif token.spelling == "(":
                was_punctuated = True
                bracket_level += 1
                text += token.spelling
            elif token.spelling == ")":
                was_punctuated = True
                bracket_level -= 1
                text += token.spelling
            elif token.kind == TokenKind.PUNCTUATION:
                was_punctuated = True
                text += token.spelling
            else:
                if not was_punctuated:
                    text += " "
                text += token.spelling
                was_punctuated = False
        if not found_end:
            RuntimeError(_("No end found for {}, '{}'").format(function.spelling, text))
        text = text.split(function.displayname)
        if len(text) > 1:
            text = " " + text[-1]
        else:
            text = ""
        return text

    def _fn_get_parameters(self, container, function):
        """
        Find the parameters for a function.

        :param container:
        :param function:
        :return:
        """
        parameters = []
        for mc in function.get_children():
            if mc.kind == CursorKind.PARM_DECL:
                parameter = mc.displayname or "__{}".format(len(parameters))
                #
                # So far so good, but we need any default value.
                #
                decl = "{} {}".format(mc.type.spelling, parameter)
                init = self._fn_get_parameter_default(function, mc)
                decl, init = rules.apply_param_rules(container, function, parameter, decl, init)
                if init:
                    decl += " = " + init
                parameters.append(decl)
            else:
                logger.debug("Ignoring non-param {} {}".format(mc.kind, mc.displayname))
                continue

        parameters = ", ".join(parameters)
        return parameters

    def _fn_get_parameter_default(self, function, parameter):
        """
        The parser does not seem to provide access to the complete text of a parameter.
        This makes it hard to find any default values, so we:

            1. Run the lexer from "here" to the end of the file, bailing out when we see the ","
            or a ")" marking the end.
            2. Watch for the assignment.
        """
        possible_extent = SourceRange.from_locations(parameter.extent.start, function.extent.end)
        text = ""
        bracket_level = 0
        found_end = False
        was_punctuated = True
        default_value = None
        for token in self.tu.get_tokens(extent=possible_extent):
            if bracket_level <= 0 and token.spelling in [",", ")", ";"]:
                found_end = True
                break
            elif token.spelling == "(":
                was_punctuated = True
                bracket_level += 1
                text += token.spelling
            elif token.spelling == ")":
                was_punctuated = True
                bracket_level -= 1
                text += token.spelling
            elif token.kind == TokenKind.PUNCTUATION:
                was_punctuated = True
                text += token.spelling
                if token.spelling == "=" and default_value is None:
                    default_value = len(text)
            else:
                if not was_punctuated:
                    text += " "
                text += token.spelling
                was_punctuated = False
        if not found_end and text:
            RuntimeError(_("No end found for {}::{}, '{}'").format(function.spelling, parameter.spelling, text))
        if default_value:
            return text[default_value:]
        else:
            return ""

    def _read_source(self, extent):
        """
        Read the given range from the unpre-processed source.

        :param extent:              The range of text required.
        """
        extract = self.unpreprocessed_source[extent.start.line - 1:extent.end.line]
        if extent.start.line == extent.end.line:
            extract[0] = extract[0][extent.start.column - 1:extent.end.column - 1]
        else:
            extract[0] = extract[0][extent.start.column - 1:]
            extract[-1] = extract[-1][:extent.end.column - 1]
        return extract

    @staticmethod
    def _find_libclang():
        """"
        Find the libclang.so to alow us to initialise the system.
        """
        if not Generator._libclang:
            lines = subprocess.check_output(["/sbin/ldconfig", "-p"])
            for line in lines.split("\n"):
                fields = line.split()
                if fields and fields[0].startswith("libclang.so"):
                    Generator._libclang = fields[-1]
                    logger.debug(_("Found libclang at {}").format(Generator._libclang))
        if Generator._libclang:
            if not cindex.Config.loaded:
                cindex.Config.set_library_file(Generator._libclang)
        else:
            raise RuntimeError(_("Cannot find libclang"))


def main(argv=None):
    """
    Take a single KDE header file and generate the corresponding SIP file.

    Examples:

        generator.py /usr/include/KF5/KItemModels/kselectionproxymodel.h
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(epilog=inspect.getdoc(main),
                                     formatter_class=HelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help=_("Enable verbose output"))
    parser.add_argument("--kde-includes", default="/usr/include/KF5", help=_("Root of KDE header paths"))
    parser.add_argument("--qt-includes", default="/usr/include/x86_64-linux-gnu/qt5", help=_("Root of Qt header paths"))
    parser.add_argument("source", help=_("File to process"))
    try:
        args = parser.parse_args(argv[1:])
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        #
        # Generate!
        #
        g = Generator(args.qt_includes, args.kde_includes)
        body, header, sip_file = g.create_sip(args.source)
        print(header)
        for r in body:
            print(r)
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
