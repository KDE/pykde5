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
class Battery : Solid::DeviceInterface
{
%TypeHeaderCode
#include <battery.h>
%End

public:
    enum BatteryType
    {
        UnknownBattery,
        PdaBattery,
        UpsBattery,
        PrimaryBattery,
        MouseBattery,
        KeyboardBattery,
        KeyboardMouseBattery,
        CameraBattery,
        PhoneBattery,
        MonitorBattery
    };
    enum ChargeState
    {
        NoCharge,
        Charging,
        Discharging,
        FullyCharged
    };
    enum Technology
    {
        UnknownTechnology,
        LithiumIon,
        LithiumPolymer,
        LithiumIronPhosphate,
        LeadAcid,
        NickelCadmium,
        NickelMetalHydride
    };
private:
    explicit                Battery (QObject* backendObject);
public:
    virtual ~Battery ();
    static Solid::DeviceInterface::Type  deviceInterfaceType ();
    bool                    isPlugged () const;
    bool                    isPowerSupply () const;
    Solid::Battery::BatteryType  type () const;
    int                     chargePercent () const;
    int                     capacity () const;
    bool                    isRechargeable () const;
    Solid::Battery::ChargeState  chargeState () const;
    Solid::Battery::Technology  technology () const;
    double                  energy () const;
    double                  energyRate () const;
    double                  voltage () const;
signals:
    void                    chargePercentChanged (int value, const QString& udi);
    void                    capacityChanged (int value, const QString& udi);
    void                    energyChanged (double energy, const QString& udi);
    void                    energyRateChanged (double energyRate, const QString& udi);
    void                    powerSupplyStateChanged (bool newState, const QString& udi);
public:
    bool                    isPresent () const;
    qlonglong               timeToEmpty () const;
    qlonglong               timeToFull () const;
    double                  temperature () const;
    bool                    isRecalled () const;
    QString                 recallVendor () const;
    QString                 recallUrl () const;
    QString                 serial () const;
signals:
    void                    presentStateChanged (bool newState, const QString& udi);
    void                    chargeStateChanged (int newState, const QString& udi);
    void                    timeToEmptyChanged (qlonglong time, const QString& udi);
    void                    timeToFullChanged (qlonglong time, const QString& udi);
    void                    voltageChanged (double voltage, const QString& udi);
    void                    temperatureChanged (double temperature, const QString& udi);
};
};
