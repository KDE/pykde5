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
import gettext
import inspect
import logging
import os
import re
import subprocess
import sys
import traceback
from clang import cindex
from clang.cindex import AccessSpecifier, CursorKind, SourceRange, StorageClass, TokenKind, TypeKind


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
    CursorKind.UNEXPOSED_EXPR,
    CursorKind.CONDITIONAL_OPERATOR, CursorKind.UNARY_OPERATOR, CursorKind.BINARY_OPERATOR,
    CursorKind.INTEGER_LITERAL, CursorKind.FLOATING_LITERAL, CursorKind.STRING_LITERAL,
    CursorKind.CXX_BOOL_LITERAL_EXPR, CursorKind.CXX_STATIC_CAST_EXPR, CursorKind.DECL_REF_EXPR
]
TEMPLATE_KINDS = [
                     CursorKind.TYPE_REF, CursorKind.TEMPLATE_REF, CursorKind.NAMESPACE_REF
                 ] + EXPR_KINDS


class SipGenerator(object):
    _libclang = None

    def __init__(self, includes, project_name, project_rules, dump_includes=False, dump_privates=False):
        """
        Constructor.

        :param includes:            A list of roots of includes file, typically including the root for all Qt and
                                    the root for all KDE include files as well as any project-specific include files.
        :param project_name:        The name of the project.
        :param project_rules:       The rules file for the project.
        :param dump_includes:       Turn on diagnostics for include files.
        :param dump_privates:       Turn on diagnostics for omitted private items.
        """
        SipGenerator._find_libclang()
        self.exploded_includes = set(includes)
        for include_root in includes:
            walk_directories(include_root, lambda d: self.exploded_includes.add(d))
        if dump_includes:
            for include in sorted(self.exploded_includes):
                logger.debug(_("Using includes from {}").format(include))
        self.project_name = project_name
        try:
            import imp
            imp.load_source("project_rules", project_rules)
        except ImportError:
            import importlib
            spec = importlib.util.spec_from_file_location("project_rules", project_rules)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        #
        # Statically prepare the rule logic. This takes the rules provided by the user and turns them into code.
        #
        self.rule_set = getattr(sys.modules["project_rules"], "RuleSet")()
        self.dump_includes = dump_includes
        self.dump_privates = dump_privates
        self.diagnostics = set()
        self.tu = None
        self.unpreprocessed_source = None

    @staticmethod
    def describe(cursor, text=None):
        if not text:
            text = cursor.spelling
        return "{} on line {} '{}'".format(cursor.kind.name, cursor.extent.start.line, text)

    def create_sip(self, root, h_file):
        """
        Actually convert the given source header file into its SIP equivalent.

        :param root:                The root of the source tree.
        :param h_file:              Add this suffix to the root to find the source (header) file of interest.
        """
        #
        # Read in the original file.
        #
        source = os.path.join(root, h_file)
        self.unpreprocessed_source = []
        with open(source, "rU") as f:
            for line in f:
                self.unpreprocessed_source.append(line)
        #
        # Create and populate the index. To run the actual compiler in proprocess-only mode:
        #
        # ["clang-3.9"] + includes + ["-x", "c++", "-std=c++11", "-ferror-limit=0", "-D__CODE_GENERATOR__", "-E"] + [source]
        #
        includes = ["-I" + i for i in self.exploded_includes]
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
        body = self._container_get(self.tu.cursor, -1, h_file)
        return body, self.tu.get_includes

    CONTAINER_SKIPPABLE_UNEXPOSED_DECL = re.compile("_DECLARE_PRIVATE|friend|;")
    CONTAINER_SKIPPABLE_ATTR = re.compile("_EXPORT")
    FN_SKIPPABLE_ATTR = re.compile("_EXPORT|Q_REQUIRED_RESULT|format\(printf")
    VAR_SKIPPABLE_ATTR = re.compile("_EXPORT")
    TYPEDEF_SKIPPABLE_ATTR = re.compile("_EXPORT")

    def _container_get(self, container, level, h_file):
        """
        Generate the (recursive) translation for a class or namespace.

        :param container:           A class or namespace.
        :param h_file:              Name of header file being processed.
        :param level:               Recursion level controls indentation.
        :return:                    A string.
        """

        def skippable_attribute(member, text):
            """
            We don't seem to have access to the __attribute__(())s, but at least we can look for stuff we care about.

            :param member:          The attribute.
            :param text:            The raw source corresponding to the region of member.
            """
            if text.find("_DEPRECATED") != -1:
                sip["annotations"].add("Deprecated")
                return True
            if SipGenerator.CONTAINER_SKIPPABLE_ATTR.search(text):
                return True
            SipGenerator._report_ignoring(container, member, text)

        sip = {
            "name": container.displayname,
            "annotations": set()
        }
        name = container.displayname
        if container.access_specifier == AccessSpecifier.PRIVATE:
            if self.dump_privates:
                logger.debug("Ignoring private {}".format(SipGenerator.describe(container)))
            return ""
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
                    logger.debug("Ignoring private {}".format(SipGenerator.describe(member)))
                continue
            decl = ""
            if member.kind in [CursorKind.CXX_METHOD, CursorKind.FUNCTION_DECL, CursorKind.FUNCTION_TEMPLATE,
                               CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR, CursorKind.CONVERSION_FUNCTION]:
                decl = self._fn_get(container, member, level + 1)
            elif member.kind == CursorKind.ENUM_DECL:
                decl = self._enum_get(container, member, level + 1) + ";\n"
            elif member.kind == CursorKind.CXX_ACCESS_SPEC_DECL:
                decl = self._get_access_specifier(member, level + 1)
            elif member.kind == CursorKind.TYPEDEF_DECL:
                decl = self._typedef_get(container, member, level + 1)
            elif member.kind == CursorKind.CXX_BASE_SPECIFIER:
                #
                # Strip off the leading "class". Except for TypeKind.UNEXPOSED...
                #
                base_specifiers.append(member.displayname.split(None, 2)[-1])
            elif member.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
                template_type_parameters.append(member.displayname)
            elif member.kind == CursorKind.TEMPLATE_NON_TYPE_PARAMETER:
                template_type_parameters.append(member.type.spelling + " " + member.displayname)
            elif member.kind in [CursorKind.VAR_DECL, CursorKind.FIELD_DECL]:
                decl = self._var_get(container, member, level + 1)
            elif member.kind in [CursorKind.NAMESPACE, CursorKind.CLASS_DECL,
                                 CursorKind.CLASS_TEMPLATE, CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION,
                                 CursorKind.STRUCT_DECL, CursorKind.UNION_DECL]:
                decl = self._container_get(member, level + 1, h_file)
            elif member.kind in TEMPLATE_KINDS + [CursorKind.USING_DECLARATION, CursorKind.USING_DIRECTIVE,
                                                  CursorKind.CXX_FINAL_ATTR]:
                #
                # Ignore:
                #
                #   TEMPLATE_KINDS: Template type parameter.
                #   CursorKind.USING_DECLARATION, CursorKind.USING_DIRECTIVE: Using? Pah!
                #   CursorKind.CXX_FINAL_ATTR: Again, not much to be done with this.
                #
                pass
            else:
                text = self._read_source(member.extent)
                if member.kind in [CursorKind.UNEXPOSED_ATTR, CursorKind.VISIBILITY_ATTR] and skippable_attribute(
                        member, text):
                    pass
                elif member.kind == CursorKind.UNEXPOSED_DECL:
                    if SipGenerator.CONTAINER_SKIPPABLE_UNEXPOSED_DECL.search(text):
                        pass
                    else:
                        decl = self._unexposed_decl_get(container, member)
                else:
                    SipGenerator._report_ignoring(container, member)
            if decl:
                body += decl
        #
        # Empty containers are still useful if they provide namespaces.
        #
        if not body:
            text = self._read_source(container.extent)
            if text.endswith("}"):
                body = "\n"
        if body and level >= 0:
            #
            # There does not seem to be an obvious way to tell a class from a struct. That should matter...
            #
            if container.kind == CursorKind.NAMESPACE:
                container_type = "namespace " + name
            elif container.kind in [CursorKind.CLASS_DECL, CursorKind.CLASS_TEMPLATE,
                                    CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION]:
                container_type = "class " + name
            elif container.kind == CursorKind.STRUCT_DECL:
                container_type = "struct {}".format(name or "__struct{}".format(container.extent.start.line))
            elif container.kind == CursorKind.UNION_DECL:
                container_type = "union {}".format(name or "__union{}".format(container.extent.start.line))
            else:
                raise AssertionError(
                    _("Unexpected container {}: {}[{}]").format(container.kind, name, container.extent.start.line))
            #
            # Flesh out the SIP context for the rules engine.
            #
            sip["template_parameters"] = ", ".join(template_type_parameters)
            sip["decl"] = container_type
            sip["base_specifiers"] = ", ".join(base_specifiers)
            sip["body"] = body
            self.rule_set.container_rules().apply(container, sip)
            pad = " " * (level * 4)
            if sip["name"]:
                decl = pad + sip["decl"]
                if sip["base_specifiers"]:
                    decl += ": " + sip["base_specifiers"]
                if sip["annotations"]:
                    decl += " /" + ",".join(sip["annotations"]) + "/"
                if sip["template_parameters"]:
                    decl = pad + "template <" + sip["template_parameters"] + ">\n" + decl
                decl += "\n" + pad + "{\n"
                if level == 0:
                    decl += "%TypeHeaderCode\n#include <{}>\n%End\n".format(h_file)
                body = decl + sip["body"] + pad + "};\n"
            else:
                body = pad + "// Discarded {}\n".format(SipGenerator.describe(container))
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
        if access_specifier == "Q_SIGNALS:":
            access_specifier = "signals:"
        elif access_specifier.endswith("slots:") or access_specifier.endswith("Q_SLOTS:"):
            access_specifier = access_specifier.split()[0] + ":"
        elif access_specifier.startswith("Q_"):
            access_specifier = "public:"
        pad = " " * ((level - 1) * 4)
        decl = pad + access_specifier + "\n"
        return decl

    def _enum_get(self, container, enum, level):
        pad = " " * (level * 4)
        decl = pad + "enum {} {{\n".format(enum.displayname or "__enum{}".format(enum.extent.start.line))
        enumerations = []
        for enum in enum.get_children():
            enumerations.append(pad + "    {}".format(enum.displayname))
            assert enum.kind == CursorKind.ENUM_CONSTANT_DECL
        decl += ",\n".join(enumerations) + "\n"
        decl += pad + "}"
        return decl

    def _fn_get(self, container, function, level):
        """
        Generate the translation for a function.

        :param container:           A class or namespace.
        :param function:            The function object.
        :param level:               Recursion level controls indentation.
        :return:                    A string.
        """

        def skippable_attribute(member, text):
            """
            We don't seem to have access to the __attribute__(())s, but at least we can look for stuff we care about.

            :param member:          The attribute.
            :param text:            The raw source corresponding to the region of member.
            """
            if text.find("_DEPRECATED") != -1:
                sip["annotations"].add("Deprecated")
                return True
            if SipGenerator.FN_SKIPPABLE_ATTR.search(text):
                return True
            SipGenerator._report_ignoring(function, member, text)

        sip = {
            "name": function.spelling,
            "annotations": set()
        }
        parameters = []
        template_type_parameters = []
        for child in function.get_children():
            if child.kind == CursorKind.PARM_DECL:
                parameter = child.displayname or "__{}".format(len(parameters))
                #
                # So far so good, but we need any default value.
                #
                child_sip = {
                    "name": parameter,
                    "decl": "{} {}".format(child.type.spelling, parameter),
                    "init": self._fn_get_parameter_default(function, child),
                    "annotations": set()
                }
                self.rule_set.param_rules().apply(container, function, child, child_sip)
                decl = child_sip["decl"]
                if child_sip["annotations"]:
                    decl += " /" + ",".join(child_sip["annotations"]) + "/"
                if child_sip["init"]:
                    decl += " = " + child_sip["init"]
                parameters.append(decl)
            elif child.kind in [CursorKind.COMPOUND_STMT, CursorKind.CXX_OVERRIDE_ATTR,
                                CursorKind.MEMBER_REF, CursorKind.DECL_REF_EXPR, CursorKind.CALL_EXPR] + TEMPLATE_KINDS:
                #
                # Ignore:
                #
                #   CursorKind.COMPOUND_STMT: Function body.
                #   CursorKind.CXX_OVERRIDE_ATTR: The "override" keyword.
                #   CursorKind.MEMBER_REF, CursorKind.DECL_REF_EXPR, CursorKind.CALL_EXPR: Constructor initialisers.
                #   TEMPLATE_KINDS: The result type.
                #
                pass
            elif child.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
                template_type_parameters.append(child.displayname)
            elif child.kind == CursorKind.TEMPLATE_NON_TYPE_PARAMETER:
                template_type_parameters.append(child.type.spelling + " " + child.displayname)
            elif child.kind == CursorKind.TEMPLATE_TEMPLATE_PARAMETER:
                template_type_parameters.append(self._template_template_param_get(child))
            else:
                text = self._read_source(child.extent)
                if child.kind in [CursorKind.UNEXPOSED_ATTR, CursorKind.VISIBILITY_ATTR] and skippable_attribute(child,
                                                                                                                 text):
                    pass
                else:
                    SipGenerator._report_ignoring(function, child)
        #
        # Flesh out the SIP context for the rules engine.
        #
        sip["template_parameters"] = ", ".join(template_type_parameters)
        if function.kind in [CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR]:
            sip["fn_result"] = ""
        else:
            sip["fn_result"] = function.result_type.spelling
        decl = ", ".join(parameters)
        decl = decl.replace("* ", "*").replace("& ", "&")
        sip["decl"] = decl
        self.rule_set.function_rules().apply(container, function, sip)
        #
        # Now the rules have run, add any prefix/suffix.
        #
        pad = " " * (level * 4)
        if sip["name"]:
            prefix, suffix = self._fn_get_keywords(function)
            decl = sip["name"] + "(" + sip["decl"] + ")"
            if sip["fn_result"]:
                if sip["fn_result"][-1] in "*&":
                    decl = sip["fn_result"] + decl
                else:
                    decl = sip["fn_result"] + " " + decl
            decl = pad + prefix + decl + suffix
            if sip["annotations"]:
                decl += " /" + ",".join(sip["annotations"]) + "/"
            if sip["template_parameters"]:
                decl = pad + "template <" + sip["template_parameters"] + ">\n" + decl
            decl += ";\n"
        else:
            decl = pad + "// Discarded {}\n".format(SipGenerator.describe(function))
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
            elif member.kind == CursorKind.TEMPLATE_TEMPLATE_PARAMETER:
                template_type_parameters.append(self._template_template_param_get(member))
            else:
                SipGenerator._report_ignoring(container, member)
        template_type_parameters = "template <" + (", ".join(template_type_parameters)) + "> class " + \
                                   container.displayname
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
        suffix = ""
        if function.is_const_method():
            suffix += " const"
        prefix = ""
        if function.is_static_method():
            prefix += "static "
        if function.is_virtual_method():
            prefix += "virtual "
            if function.is_pure_virtual_method():
                suffix += " = 0"
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
        """
        Generate the translation for a typedef.

        :param container:           A class or namespace.
        :param typedef:             The typedef object.
        :param level:               Recursion level controls indentation.
        :return:                    A string.
        """
        def skippable_attribute(member, text):
            """
            We don't seem to have access to the __attribute__(())s, but at least we can look for stuff we care about.

            :param member:          The attribute.
            :param text:            The raw source corresponding to the region of member.
            """
            if text.find("_DEPRECATED") != -1:
                sip["annotations"].add("Deprecated")
                return True
            if SipGenerator.TYPEDEF_SKIPPABLE_ATTR.search(text):
                return True
            SipGenerator._report_ignoring(typedef, member, text)

        sip = {
            "name": typedef.displayname,
            "annotations": set()
        }
        args = []
        result_type = ""
        for child in typedef.get_children():
            if child.kind == CursorKind.TEMPLATE_REF:
                result_type = child.displayname
            elif child.kind == CursorKind.TYPE_REF:
                #
                # Sigh. For results which are pointers, we dont have a way of detecting the need for the "*".
                #
                result_type = child.type.spelling
            elif child.kind == CursorKind.ENUM_DECL:
                if child.underlying_typedef_type:
                    #
                    # Typedefs for inlined enums seem to be emitted twice. Refer back to original.
                    #
                    enum = child.type.get_declaration()
                    decl = "__enum{}".format(enum.extent.start.line)
                else:
                    decl = self._enum_get(container, child, level)
                args.append(decl)
            elif child.kind == CursorKind.STRUCT_DECL:
                if child.underlying_typedef_type:
                    #
                    # Typedefs for inlined structs seem to be emitted twice. Refer back to original.
                    #
                    struct = child.type.get_declaration()
                    decl = "__struct{}".format(struct.extent.start.line)
                else:
                    decl = self._container_get(child, level, None)
                args.append(decl)
            elif child.kind == CursorKind.PARM_DECL:
                decl = child.displayname or "__{}".format(len(args))
                #
                # So far so good, but we need any default value.
                #
                decl = "{} {}".format(child.type.spelling, decl)
                args.append(decl)
            elif child.kind in EXPR_KINDS + [CursorKind.NAMESPACE_REF]:
                #
                # Ignore:
                #
                #   EXPR_KINDS: Array size etc.
                #   CursorKind.NAMESPACE_REF: Type stuff.
                #
                pass
            else:
                text = self._read_source(child.extent)
                if child.kind in [CursorKind.UNEXPOSED_ATTR, CursorKind.VISIBILITY_ATTR] and skippable_attribute(child,
                                                                                                                 text):
                    pass
                else:
                    SipGenerator._report_ignoring(typedef, child)
        #
        # Flesh out the SIP context for the rules engine.
        #
        sip["fn_result"] = ""
        if typedef.underlying_typedef_type.kind == TypeKind.MEMBERPOINTER:
            sip["fn_result"] = result_type
            sip["decl"] = ", ".join(args)
        elif typedef.underlying_typedef_type.kind == TypeKind.RECORD:
            sip["decl"] = result_type
        else:
            sip["decl"] = typedef.underlying_typedef_type.spelling
        sip["args"] = args
        #
        # Working out if a typedef is for a function pointer seems hard if not impossible in many cases. For such
        # cases, the only recourse right now is the following heristic (maybe it is safer to put this in the rules
        # engine?)
        #
        if typedef.underlying_typedef_type.kind != TypeKind.MEMBERPOINTER:
            if sip["decl"].endswith(")"):
                parts = sip["decl"].split("(*)", 2)
                if len(parts) == 2 and parts[1].startswith("("):
                    sip["fn_result"] = parts[0]
                    sip["decl"] = parts[1][1:-1]
        self.rule_set.typedef_rules().apply(container, typedef, sip)
        #
        # Now the rules have run, add any prefix/suffix.
        #
        pad = " " * (level * 4)
        if sip["name"]:
            if sip["fn_result"]:
                decl = pad + "typedef {}(*{})({})".format(sip["fn_result"], sip["name"], sip["decl"])
                decl = decl.replace("* ", "*").replace("& ", "&")
            else:
                decl = pad + "typedef {} {}".format(sip["decl"], sip["name"])
            #
            # SIP does not support deprecation of typedefs.
            #
            sip["annotations"].discard("Deprecated")
            if sip["annotations"]:
                decl += " /" + ",".join(sip["annotations"]) + "/"
            decl += ";\n"
        else:
            decl = pad + "// Discarded {}\n".format(SipGenerator.describe(typedef))
        return decl

    def _unexposed_decl_get(self, parent, decl):
        """
        The parser does not seem to provide access to the complete text of an unexposed decl.

            1. Run the lexer from "here" to the end of the outer scope, bailing out when we see the ";"
            or a "{" marking the end.
        """
        possible_extent = SourceRange.from_locations(decl.extent.start, parent.extent.end)
        text = ""
        found_end = False
        was_punctuated = True
        for token in self.tu.get_tokens(extent=possible_extent):
            if token.spelling in [";", "{"]:
                found_end = True
                break
            elif token.kind == TokenKind.PUNCTUATION:
                was_punctuated = True
                text += token.spelling
            else:
                if not was_punctuated:
                    text += " "
                text += token.spelling
                was_punctuated = False
        if not found_end and text:
            RuntimeError(_("No end found for {}::{}, '{}'").format(parent.spelling, decl.spelling, text))
        return text

    def _var_get(self, container, variable, level):
        """
        Generate the translation for a variable.

        :param container:           A class or namespace.
        :param variable:            The variable object.
        :param level:               Recursion level controls indentation.
        :return:                    A string.
        """

        def skippable_attribute(member, text):
            """
            We don't seem to have access to the __attribute__(())s, but at least we can look for stuff we care about.

            :param member:          The attribute.
            :param text:            The raw source corresponding to the region of member.
            """
            if SipGenerator.VAR_SKIPPABLE_ATTR.search(text):
                return True
            SipGenerator._report_ignoring(container, member, text)

        sip = {
            "name": variable.spelling,
            "annotations": set()
        }
        for child in variable.get_children():
            if child.kind in TEMPLATE_KINDS + [CursorKind.STRUCT_DECL, CursorKind.UNION_DECL]:
                #
                # Ignore:
                #
                #   TEMPLATE_KINDS, CursorKind.STRUCT_DECL, CursorKind.UNION_DECL: : The variable type.
                #
                pass
            else:
                text = self._read_source(child.extent)
                if child.kind == CursorKind.VISIBILITY_ATTR and skippable_attribute(child, text):
                    pass
                else:
                    SipGenerator._report_ignoring(variable, child)
        #
        # Flesh out the SIP context for the rules engine.
        #
        decl = "{} {}".format(variable.type.spelling, variable.spelling)
        decl = decl.replace("* ", "*").replace("& ", "&")
        sip["decl"] = decl
        self.rule_set.var_rules().apply(container, variable, sip)
        #
        # Now the rules have run, add any prefix/suffix.
        #
        pad = " " * (level * 4)
        if sip["name"]:
            prefix = self._var_get_keywords(variable)
            decl = prefix + sip["decl"]
            if sip["annotations"]:
                decl += " /" + ",".join(sip["annotations"]) + "/"
            #
            # SIP does not support protected variables, so we promote to public.
            #
            if variable.access_specifier == AccessSpecifier.PROTECTED:
                decl = pad + "public: " + decl +"; protected: // Promoted to public\n"
            else:
                decl = pad + decl + ";\n"
        else:
            decl = pad + "// Discarded {}\n".format(SipGenerator.describe(variable))
        return decl

    def _var_get_keywords(self, variable):
        """
        The parser does not provide direct access to the complete keywords (static, etc) of a variable
        in the displayname. It would be nice to get these from the AST, but I cannot find where they are hiding.

        :param variable:                    The variable object.
        :return: prefix                     String containing any prefix keywords.
        """
        if variable.storage_class == StorageClass.STATIC:
            #
            # SIP does not support "static".
            #
            prefix = ""
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
        if not SipGenerator._libclang:
            lines = subprocess.check_output(["/sbin/ldconfig", "-p"])
            for line in lines.split("\n"):
                fields = line.split()
                if fields and fields[0].startswith("libclang.so"):
                    SipGenerator._libclang = fields[-1]
                    logger.debug(_("Found libclang at {}").format(SipGenerator._libclang))
        if SipGenerator._libclang:
            if not cindex.Config.loaded:
                cindex.Config.set_library_file(SipGenerator._libclang)
        else:
            raise RuntimeError(_("Cannot find libclang"))

    @staticmethod
    def _report_ignoring(parent, child, text=None):
        if not text:
            text = child.displayname or child.spelling
        logger.debug(_("Ignoring {} {} child {}").format(parent.kind.name, parent.spelling, SipGenerator.describe(child, text)))


