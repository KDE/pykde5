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

"""Customisation logic."""
import ctypes


def c13n_hook(pkg_module):
    #
    # Replace the rather cumbersome QApplication constructor with something
    # easier to use.
    #
    clazz = pkg_module.QApplication
    old__init__ = clazz.__init__

    def QApplication(self, argv, flags = clazz.ApplicationFlags):
        """
        QApplication::QApplication(self, argv, int = ApplicationFlags)
        The QApplication object must remain in scope for the lifetime of
        the program. Note that value of argv can be modified on return,
        any subsequent changes are exposed via the argv property.
        """
        #
        # Not only can the QApplication constructor modify argc/argv, other
        # members can use the values later, so we must ensure the passed values
        # remain in scope till the end of the program.
        #
        argc = len(argv)
        self._argc = ctypes.c_int(argc)
        self._argv = (ctypes.c_char_p * argc)(*[ctypes.c_char_p(a.encode('ascii')) for a in argv])
        old__init__(self, self._argc, self._argv, flags)
        argv[:] = self.argv

    @property
    def argv(self):
        """Ongoing access to the (modified) argv."""
        return [self._argv[i].decode('ascii') for i in range(self._argc.value)]

    clazz.__init__ = QApplication
    clazz.argv = argv