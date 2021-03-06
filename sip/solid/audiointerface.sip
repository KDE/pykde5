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

namespace Solid
{
class AudioInterface : Solid::DeviceInterface
{
%TypeHeaderCode
#include <audiointerface.h>
%End

public:
    enum AudioDriver
    {
        Alsa,
        OpenSoundSystem,
        UnknownAudioDriver
    };
    enum AudioInterfaceType
    {
        UnknownAudioInterfaceType,
        AudioControl,
        AudioInput,
        AudioOutput
    };
    typedef QFlags<Solid::AudioInterface::AudioInterfaceType> AudioInterfaceTypes;
    enum SoundcardType
    {
        InternalSoundcard,
        UsbSoundcard,
        FirewireSoundcard,
        Headset,
        Modem
    };
private:
    explicit                AudioInterface (QObject* backendObject);
public:
    virtual ~AudioInterface ();
    static Solid::DeviceInterface::Type  deviceInterfaceType ();
    Solid::AudioInterface::AudioDriver  driver () const;
    QVariant                driverHandle () const;
    QString                 name () const;
    Solid::AudioInterface::AudioInterfaceTypes  deviceType () const;
    Solid::AudioInterface::SoundcardType  soundcardType () const;
};
};
