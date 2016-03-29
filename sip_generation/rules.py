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
"""SIP file generator overrides for PyKDE."""
from __future__ import print_function
import argparse
from copy import copy
import gettext
import inspect
import logging
import re
import sys
import traceback


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


logger = logging.getLogger(__name__)
gettext.install(__name__)

# Keep PyCharm happy.
_ = _


def function_discard(container, function, text, matcher):
    return ""


def KF5_FUNCTION_RULES():
    return [
        [".*", "metaObject|qt_metacast|tr|trUtf8|qt_metacall|qt_check_for_QOBJECT_macro", ".*", function_discard],
    ]


def parameter_out(container, function, parameter, decl, init, matcher):
    parameter.sip_annotations.append("Out")
    return decl, init


def parameter_transfer_this(container, function, parameter, decl, init, matcher):
    parameter.sip_annotations.append("TransferThis")
    return decl, init


def KF5_PARAMETER_RULES():
    return [
        [".*", ".*", ".*", r"[KQ][A-Za-z_0-9]+\W*\*\W*parent", ".*", parameter_transfer_this],
        ["KDateTime", "fromString", "negZero", ".*", ".*", parameter_out],
    ]


class Rule(object):
    def __init__(self, db, rule_number, fn, pattern_zip):
        self.db = db
        self.rule_number = rule_number
        self.fn = fn
        try:
            groups = ["(?P<{}>{})".format(name, pattern) for pattern, name in pattern_zip]
            groups = "-".join(groups)
            self.matcher = re.compile(groups)
        except Exception as e:
            groups = ["{} '{}'".format(name, pattern) for pattern, name in pattern_zip]
            groups = ", ".join(groups)
            raise RuntimeError(_("Bad {}: {}: {}").format(self, groups, e))

    def match(self, candidate):
        return self.matcher.match(candidate)

    def trace_result(self, original, modified):
        if not modified[:-2]:
            logger.debug(_("Rule {} suppressed {}").format(self, original))
        elif original[:-2] != modified[:-2] or original[-1] != modified[-1]:
            logger.debug(_("Rule {} modified {}->{}").format(self, original, modified))
        else:
            logger.warn(_("Rule {} did not modify {}").format(self, original))

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
        self.candidate_formatter = "-".join(["{}"] * len(parameter_names))

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


class FunctionRuleDb(AbstractCompiledRuleDb):
    def __init__(self, db):
        super(FunctionRuleDb, self).__init__(db, ["container", "function", "decl"])

    def apply(self, container, function, decl):
        """
        Walk over the rules database for functions, applying the first matching transformation.

        :param container:
        :param function:
        :param decl:
        :return:
        """
        matcher, rule = self._match(container.spelling, function.spelling, decl)
        if matcher:
            annotations = copy(function.sip_annotations)
            decl2 = rule.fn(container.spelling, function.spelling, decl, matcher)
            rule.trace_result((decl, annotations), (decl2, function.sip_annotations))
            decl = decl2
        return decl


class ParameterRuleDb(AbstractCompiledRuleDb):
    def __init__(self, db):
        super(ParameterRuleDb, self).__init__(db, ["container", "function", "parameter", "decl", "init"])

    def apply(self, container, function, parameter, decl, init):
        """
        Walk over the rules database for parameters, applying the first matching transformation.

        :param parameter:
        :param container:
        :param function:
        :param decl:
        :param init:
        :return:
        """
        matcher, rule = self._match(container.spelling, function.spelling, parameter, decl, init)
        if matcher:
            annotations = copy(parameter.sip_annotations)
            decl2, init2 = rule.fn(container.spelling, function.spelling, parameter, decl, init, matcher)
            rule.trace_result((decl, init, annotations), (decl2, init2, parameter.sip_annotations))
            decl, init = decl2, init2
        return decl, init


class RuleSet(object):
    def __init__(self, fn_db, param_db):
        self._fn_rules = FunctionRuleDb(fn_db)
        self._param_rules = ParameterRuleDb(param_db)

    def fn_rules(self):
        """
        THE RULES FOR FUNCTIONS.

        These are used to customise the behaviour of the SIP generator by allowing
        the declaration for any function to be customised, for example to add SIP
        compiler annotations.

        Each entry in the raw rule database must be a list with members as follows:

            0. A regular expression which matches the class or namespace "container"
            name enclosing the function.

            1. A regular expression which matches the function name.

            2. A regular expression which matches the parameter declaration (e.g.
            "int foo()").

            3. A function.

        In use, the database is walked in order from the first entry. If the regular
        expressions are matched, the function is called, and no further entries are
        walked. The function is called with the following contract:

            def function_xxx(container, function, decl, matcher):
                '''
                Return a modified declaration for the given function.

                :param container:               The clang.cindex.Cursor for the container.
                :param function:                The clang.cindex.Cursor for the function.
                :param decl:                    The text of the declaration.
                :param matcher:                 The re.Match object. This contains named
                                                groups corresponding to the parameter
                                                names above.
                :return: An updated decl, or function.sip_annotations.
                '''

        :return: The compiled form of the rules.
        """
        return self._fn_rules

    def param_rules(self):
        """
        THE RULES FOR FUNCTION PARAMETERS.

        These are used to customise the behaviour of the SIP generator by allowing
        the declaration for any parameter in any function to be customised, for
        example to add SIP compiler annotations.

        Each entry in the raw rule database must be a list with members as follows:

            0. A regular expression which matches the class or namespace "container"
            name enclosing the function.

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

            def parameter_xxx(container, function, parameter, decl, init, matcher):
                '''
                Return a modified declaration and initialiser for the given parameter.

                :param container:               The clang.cindex.Cursor for the container.
                :param function:                The clang.cindex.Cursor for the function.
                :param parameter:               The clang.cindex.Cursor for the parameter.
                :param decl:                    The text of the declaration.
                :param init:                    The text of any initialiser.
                :param matcher:                 The re.Match object. This contains named
                                                groups corresponding to the parameter
                                                names above.
                :return: An updated (decl, init) pair, or function.sip_annotations.
            '''

        :return: The compiled form of the rules.
        """
        return self._param_rules

#
# Statically prepare the rule logic. This takes the rules provided by the user and turns them into code.
#
rule_set = RuleSet(KF5_FUNCTION_RULES, KF5_PARAMETER_RULES)


def main(argv = None):
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
        for db in [rule_set.fn_rules, rule_set.param_rules]:
            print(inspect.getdoc(db))
            print()
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
