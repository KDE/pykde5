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
"""SIP file generator rules for PyKF5."""


def container_discard_qmetatypeid(container, sip, matcher):
    sip["decl"] = ""


def function_discard(container, function, sip, matcher):
    sip["decl"] = ""


def parameter_out_kdatetime_negzero(container, function, parameter, sip, matcher):
    sip["annotations"].add("Out")


def parameter_transfer_to_parent(container, function, parameter, sip, matcher):
    if function.is_static_method():
        sip["annotations"].add("Transfer")
    else:
        sip["annotations"].add("TransferThis")


def variable_discard_qobject(container, variable, sip, matcher):
    sip["decl"] = ""


def container_rules():

    return [
        ["QMetaTypeId<.*>", ".*", ".*", ".*", container_discard_qmetatypeid],
    ]


def function_rules():

    return [
        #
        # SIP does not support operator=.
        #
        [".*", "operator=", ".*", ".*", function_discard],
        #
        # Discard functions emitted by QOBJECT.
        #
        [".*", "metaObject|qt_metacast|tr|trUtf8|qt_metacall|qt_check_for_QOBJECT_macro", ".*", ".*", function_discard],
    ]


def parameter_rules():

    return [
        #
        # Annotate with Transfer or TransferThis when we see a parent object.
        #
        [".*", ".*", ".*", r"[KQ][A-Za-z_0-9]+\W*\*\W*parent", ".*", parameter_transfer_to_parent],
        ["KDateTime", "fromString", "negZero", ".*", ".*", parameter_out_kdatetime_negzero],
    ]


def variable_rules():

    return [
        [".*", "staticMetaObject", ".*", variable_discard_qobject],
    ]
