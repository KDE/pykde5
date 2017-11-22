#!/usr/bin/env python
# Copyright 2017 Shaheed Haque <srhaque@theiet.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import gettext
import logging
import sys
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

import cppyy
from Qt5.Core import QCommandLineParser, QString
from Qt5.Widgets import QApplication
from KF5.CoreAddons import KAboutData, KAboutLicense
from KF5.WidgetsAddons import KGuiItem, KMessageBox


logger = logging.getLogger(__name__)
gettext.install("tutorial1")
_ = lambda i18n: QString(builtins._(i18n))

help_text = """This short program is the basic KDE application.

It uses KAboutData to initialize some basic program information
that is used by KDE (beyond simply setting up the About dialog
box in a more complex program).

See https://techbase.kde.org/Development/Tutorials/First_program.
"""

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        app = QApplication(argv)
        #
        # We prefer to use a Pythonic approach to i18n using gettext, rather than rely
        # on the C++ toolchain: see gettext usage.
        #
        # KLocalizedString.setApplicationDomain("tutorial1")
        #
        about_data = KAboutData(
             # The program name used internally. (componentName)
             QString("tutorial1"),
             # A displayable program name string. (displayName)
             _("Tutorial 1"),
             # The program version string. (version)
             QString("1.0"),
             # Short description of what the app does. (shortDescription)
             _("Displays a KMessageBox popup"),
             # The license this code is released under
             KAboutLicense.GPL,
             # Copyright Statement (copyrightStatement = QString())
             _("(c) 2017"),
             # Optional text shown in the About box.
             # Can contain any information desired. (otherText)
             _(help_text),
             # The program homepage string. (homePageAddress = QString())
             QString("http://example.com/"),
             # The bug report email address
             # (bugsEmailAddress = QLatin1String("submit@bugs.kde.org")
             QString("submit@bugs.kde.org"))
        about_data.addAuthor(_("Name"), _("Task"), QString("your@email.com"),
                             QString("http://your.website.com"), QString("OSC Username"))
        KAboutData.setApplicationData(about_data)

        parser = QCommandLineParser()
        parser.addHelpOption()
        parser.addVersionOption()
        about_data.setupCommandLine(parser)
        parser.process(app)
        about_data.processCommandLine(parser)
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

        yes_button = KGuiItem(_("Hello"), QString(), _("This is a tooltip"),
                              _("This is a WhatsThis help text."))
        answer = KMessageBox.questionYesNo(cppyy.nullptr, _("Hello World"), _("Hello"), yes_button)
        return 0 if answer == KMessageBox.Yes else 1
    except RuntimeError as e:
        logger.error("Unexpected {}".format(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
