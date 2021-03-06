// Copyright 2014 Simon Edwards <simon@simonzone.com>

//                 Generated by twine2

// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU Library General Public License as
// published by the Free Software Foundation; either version 2, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details

// You should have received a copy of the GNU Library General Public
// License along with this program; if not, write to the
// Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

class KProcess : QProcess
{
%TypeHeaderCode
#include <kprocess.h>
%End

public:
    enum OutputChannelMode
    {
        SeparateChannels,
        MergedChannels,
        ForwardedChannels,
        OnlyStdoutChannel,
        OnlyStderrChannel
    };
    explicit                KProcess (QObject* parent = 0);
    virtual ~KProcess ();
    void                    setOutputChannelMode (KProcess::OutputChannelMode mode);
    KProcess::OutputChannelMode  outputChannelMode () const;
    void                    setNextOpenMode (QIODevice::OpenMode mode);
    void                    setEnv (const QString& name, const QString& value, bool overwrite = 1);
    void                    unsetEnv (const QString& name);
    void                    clearEnvironment ();
    void                    setProgram (const QString& exe, const QStringList& args = QStringList());
    void                    setProgram (const QStringList& argv);
    void                    clearProgram ();
    void                    setShellCommand (const QString& cmd);
    QStringList             program () const;
    void                    start ();
    int                     execute (int msecs = -1);
    static int              execute (const QString& exe, const QStringList& args = QStringList(), int msecs = -1);
    static int              execute (const QStringList& argv, int msecs = -1);
    int                     startDetached ();
    static int              startDetached (const QString& exe, const QStringList& args = QStringList());
    static int              startDetached (const QStringList& argv);
    int                     pid () const;
protected:
//ig                            KProcess (KProcessPrivate* d, QObject* parent);
public:
    KProcess&               operator<< (const QString& arg);
    KProcess&               operator<< (const QStringList& args);
};
