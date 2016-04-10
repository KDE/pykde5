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
"""SIP file generator rules engine for PyKDE."""
from __future__ import print_function

import argparse
import gettext
import inspect
import logging
import re
import sys
import traceback
from copy import deepcopy
from clang.cindex import CursorKind

class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


logger = logging.getLogger(__name__)
gettext.install(__name__)
_SEPARATOR = "\x00"

# Keep PyCharm happy.
_ = _


def _parents(container):
    parents = []
    parent = container.semantic_parent
    while parent and parent.kind != CursorKind.TRANSLATION_UNIT:
        parents.append(parent.spelling)
        parent = parent.semantic_parent
    parents = "::".join(reversed(parents))
    return parents


class Rule(object):
    def __init__(self, db, rule_number, fn, pattern_zip):
        self.db = db
        self.rule_number = rule_number
        self.fn = fn
        try:
            groups = ["(?P<{}>{})".format(name, pattern) for pattern, name in pattern_zip]
            groups = _SEPARATOR.join(groups)
            self.matcher = re.compile(groups)
        except Exception as e:
            groups = ["{} '{}'".format(name, pattern) for pattern, name in pattern_zip]
            groups = ", ".join(groups)
            raise RuntimeError(_("Bad {}: {}: {}").format(self, groups, e))

    def match(self, candidate):
        return self.matcher.match(candidate)

    def trace_result(self, parents, original, modified):
        fqn = parents + "::" + original["name"]
        if not modified["name"]:
            logger.debug(_("Rule {} suppressed {}, {}").format(self, fqn, original))
        else:
            delta = False
            for k, v in original.iteritems():
                if v != modified[k]:
                    delta = True
                    break
            if delta:
                logger.debug(_("Rule {} modified {}, {}->{}").format(self, fqn, original, modified))
            else:
                logger.warn(_("Rule {} did not modify {}, {}").format(self, fqn, original))

    def __str__(self):
        return "{}[{}],{}".format(self.db.__name__, self.rule_number, self.fn.__name__)


class AbstractCompiledRuleDb(object):
    def __init__(self, db, parameter_names):
        self.db = db
        self.compiled_rules = []
        for i, raw_rule in enumerate(db()):
            if len(raw_rule) != len(parameter_names) + 1:
                raise RuntimeError(_("Bad raw rule {}: {}: {}").format(db.__name__, raw_rule, parameter_names))
            z = zip(raw_rule[:-1], parameter_names)
            self.compiled_rules.append(Rule(db, i, raw_rule[-1], z))
        self.parameter_names = parameter_names
        self.candidate_formatter = _SEPARATOR.join(["{}"] * len(parameter_names))

    def _match(self, *args):
        candidate = self.candidate_formatter.format(*args)
        for rule in self.compiled_rules:
            matcher = rule.match(candidate)
            if matcher:
                #
                # Only use the first matching rule.
                #
                return matcher, rule
        return None, None

    def apply(self, *args):
        raise NotImplemented(_("Missing subclass"))


class ContainerRuleDb(AbstractCompiledRuleDb):
    """
    THE RULES FOR CONTAINERS.

    These are used to customise the behaviour of the SIP generator by allowing
    the declaration for any container (class, namespace, struct, union) to be
    customised, for example to add SIP compiler annotations.

    Each entry in the raw rule database must be a list with members as follows:

        0. A regular expression which matches the fully-qualified name of the
        "container" enclosing the container.

        1. A regular expression which matches the container name.

        2. A regular expression which matches any template parameters.

        3. A regular expression which matches the container declaration.

        4. A regular expression which matches any base specifiers.

        5. A function.

    In use, the database is walked in order from the first entry. If the regular
    expressions are matched, the function is called, and no further entries are
    walked. The function is called with the following contract:

        def container_xxx(container, sip, matcher):
            '''
            Return a modified declaration for the given container.

            :param container:   The clang.cindex.Cursor for the container.
            :param sip:         A dict with the following keys:

                                    name                The name of the container.
                                    template_parameters Any template parameters.
                                    decl                The declaration.
                                    base_specifiers     Any base specifiers.
                                    body                The body, less the outer
                                                        pair of braces.
                                    annotations         Any SIP annotations.

            :param matcher:         The re.Match object. This contains named
                                    groups corresponding to the key names above
                                    EXCEPT body and annotations.

            :return: An updated set of sip.xxx values. Setting sip.name to the
                     empty string will cause the container to be suppressed.
            '''

    :return: The compiled form of the rules.
    """
    def __init__(self, db):
        super(ContainerRuleDb, self).__init__(db, ["parents", "container", "template_parameters", "decl", "base_specifiers"])

    def apply(self, container, sip):
        """
        Walk over the rules database for functions, applying the first matching transformation.

        :param container:           The clang.cindex.Cursor for the container.
        :param sip:                 The SIP dict.
        """
        parents = _parents(container)
        matcher, rule = self._match(parents, sip["name"], sip["template_parameters"], sip["decl"], sip["base_specifiers"])
        if matcher:
            before = deepcopy(sip)
            rule.fn(container, sip, matcher)
            rule.trace_result(parents, before, sip)


