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
import gettext
import logging
import re


logger = logging.getLogger(__name__)
gettext.install(__name__)

# Keep PyCharm happy.
_ = _


def function_discard(container, function, text, matcher):
    return ""


function_rules = [
        (".*", "(metaObject|qt_metacast|tr|trUtf8|qt_metacall)", ".*", function_discard)
    ]


def parameter_transfer_this(container, function, parameter, decl, init, matcher):
    return decl + " /TransferThis/", init


parameter_rules = [
        (".*", ".*", ".*", r"[KQ][A-Za-z_0-9]+\W*\*\W*parent", ".*", parameter_transfer_this)
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
    for i, o in enumerate(parameter_rules):
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
    for i, o in enumerate(function_rules):
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
