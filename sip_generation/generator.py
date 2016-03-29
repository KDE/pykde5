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
import re
import subprocess
import sys
import traceback
from clang import cindex
from clang.cindex import AccessSpecifier, CursorKind, SourceRange, StorageClass, TokenKind

from rules import rule_set


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


EXPR_KINDS = [
        CursorKind.UNEXPOSED_EXPR, CursorKind.UNARY_OPERATOR, CursorKind.BINARY_OPERATOR,
        CursorKind.INTEGER_LITERAL, CursorKind.FLOATING_LITERAL, CursorKind.STRING_LITERAL,
        CursorKind.CXX_BOOL_LITERAL_EXPR
    ]
TEMPLATE_KINDS = [
        CursorKind.TYPE_REF, CursorKind.TEMPLATE_REF, CursorKind.NAMESPACE_REF
    ] + EXPR_KINDS


class Generator(object):
    _libclang = None

    def __init__(self, qt_includes, kde_includes, dump_includes=False, dump_privates=False):
        """
        Constructor.

        :param qt_includes:         The root for all Qt include files.
        :param kde_includes:        The root for all KDE include files.
        :param dump_includes:       Turn on diagnostics for include files.
        :param dump_privates:       Turn on diagnostics for omitted private items.
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
        self.dump_privates = dump_privates
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
        body = self._container_get(self.tu.cursor, -1, h_file)
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

    CONTAINER_SKIPPABLE_UNEXPOSED_DECL = re.compile("(_DECLARE_PRIVATE|friend)\W")

    def _container_get(self, container, level, h_file):
        """
        Recursive walk of a class or namespace.
        
        :param container:           A class or namespace.
        :param h_file:              Name of header file being processed.
        :param level:               Recursion level controls indentation.
        :return:                    A string.
        """
        def skippable_unexposed_decl(member):
            text = self._read_source(member.extent)
            if Generator.CONTAINER_SKIPPABLE_UNEXPOSED_DECL.search(text):
                return True
            logger.debug(_("Ignoring {} child {}[{}]::{} {}").format(container.kind, container.spelling,
                                                                     member.extent.start.line, text, member.kind))

        def skippable_visibility_attr(member):
            text = self._read_source(member.extent)
            if text.endswith("_EXPORT"):
                return True
            logger.debug(_("Ignoring {} child {}[{}]::{} {}").format(container.kind, container.spelling,
                                                                     member.extent.start.line, text, member.kind))

        name = container.displayname
        if container.access_specifier == AccessSpecifier.PRIVATE:
            if self.dump_privates:
                logger.debug("Ignoring private {} {}".format(container.kind, name))
            return ""
        setattr(container, "sip_annotations", [])
        body = ""
        base_specifiers = []
        template_type_parameters = []
        for member in container.get_children():
            #
            # Only emit items in the translation unit.
            #
            if member.location.file.name != self.tu.spelling:
                continue
            if member.access_specifier == AccessSpecifier.PRIVATE:
                if self.dump_privates:
                    logger.debug("Ignoring private {}::{} {}".format(name, member.displayname, member.kind))
                continue
            decl = ""
            if member.kind in [CursorKind.CXX_METHOD, CursorKind.FUNCTION_DECL, CursorKind.FUNCTION_TEMPLATE,
                               CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR, CursorKind.CONVERSION_FUNCTION]:
                decl = self._fn_get(container, member, level + 1)
            elif member.kind == CursorKind.ENUM_DECL:
                decl = self._enum_get(container, member, level + 1)
            elif member.kind == CursorKind.CXX_ACCESS_SPEC_DECL:
                decl = self._get_access_specifier(member, level + 1)
            elif member.kind == CursorKind.TYPEDEF_DECL:
                decl = self._typedef_get(container, member, level + 1)
            elif member.kind == CursorKind.CXX_BASE_SPECIFIER:
                base_specifiers.append(member.displayname)
            elif member.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
                template_type_parameters.append("typename " + member.displayname)
            elif member.kind in [CursorKind.VAR_DECL, CursorKind.FIELD_DECL]:
                decl = self._var_get(container, member, level + 1)
            elif member.kind in [CursorKind.NAMESPACE, CursorKind.CLASS_DECL, CursorKind.CLASS_TEMPLATE, CursorKind.STRUCT_DECL]:
                decl = self._container_get(member, level + 1, h_file)
            elif member.kind == CursorKind.UNEXPOSED_ATTR and self._read_source(member.extent).find("_DEPRECATED") != -1:
                #
                # We don't seem to have access to the __attribute__(())s, but at least we can look for stuff we care about.
                #
                container.sip_annotations.append("Deprecated")
            elif member.kind in TEMPLATE_KINDS:
                #
                # Ignore:
                #
                #   TEMPLATE_KINDS: Template type parameter.
                #
                pass
            elif member.kind == CursorKind.VISIBILITY_ATTR and skippable_visibility_attr(member):
                pass
            elif member.kind == CursorKind.UNEXPOSED_DECL and skippable_unexposed_decl(member):
                pass
            else:
                Generator._report_ignoring(container, member)
            if decl:
                body += decl
        #
        # Empty containers are still useful if they provide namespaces.
        #
        if not body:
            text = self._read_source(container.extent)
            if text.endswith("}"):
                body = "\n"
        if body:
            pad = " " * (level * 4)
            if container.kind == CursorKind.CLASS_TEMPLATE or name.endswith(">"):
                template_type_parameters = pad + "template <" + (", ".join(template_type_parameters)) + ">\n"
            else:
                template_type_parameters = ""
            if base_specifiers:
                base_specifiers = ": " + (", ".join(base_specifiers))
            else:
                base_specifiers = ""
            if level >= 0:
                #
                # There does not seem to be an obvious way to tell a class from a struct. That should matter...
                #
                if container.kind == CursorKind.NAMESPACE:
                    container_type = pad + "namespace"
                else:
                    container_type = pad + "class"
                if level == 0:
                    h_file = "%TypeHeaderCode\n#include <{}>\n%End\n".format(h_file)
                else:
                    h_file = ""
                prefix = "{}{} {}{}\n{}{{\n{}".format(template_type_parameters, container_type, name, base_specifiers, pad, h_file)
                if container.sip_annotations:
                    suffix = "} /" + ",".join(container.sip_annotations) + "/;\n"
                else:
                    suffix = "};\n"
                body = prefix + body + pad + suffix
        return body

    def _get_access_specifier(self, member, level):
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
        if access_specifier == "Q_OBJECT":
            access_specifier = "public:"
        elif access_specifier == "Q_SIGNALS:":
            access_specifier = "signals:"
        elif access_specifier.endswith("slots:") or access_specifier.endswith("Q_SLOTS:"):
            access_specifier = access_specifier.split()[0] + ":"
        pad = " " * ((level - 1) * 4)
        decl = pad + access_specifier + "\n"
        return decl

    def _enum_get(self, container, enum, level):
        pad = " " * (level * 4)
        decl = pad + "enum {} {{\n".format(enum.displayname)
        enumerations = []
        for enum in enum.get_children():
            enumerations.append(pad + "    {}".format(enum.displayname))
            assert enum.kind == CursorKind.ENUM_CONSTANT_DECL
        decl += ",\n".join(enumerations) + "\n"
        decl += pad + "};\n"
        return decl

    def _fn_get(self, container, function, level):
        """
        Walk of a function.

        :param container:           A class or namespace.
        :param function:            The function object.
        :param level:               Recursion level controls indentation.
        :return:                    A string.
        """
        def skippable_visibility_attr(member):
            text = self._read_source(member.extent)
            if text.endswith("_EXPORT"):
                return True
            logger.debug(_("Ignoring {} child {}[{}]::{} {}").format(function.kind, function.spelling,
                                                                     member.extent.start.line, text, member.kind))

        pad = " " * (level * 4)
        setattr(function, "sip_annotations", [])
        parameters = []
        template_type_parameters = []
        for child in function.get_children():
            if child.kind == CursorKind.PARM_DECL:
                parameter = child.displayname or "__{}".format(len(parameters))
                #
                # So far so good, but we need any default value.
                #
                decl = "{} {}".format(child.type.spelling, parameter)
                init = self._fn_get_parameter_default(function, child)
                setattr(child, "sip_annotations", [])
                decl, init = rule_set.param_rules().apply(container, function, child, decl, init)
                if child.sip_annotations:
                    decl += " /" + ",".join(child.sip_annotations) + "/"
                if init:
                    decl += " = " + init
                parameters.append(decl)
            elif child.kind in [CursorKind.COMPOUND_STMT, CursorKind.CXX_OVERRIDE_ATTR, CursorKind.MEMBER_REF] + TEMPLATE_KINDS:
                #
                # Ignore:
                #
                #   CursorKind.COMPOUND_STMT: Function body.
                #   CursorKind.CXX_OVERRIDE_ATTR: The "override" keyword.
                #   CursorKind.MEMBER_REF: Constructor initialisers.
                #   TEMPLATE_KINDS: The result type.
                #
                pass
            elif child.kind == CursorKind.UNEXPOSED_ATTR and self._read_source(child.extent).find("_DEPRECATED") != -1:
                #
                # We don't seem to have access to the __attribute__(())s, but at least we can look for stuff we care about.
                #
                function.sip_annotations.append("Deprecated")
            elif child.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
                template_type_parameters.append("typename " + child.displayname)
            elif child.kind == CursorKind.TEMPLATE_TEMPLATE_PARAMETER:
                template_type_parameters.append(self._template_template_param_get(child))
            elif child.kind == CursorKind.VISIBILITY_ATTR and skippable_visibility_attr(child):
                pass
            else:
                Generator._report_ignoring(function, child)
        parameters = ", ".join(parameters)
        if function.kind in [CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR]:
            decl = "{}({})".format(function.spelling, parameters)
        else:
            decl = "{} {}({})".format(function.result_type.spelling, function.spelling, parameters)
        decl = decl.replace("* ", "*").replace("& ", "&")
        decl = rule_set.fn_rules().apply(container, function, decl)
        #
        # Now the rules have run, add any prefix/suffix.
        #
        if decl:
            if function.kind == CursorKind.FUNCTION_TEMPLATE:
                template_type_parameters = pad + "template <" + (", ".join(template_type_parameters)) + ">\n"
            else:
                template_type_parameters = ""
            prefix, suffix = self._fn_get_keywords(function)
            decl = prefix + decl + suffix
            if function.sip_annotations:
                decl += " /" + ",".join(function.sip_annotations) + "/"
            decl = template_type_parameters + pad + decl + ";\n"
        return decl

    def _template_template_param_get(self, container):
        """
        Recursive template template parameter walk.

        :param container:                   The template template object.
        :return:                            String containing the template template parameter.
        """
        template_type_parameters = []
        for member in container.get_children():
            if member.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
                template_type_parameters.append("typename")
            elif child.kind == CursorKind.TEMPLATE_TEMPLATE_PARAMETER:
                template_type_parameters.append(self._template_template_param_get(member))
            else:
                Generator._report_ignoring(container, child)
        template_type_parameters = "template <" + (", ".join(template_type_parameters)) + "> class " + container.displayname
        return template_type_parameters

    def _fn_get_keywords(self, function):
        """
        The parser does not provide direct access to the complete keywords (explicit, const, static, etc) of a function
        in the displayname. It would be nice to get these from the AST, but I cannot find where they are hiding.

        Now, we could resort to using the original source. That does not bode well if you have macros (QOBJECT,
        xxxDEPRECATED?), inlined bodies and the like, using the rule engine could be used to patch corner cases...

        ...or we can try to guess what SIP cares about, i.e static and maybe const. Luckily (?), we have those to hand!

        :param function:                    The function object.
        :return: prefix, suffix             String containing any prefix or suffix keywords.
        """
        if function.is_const_method():
            suffix = " const"
        else:
            suffix = ""
        if function.is_static_method():
            prefix = "static "
        else:
            prefix = ""
        return prefix, suffix

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

    def _typedef_get(self, container, typedef, level):
        pad = " " * (level * 4)
        alias = typedef.displayname
        template = ""
        args = []
        for child in typedef.get_children():
            if child.kind == CursorKind.TEMPLATE_REF:
                template = child.displayname
            elif child.kind == CursorKind.TYPE_REF:
                args.append(child.displayname)
            else:
                Generator._report_ignoring(typedef, child)
        if template:
            decl = pad + "typedef {}<{}> {};\n".format(template, ", ".join(args), alias)
        else:
            decl = pad + "typedef {} {};\n".format("::".join(args), alias)
        return decl

    def _var_get(self, container, variable, level):
        """
        Walk of a variable.

        :param container:           A class or namespace.
        :param variable:            The variable object.
        :param level:               Recursion level controls indentation.
        :return:                    A string.
        """
        pad = " " * (level * 4)
        setattr(variable, "sip_annotations", [])
        template_type_parameters = []
        for child in variable.get_children():
            if child.kind in TEMPLATE_KINDS:
                #
                # Ignore:
                #
                #   TEMPLATE_KINDS: The variable type.
                #
                pass
            else:
                Generator._report_ignoring(variable, child)
        decl = "{} {}".format(variable.type.spelling, variable.spelling)
        decl = decl.replace("* ", "*").replace("& ", "&")
        decl = rule_set.var_rules().apply(container, variable, decl)
        #
        # Now the rules have run, add any prefix/suffix.
        #
        if decl:
            prefix = self._var_get_keywords(variable)
            decl = prefix + decl
            if variable.sip_annotations:
                decl += " /" + ",".join(variable.sip_annotations) + "/"
            decl = pad + decl + ";\n"
        return decl

    def _var_get_keywords(self, variable):
        """
        The parser does not provide direct access to the complete keywords (static, etc) of a variable
        in the displayname. It would be nice to get these from the AST, but I cannot find where they are hiding.

        :param variable:                    The variable object.
        :return: prefix                     String containing any prefix keywords.
        """
        if variable.storage_class == StorageClass.STATIC:
            prefix = "static "
        else:
            prefix = ""
        return prefix

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
        #
        # Return a single line of text.
        #
        return "".join(extract).replace("\n", " ")

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

    @staticmethod
    def _report_ignoring(parent, child):
        child_id = child.displayname or child.spelling
        logger.debug(_("Ignoring {} child {}[{}]::{} {}").format(parent.kind, parent.spelling, child.extent.start.line,
                                                                 child_id, child.kind))


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
        if body:
            print(header)
            print(body)
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