class FunctionRuleDb(AbstractCompiledRuleDb):
    """
    THE RULES FOR FUNCTIONS.

    These are used to customise the behaviour of the SIP generator by allowing
    the declaration for any function to be customised, for example to add SIP
    compiler annotations.

    Each entry in the raw rule database must be a list with members as follows:

        0. A regular expression which matches the fully-qualified name of the
        "container" enclosing the function.

        1. A regular expression which matches the function name.

        2. A regular expression which matches any template parameters.

        3. A regular expression which matches the function declaration (e.g.
        "int foo()").

        4. A function.

    In use, the database is walked in order from the first entry. If the regular
    expressions are matched, the function is called, and no further entries are
    walked. The function is called with the following contract:

        def function_xxx(container, function, sip, matcher):
            '''
            Return a modified declaration for the given function.

            :param container:   The clang.cindex.Cursor for the container.
            :param function:    The clang.cindex.Cursor for the function.
            :param sip:         A dict with the following keys:

                                    name                The name of the function.
                                    template_parameters Any template parameters.
                                    decl                The declaration.
                                    annotations         Any SIP annotations.

            :param matcher:         The re.Match object. This contains named
                                    groups corresponding to the key names above
                                    EXCEPT annotations.

            :return: An updated set of sip.xxx values. Setting sip.name to the
                     empty string will cause the container to be suppressed.
            '''

    :return: The compiled form of the rules.
    """
    def __init__(self, db):
        super(FunctionRuleDb, self).__init__(db, ["container", "function", "template_parameters", "decl"])

    def apply(self, container, function, sip):
        """
        Walk over the rules database for functions, applying the first matching transformation.

        :param container:           The clang.cindex.Cursor for the container.
        :param function:            The clang.cindex.Cursor for the function.
        :param sip:                 The SIP dict.
        """
        parents = _parents(function)
        matcher, rule = self._match(parents, sip["name"], sip["template_parameters"], sip["decl"])
        if matcher:
            before = deepcopy(sip)
            rule.fn(container, function, sip, matcher)
            rule.trace_result(parents, before, sip)


class ParameterRuleDb(AbstractCompiledRuleDb):
    """
    THE RULES FOR FUNCTION PARAMETERS.

    These are used to customise the behaviour of the SIP generator by allowing
    the declaration for any parameter in any function to be customised, for
    example to add SIP compiler annotations.

    Each entry in the raw rule database must be a list with members as follows:

        0. A regular expression which matches the fully-qualified name of the
        "container" enclosing the function enclosing the parameter.

        1. A regular expression which matches the function name enclosing the
        parameter.

        2. A regular expression which matches the parameter name.

        3. A regular expression which matches the parameter declaration (e.g.
        "int foo").

        4. A regular expression which matches the parameter initialiser (e.g.
        "Xyz:MYCONST + 42").

        5. A function.

    In use, the database is walked in order from the first entry. If the regular
    expressions are matched, the function is called, and no further entries are
    walked. The function is called with the following contract:

        def parameter_xxx(container, function, parameter, sip, init, matcher):
            '''
            Return a modified declaration and initialiser for the given parameter.

            :param container:   The clang.cindex.Cursor for the container.
            :param function:    The clang.cindex.Cursor for the function.
            :param parameter:   The clang.cindex.Cursor for the parameter.
            :param sip:         A dict with the following keys:

                                    name                The name of the function.
                                    decl                The declaration.
                                    init                Any initialiser.
                                    annotations         Any SIP annotations.

            :param matcher:         The re.Match object. This contains named
                                    groups corresponding to the key names above
                                    EXCEPT annotations.

            :return: An updated set of sip.xxx values.
        '''

    :return: The compiled form of the rules.
    """
    def __init__(self, db):
        super(ParameterRuleDb, self).__init__(db, ["container", "function", "parameter", "decl", "init"])

    def apply(self, container, function, parameter, sip):
        """
        Walk over the rules database for parameters, applying the first matching transformation.

        :param container:           The clang.cindex.Cursor for the container.
        :param function:            The clang.cindex.Cursor for the function.
        :param parameter:           The clang.cindex.Cursor for the parameter.
        :param sip:                 The SIP dict.
        """
        parents = _parents(function)
        matcher, rule = self._match(parents, function.spelling, sip["name"], sip["decl"], sip["init"])
        if matcher:
            before = deepcopy(sip)
            rule.fn(container, function, parameter, sip, matcher)
            rule.trace_result(parents, before, sip)


