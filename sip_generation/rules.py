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


def _FUNCTION_RULES():
    """
    THE RULE DATABASE FOR FUNCTIONS.

    This is used to customise the behaviour of the SIP generator by allowing
    the declaration for any function to be customised, for example to add SIP
    compiler annotations.

    Each entry must be a tuple with members as follows:

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
            :return: An updated decl, init pair.
            '''
    """
    return [
        (".*", "metaObject|qt_metacast|tr|trUtf8|qt_metacall|qt_check_for_QOBJECT_macro", ".*", function_discard),
    ]


def parameter_out(container, function, parameter, decl, init, matcher):
    return decl + " /Out/", init


def parameter_transfer_this(container, function, parameter, decl, init, matcher):
    return decl + " /TransferThis/", init


def _PARAMETER_RULES():
    """
    THE RULE DATABASE FOR FUNCTIONS PARAMETERS.

    This is used to customise the behaviour of the SIP generator by allowing
    the declaration for any parameter in any function to be customised, for
    example to add SIP compiler annotations.

    Each entry must be a tuple with members as follows:

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
            :return: An updated decl, init pair.
          '''
    """
    return [
        (".*", ".*", ".*", r"[KQ][A-Za-z_0-9]+\W*\*\W*parent", ".*", parameter_transfer_this),
        ("KDateTime", "fromString", "negZero", ".*", ".*", parameter_out),
    ]


def apply_function_rules(container, function, decl):
    """
    Walk over the rules database for functions, applying the first matching transformation.

    :param container:
    :param function:
    :param decl:
    :return:
    """
    candidate = "{}-{}-{}".format(container.spelling, function.spelling, decl)
    for i, o in enumerate(_compiled_fn_rules):
        m, x = o
        if m.match(candidate):
            modified_decl = x(container.spelling, function.spelling, decl, m)
            if not modified_decl:
                logger.debug(_("Rule {} suppressed {}").format(i, decl))
            else:
                if decl != modified_decl:
                    logger.info(_("Rule {} modified {}").format(i, decl))
            decl = modified_decl
            #
            # Only use the first matching rule.
            #
            break
    return decl


def apply_param_rules(container, function, parameter, decl, init):
    """
    Walk over the rules database for parameters, applying the first matching transformation.

    :param parameter:
    :param container:
    :param function:
    :param decl:
    :param init:
    :return:
    """
    candidate = "{}-{}-{}-{}-{}".format(container.spelling, function.spelling, parameter, decl, init)
    for i, o in enumerate(_compiled_param_rules):
        m, x = o
        matcher = m.match(candidate)
        if matcher:
            decl2, init2 = x(container.spelling, function.spelling, parameter, decl, init, matcher)
            if decl != decl2 or init != init2:
                logger.debug(
                    _("Rule {}[{}] modified '{}'->'{}', '{}'->'{}'").format(
                        i, x.__name__, decl, decl2, init, init2))
                decl = decl2
                init = init2
            else:
                logger.warn(_("Rule {}[{}] did not modify '{}' '{}'").format(i, x.__name__, decl, init))
            #
            # Only use the first matching rule.
            #
            break
    return decl, init


def _compile_parameter_rules():
    """
    Take the rules provided by the user and turns them into code.
    """
    results = []
    for i, o in enumerate(_PARAMETER_RULES()):
        c, f, p, d, init, handler = o
        z = zip([c, f, p, d, init],
                ["container", "function", "parameter", "decl", "init"])
        try:
            groups = ["(?P<{}>{})".format(name, pattern) for pattern, name in z]
            groups = "-".join(groups)
            results.append((re.compile(groups), handler))
        except Exception as e:
            groups = ["{} '{}'".format(name, pattern) for pattern, name in z]
            groups = ", ".join(groups)
            raise RuntimeError(_("Bad parameter_rules[{}]: {}: {}").format(i, groups, e))
    return results


def _compile_function_rules():
    """
    Take the rules provided by the user and turns them into code.
    """
    results = []
    for i, o in enumerate(_FUNCTION_RULES()):
        c, f, d, handler = o
        z = zip([c, f, d],
                ["container", "function", "decl"])
        try:
            groups = ["(?P<{}>{})".format(name, pattern) for pattern, name in z]
            groups = "-".join(groups)
            results.append((re.compile(groups), handler))
        except Exception as e:
            groups = ["{} '{}'".format(name, pattern) for pattern, name in z]
            groups = ", ".join(groups)
            raise RuntimeError(_("Bad function_rule[{}]: {}: {}").format(i, groups, e))
    return results


#
# Staticallly prepare the rule logic. This takes the rules provided by the user and turns them into
#
_compiled_fn_rules = _compile_function_rules()
_compiled_param_rules = _compile_parameter_rules()


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
        for db in [_FUNCTION_RULES, _PARAMETER_RULES]:
            print(_(""))
            help = inspect.getdoc(db)
            print(db.__name__ + ": " + help)
            print()
    except Exception as e:
        tbk = traceback.format_exc()
        print(tbk)
        return -1


if __name__ == "__main__":
    sys.exit(main())
