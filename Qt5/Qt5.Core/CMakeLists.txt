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

set(_pkg "Qt5.Core")
project(${_pkg})

#
# Get the information needed to create bindings for a set of related components.
# Increase the VERBOSE setting for diagnostics.
#
get_binding_info(
    VERBOSE 0
    COMPONENTS Qt5Core)
#
# Customise the automatically generated information.
#
list(FILTER h_files EXCLUDE REGEX ".*/qatomic_.*.h")
list(FILTER h_files EXCLUDE REGEX ".*/qfunctions_.*.h")
list(FILTER h_files EXCLUDE REGEX ".*/.*_impl.h")
list(FILTER h_files EXCLUDE REGEX ".*/qt_windows.h")
list(FILTER h_files EXCLUDE REGEX ".*/.*.conf")
list(FILTER h_files EXCLUDE REGEX ".*/Q_.*")
#
# Including qlist.h causes rootcling to crash.
#
list(FILTER h_files EXCLUDE REGEX ".*/qlist.h")
set(linkdefs "#pragma link off class QAbstractAnimationPrivate\;
#pragma link off class QAbstractEventDispatcherPrivate\;
#pragma link off class QAbstractItemModelPrivate\;
#pragma link off class QAbstractItemViewPrivate\;
#pragma link off class QAbstractNativeEventFilterPrivate\;
#pragma link off class QAbstractProxyModelPrivate\;
#pragma link off class QAbstractStatePrivate\;
#pragma link off class QAbstractTransitionPrivate\;
#pragma link off class QAnimationDriverPrivate\;
#pragma link off class QAnimationGroupPrivate\;
#pragma link off class QApplicationPrivate\;
#pragma link off class QBufferPrivate\;
#pragma link off class QByteArrayMatcherPrivate\;
#pragma link off class QCocoaEventDispatcherPrivate\;
#pragma link off class QCollatorPrivate\;
#pragma link off class QCollatorSortKeyPrivate\;
#pragma link off class QCommandLineOptionPrivate\;
#pragma link off class QCommandLineParserPrivate\;
#pragma link off class QCoreApplicationPrivate\;
#pragma link off class QCryptographicHashPrivate\;
#pragma link off class QDataStreamPrivate\;
#pragma link off class QDateTimePrivate\;
#pragma link off class QDebugStateSaverPrivate\;
#pragma link off class QDirIteratorPrivate\;
#pragma link off class QDirPrivate\;
#pragma link off class QDoubleValidatorPrivate\;
#pragma link off class QEasingCurvePrivate\;
#pragma link off class QEventDispatcherUNIXPrivate\;
#pragma link off class QEventLoopLockerPrivate\;
#pragma link off class QEventLoopPrivate\;
#pragma link off class QEventPrivate\;
#pragma link off class QEventTransitionPrivate\;
#pragma link off class QFileDevicePrivate\;
#pragma link off class QFileInfoPrivate\;
#pragma link off class QFilePrivate\;
#pragma link off class QFileSelectorPrivate\;
#pragma link off class QFileSystemWatcherPrivate\;
#pragma link off class QFinalStatePrivate\;
#pragma link off class QFutureInterfaceBasePrivate\;
#pragma link off class QFutureWatcherBasePrivate\;
#pragma link off class QGraphicsScenePrivate\;
#pragma link off class QGuiApplicationPrivate\;
#pragma link off class QHistoryStatePrivate\;
#pragma link off class QIdentityProxyModelPrivate\;
#pragma link off class QIODevicePrivate\;
#pragma link off class QItemSelectionModelPrivate\;
#pragma link off class QLibraryPrivate\;
#pragma link off class QLocalePrivate\;
#pragma link off class QLockFilePrivate\;
#pragma link off class QMessageAuthenticationCodePrivate\;
#pragma link off class QMetaMethodPrivate\;
#pragma link off class QMimeDatabasePrivate\;
#pragma link off class QMimeDataPrivate\;
#pragma link off class QMimeTypePrivate\;
#pragma link off class QObjectPrivate\;
#pragma link off class QParallelAnimationGroupPrivate\;
#pragma link off class QPauseAnimationPrivate\;
#pragma link off class QProcessEnvironmentPrivate\;
#pragma link off class QProcessPrivate\;
#pragma link off class QPropertyAnimationPrivate\;
#pragma link off class QReadWriteLockPrivate\;
#pragma link off class QResourcePrivate\;
#pragma link off class QSaveFilePrivate\;
#pragma link off class QSemaphorePrivate\;
#pragma link off class QSequentialAnimationGroupPrivate\;
#pragma link off class QSettingsPrivate\;
#pragma link off class QSharedMemoryPrivate\;
#pragma link off class QSignalMapperPrivate\;
#pragma link off class QSignalTransitionPrivate\;
#pragma link off class QSocketNotifierPrivate\;
#pragma link off class QSortFilterProxyModelPrivate\;
#pragma link off class QStateMachinePrivate\;
#pragma link off class QStatePrivate\;
#pragma link off class QStorageInfoPrivate\;
#pragma link off class QStringMatcherPrivate\;
#pragma link off class QSystemSemaphorePrivate\;
#pragma link off class QTemporaryDirPrivate\;
#pragma link off class QTemporaryFilePrivate\;
#pragma link off class QTextBoundaryFinderPrivate\;
#pragma link off class QTextStreamPrivate\;
#pragma link off class QThreadPoolPrivate\;
#pragma link off class QThreadPrivate\;
#pragma link off class QTimeLinePrivate\;
#pragma link off class QTimeZonePrivate\;
#pragma link off class QTranslatorPrivate\;
#pragma link off class QUrlPrivate\;
#pragma link off class QUrlQueryPrivate\;
#pragma link off class QVariantAnimationPrivate\;
#pragma link off class QVariant::Private::Data\;
#pragma link off class QWaitConditionPrivate\;
#pragma link off class QWidgetPrivate\;
#pragma link off class QWinEventNotifierPrivate\;
#pragma link off class QXmlStreamReaderPrivate\;
#pragma link off class QXmlStreamWriterPrivate\;")
#
# Generate the bindings.
#
add_bindings(${_pkg} "Shaheed Haque" "srhaque@theiet.org" "${version}" "${include_dirs}" "${link_libraries}" "${linkdefs}" "${h_dirs}" "${h_files}")
unset(_pkg)
