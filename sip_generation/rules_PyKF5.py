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


def function_discard_qobject(container, function, text, matcher):
    return ""


def variable_discard_qobject(container, variable, text, matcher):
    return ""


def parameter_out_kdatetime_negzero(container, function, parameter, decl, init, matcher):
    parameter.sip_annotations.add("Out")
    return decl, init


def parameter_transfer_this_qobject_parents(container, function, parameter, decl, init, matcher):
    parameter.sip_annotations.add("TransferThis")
    return decl, init


def container_rules():

    return [
        ["QMetaTypeId<.*>", ".*", ".*", ".*", container_discard_qmetatypeid],
    ]


def function_rules():

    return [
        [".*", "metaObject|qt_metacast|tr|trUtf8|qt_metacall|qt_check_for_QOBJECT_macro", ".*", function_discard_qobject],
    ]


def parameter_rules():

    return [
        [".*", ".*", ".*", r"[KQ][A-Za-z_0-9]+\W*\*\W*parent", ".*", parameter_transfer_this_qobject_parents],
        ["KDateTime", "fromString", "negZero", ".*", ".*", parameter_out_kdatetime_negzero],
    ]


def variable_rules():

    return [
        [".*", "staticMetaObject", ".*", variable_discard_qobject],
    ]