class TypedefRuleDb(AbstractCompiledRuleDb):
    """
    THE RULES FOR TYPEDEFS.

    These are used to customise the behaviour of the SIP generator by allowing
    the declaration for any typedef to be customised, for example to add SIP
    compiler annotations.

    Each entry in the raw rule database must be a list with members as follows:

        0. A regular expression which matches the fully-qualified name of the
        "container" enclosing the typedef.

        1. A regular expression which matches the typedef name.

        2. A regular expression which matches the typedef declaration (e.g.
        "typedef int foo").

        3. A function.

    In use, the database is walked in order from the first entry. If the regular
    expressions are matched, the function is called, and no further entries are
    walked. The function is called with the following contract:

        def typedef_xxx(container, typedef, sip, matcher):
            '''
            Return a modified declaration for the given function.

            :param container:   The clang.cindex.Cursor for the container.
            :param typedef:     The clang.cindex.Cursor for the typedef.
            :param sip:         A dict with the following keys:

                                    name                The name of the typedef.
                                    decl                The declaration.
                                    annotations         Any SIP annotations.

            :param matcher:         The re.Match object. This contains named
                                    groups corresponding to the key names above
                                    EXCEPT annotations.

            :return: An updated set of sip.xxx values. Setting sip.name to the
                     empty string will cause the container to be suppressed.
            '''

    :return: The compiled form of the rules.
    """
    def __init__(self, db):
        super(TypedefRuleDb, self).__init__(db, ["container", "typedef", "decl"])

    def apply(self, container, typedef, sip):
        """
        Walk over the rules database for typedefs, applying the first matching transformation.

        :param container:           The clang.cindex.Cursor for the container.
        :param typedef:             The clang.cindex.Cursor for the typedef.
        :param sip:                 The SIP dict.
        """
        parents = _parents(typedef)
        matcher, rule = self._match(parents, sip["name"], sip["decl"])
        if matcher:
            before = deepcopy(sip)
            rule.fn(container, typedef, sip, matcher)
            rule.trace_result(parents, before, sip)


class VariableRuleDb(AbstractCompiledRuleDb):
    """
    THE RULES FOR VARIABLES.

    These are used to customise the behaviour of the SIP generator by allowing
    the declaration for any variable to be customised, for example to add SIP
    compiler annotations.

    Each entry in the raw rule database must be a list with members as follows:

        0. A regular expression which matches the fully-qualified name of the
        "container" enclosing the variable.

        1. A regular expression which matches the variable name.

        2. A regular expression which matches the variable declaration (e.g.
        "int foo").

        3. A function.

    In use, the database is walked in order from the first entry. If the regular
    expressions are matched, the function is called, and no further entries are
    walked. The function is called with the following contract:

        def variable_xxx(container, variable, sip, matcher):
            '''
            Return a modified declaration for the given function.

            :param container:   The clang.cindex.Cursor for the container.
            :param variable:    The clang.cindex.Cursor for the variable.
            :param sip:         A dict with the following keys:

                                    name                The name of the variable.
                                    decl                The declaration.
                                    annotations         Any SIP annotations.

            :param matcher:         The re.Match object. This contains named
                                    groups corresponding to the key names above
                                    EXCEPT annotations.

            :return: An updated set of sip.xxx values. Setting sip.name to the
                     empty string will cause the container to be suppressed.
            '''

    :return: The compiled form of the rules.
    """
    def __init__(self, db):
        super(VariableRuleDb, self).__init__(db, ["container", "variable", "decl"])

    def apply(self, container, variable, sip):
        """
        Walk over the rules database for variables, applying the first matching transformation.

        :param container:           The clang.cindex.Cursor for the container.
        :param variable:            The clang.cindex.Cursor for the variable.
        :param sip:                 The SIP dict.
        """
        parents = _parents(variable)
        matcher, rule = self._match(parents, sip["name"], sip["decl"])
        if matcher:
            before = deepcopy(sip)
            rule.fn(container, variable, sip, matcher)
            rule.trace_result(parents, before, sip)


class RuleSet(object):
    def __init__(self, rules_module):
        self._container_rules = ContainerRuleDb(rules_module.container_rules)
        self._fn_rules = FunctionRuleDb(rules_module.function_rules)
        self._param_rules = ParameterRuleDb(rules_module.parameter_rules)
        self._typedef_rules = TypedefRuleDb(rules_module.typedef_rules)
        self._var_rules = VariableRuleDb(rules_module.variable_rules)

    def container_rules(self):
        return self._container_rules

    def fn_rules(self):
        return self._fn_rules

    def param_rules(self):
        return self._param_rules

    def typedef_rules(self):
        return self._typedef_rules

    def var_rules(self):
        return self._var_rules


def main(argv=None):
    """
    Rules engine for SIP file generation.

    Examples:

        rules.py
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(epilog=inspect.getdoc(main),
                                     formatter_class=HelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help=_("Enable verbose output"))
    try:
        args = parser.parse_args(argv[1:])
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        #
        # Generate help!
        #
        for db in [ContainerRuleDb, FunctionRuleDb, ParameterRuleDb, TypedefRuleDb, VariableRuleDb]:
            print(inspect.getdoc(db))
            print()
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