def main(argv=None):
    """
    Take a single C++ header file and generate the corresponding SIP file.
    Beyond simple generation of the SIP file from the corresponding C++
    header file, a set of rules can be used to customise the generated
    SIP file.

    Examples:

        sip_generator.py /usr/include/KF5/KItemModels/kselectionproxymodel.h
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(epilog=inspect.getdoc(main),
                                     formatter_class=HelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help=_("Enable verbose output"))
    parser.add_argument("--includes", default="/usr/include/x86_64-linux-gnu/qt5",
                        help=_("Roots of C++ headers to include"))
    parser.add_argument("--project-name", default="PyKF5", help=_("Project name"))
    parser.add_argument("--project-rules", default=os.path.join(os.path.dirname(__file__), "rules_PyKF5.py"),
                        help=_("Project rules"))
    parser.add_argument("--sources", default="/usr/include/KF5", help=_("Root of C++ headers to process"))
    parser.add_argument("source", help=_("C++ header to process, relative to --project-root"))
    try:
        args = parser.parse_args(argv[1:])
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        includes = args.includes.split(",")
        includes = [i.strip() for i in includes] + [args.sources]
        for path in includes:
            if not os.path.isdir(path):
                raise RuntimeError(_("Path '{}' is not a directory").format(path))
        #
        # Generate!
        #
        g = SipGenerator(includes, args.project_name, args.project_rules)
        body, includes = g.create_sip(args.sources, args.source)
        if body:
            print(body)
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
