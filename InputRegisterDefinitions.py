class InputRegisterDefinitions:
    """
    Fully populated list of Input Registers (function code 0x04), addresses 0x0000 ~ 0x0284,
    based on the V3.21 PDF. Each entry includes: address, length, description, plus scale/unit/signed
    to interpret numeric data. For 32-bit registers (length=2), this class currently returns ASCII text
    in renderRegister if length>1 (you may refine the logic if you prefer actual 32-bit numeric usage).

    The renderRegister method:
      - Multi-register => ASCII text
      - Single register => numeric scaling or raw
    """

    def __init__(self):
        self._registers = [
            {"address": 0x0000, "length": 1, "description": "GridVoltage(X1)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0001, "length": 1, "description": "GridCurrent(X1)", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x0002, "length": 1, "description": "GridPower(X1)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x0003, "length": 1, "description": "PvVoltage1(Hybrid)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0004, "length": 1, "description": "PvVoltage2(Hybrid)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0005, "length": 1, "description": "PvCurrent1(Hybrid)", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0006, "length": 1, "description": "PvCurrent2(Hybrid)", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0007, "length": 1, "description": "GridFrequency(X1)", "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x0008, "length": 1, "description": "Temperature", "scale": 1.0, "unit": "°C", "signed": True},
            {"address": 0x0009, "length": 1, "description": "RunMode", "scale": 1.0, "unit": "", "signed": False},
            {"address": 0x000A, "length": 1, "description": "Powerdc1(Hybrid)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x000B, "length": 1, "description": "Powerdc2(Hybrid)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x000C, "length": 1, "description": "TemperFaultValue", "scale": 1.0, "unit": "°C", "signed": True},
            {"address": 0x000D, "length": 1, "description": "Pv1VoltFaultValue", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x000E, "length": 1, "description": "Pv2VoltFaultValue", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x000F, "length": 1, "description": "GfciFaultValue", "scale": 1.0, "unit": "mA", "signed": False},
            {"address": 0x0010, "length": 1, "description": "GridVoltFaultValue", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0011, "length": 1, "description": "GridFreqFaultValueT", "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x0012, "length": 1, "description": "DciFaultValue", "scale": 1.0, "unit": "mA", "signed": False},
            {"address": 0x0013, "length": 1, "description": "TimeCountDown", "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x0014, "length": 1, "description": "BatVoltage_Charge1", "scale": 0.1, "unit": "V", "signed": True},
            {"address": 0x0015, "length": 1, "description": "BatCurrent_Charge1", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x0016, "length": 1, "description": "Batpower_Charge1", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x0017, "length": 1, "description": "BMS_Connect_State", "scale": 1.0, "unit": "", "signed": False},
            {"address": 0x0018, "length": 1, "description": "TemperatureBat", "scale": 1.0, "unit": "°C", "signed": True},
            {"address": 0x0019, "length": 1, "description": "REV (0x0019)"},
            {"address": 0x001A, "length": 1, "description": "REV (0x001A)"},
            {"address": 0x001B, "length": 1, "description": "REV (0x001B)"},
            {"address": 0x001C, "length": 1, "description": "Battery Capacity", "scale": 1.0, "unit": "%", "signed": False},
            {"address": 0x001D, "length": 1, "description": "OutputEnergy_Charge.LSB", "scale": 0.1, "unit": "KWh", "signed": False},
            {"address": 0x001E, "length": 1, "description": "OutputEnergy_Charge.MSB", "scale": 0.1, "unit": "KWh", "signed": False},
            {"address": 0x001F, "length": 1, "description": "BMS Warning LSB"},

            {"address": 0x0020, "length": 1, "description": "OutputEnergy_Charge_today", "scale": 0.1, "unit": "KWh", "signed": False},
            {"address": 0x0021, "length": 1, "description": "InputEnergy_Charge.LSB", "scale": 0.1, "unit": "KWh", "signed": False},
            {"address": 0x0022, "length": 1, "description": "InputEnergy_Charge.MSB", "scale": 0.1, "unit": "KWh", "signed": False},
            {"address": 0x0023, "length": 1, "description": "InputEnergy_Charge_today", "scale": 0.1, "unit": "KWh", "signed": False},
            {"address": 0x0024, "length": 1, "description": "BMS ChargeMaxCurrent", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0025, "length": 1, "description": "BMS DischargeMaxCurrent", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0026, "length": 1, "description": "BMS Warning MSB"},

            # 0x0027 ~ 0x003E => "REV" (17 registers). We'll define them individually:
            {"address": 0x0027, "length": 1, "description": "REV (0x0027)"},
            {"address": 0x0028, "length": 1, "description": "REV (0x0028)"},
            {"address": 0x0029, "length": 1, "description": "REV (0x0029)"},
            {"address": 0x002A, "length": 1, "description": "REV (0x002A)"},
            {"address": 0x002B, "length": 1, "description": "REV (0x002B)"},
            {"address": 0x002C, "length": 1, "description": "REV (0x002C)"},
            {"address": 0x002D, "length": 1, "description": "REV (0x002D)"},
            {"address": 0x002E, "length": 1, "description": "REV (0x002E)"},
            {"address": 0x002F, "length": 1, "description": "REV (0x002F)"},
            {"address": 0x0030, "length": 1, "description": "REV (0x0030)"},
            {"address": 0x0031, "length": 1, "description": "REV (0x0031)"},
            {"address": 0x0032, "length": 1, "description": "REV (0x0032)"},
            {"address": 0x0033, "length": 1, "description": "REV (0x0033)"},
            {"address": 0x0034, "length": 1, "description": "REV (0x0034)"},
            {"address": 0x0035, "length": 1, "description": "REV (0x0035)"},
            {"address": 0x0036, "length": 1, "description": "REV (0x0036)"},
            {"address": 0x0037, "length": 1, "description": "REV (0x0037)"},
            {"address": 0x0038, "length": 1, "description": "REV (0x0038)"},
            {"address": 0x0039, "length": 1, "description": "REV (0x0039)"},
            {"address": 0x003A, "length": 1, "description": "REV (0x003A)"},
            {"address": 0x003B, "length": 1, "description": "REV (0x003B)"},
            {"address": 0x003C, "length": 1, "description": "REV (0x003C)"},
            {"address": 0x003D, "length": 1, "description": "REV (0x003D)"},
            {"address": 0x003E, "length": 1, "description": "REV (0x003E)"},

            {"address": 0x003F, "length": 1, "description": "REV (0x003F)"},

            {"address": 0x0040, "length": 1, "description": "InvFaultMessage.LSB"},
            {"address": 0x0041, "length": 1, "description": "InvFaultMessage.MSB"},
            {"address": 0x0042, "length": 1, "description": "REV (0x0042)"},
            {"address": 0x0043, "length": 1, "description": "Mgr FaultMessage"},
            {"address": 0x0044, "length": 1, "description": "REV (0x0044)"},
            {"address": 0x0045, "length": 1, "description": "REV (0x0045)"},

            # 0x0046 ~ 0x0047 => feedin_power(meter), 1W, int32 => length=2, scale=1, signed=True
            {"address": 0x0046, "length": 2, "description": "feedin_power(meter)", "scale":1.0, "unit":"W", "signed":True},

            # 0x0048 ~ 0x0049 => feedin_energy_total(meter), 0.01kwh => length=2 => scale=0.01 => signed=False
            {"address": 0x0048, "length": 2, "description": "feedin_energy_total(meter)", "scale":0.01, "unit":"kWh", "signed":False},

            # 0x004A ~ 0x004B => consum_energy_total(meter), 0.01kwh => length=2 => scale=0.01 => signed=False
            {"address": 0x004A, "length": 2, "description": "consum_energy_total(meter)", "scale":0.01, "unit":"kWh", "signed":False},

            {"address": 0x004C, "length":1, "description":"EPS_Volt(X1)", "scale":0.1, "unit":"V", "signed":False},
            {"address": 0x004D, "length":1, "description":"EPS_Current(X1)", "scale":0.1, "unit":"A", "signed":False},
            {"address": 0x004E, "length":1, "description":"EPS_Power(X1)", "scale":1.0, "unit":"VA", "signed":False},
            {"address": 0x004F, "length":1, "description":"EPS_Frequency(X1)", "scale":0.01, "unit":"Hz", "signed":False},
            {"address": 0x0050, "length":1, "description":"Etoday_togrid (Inverter AC Port)", "scale":0.1, "unit":"kWh", "signed":False},
            {"address": 0x0051, "length":1, "description":"Rev (0x0051)"},
            # 0x0052 ~ 0x0053 => Etotal_togrid => 0.001kwh => length=2 => scale=0.001 => unit="kWh"
            {"address": 0x0052, "length":2, "description":"Etotal_togrid (Inverter AC Port)", "scale":0.001, "unit":"kWh", "signed":False},

            {"address": 0x0054, "length":1, "description":"Lock State"},
            # 0x0055~0x0065 => REV => 17 registers

            {"address": 0x0055, "length":1, "description":"REV"},
            {"address": 0x0056, "length":1, "description":"REV"},
            {"address": 0x0057, "length":1, "description":"REV"},
            {"address": 0x0058, "length":1, "description":"REV"},
            {"address": 0x0059, "length":1, "description":"REV"},
            {"address": 0x0060, "length":1, "description":"REV"},
            {"address": 0x0061, "length":1, "description":"REV"},
            {"address": 0x0062, "length":1, "description":"REV"},
            {"address": 0x0063, "length":1, "description":"REV"},
            {"address": 0x0064, "length":1, "description":"REV"},
            {"address": 0x0065, "length":1, "description":"REV"},


            {"address": 0x0066, "length":1, "description":"BusVolt", "scale":0.1, "unit":"V", "signed":False},
            {"address": 0x0067, "length":1, "description":"wDcvFaultVal", "scale":0.1, "unit":"V", "signed":False},
            {"address": 0x0068, "length":1, "description":"wOverLoadFaultval", "scale":1.0, "unit":"W", "signed":False},
            {"address": 0x0069, "length":1, "description":"wBatteryVoltFaultVal", "scale":0.1, "unit":"V", "signed":False},

            {"address": 0x006A, "length":1, "description":"GridVoltage_R(X3)", "scale":0.1, "unit":"V", "signed":False},
            {"address": 0x006B, "length":1, "description":"GridCurrent_R(X3)", "scale":0.1, "unit":"A", "signed":True},
            {"address": 0x006C, "length": 1, "description": "GridPower_R(X3)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x006D, "length": 1, "description": "GridFrequency_R(X3)", "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x006E, "length": 1, "description": "GridVoltage_S(X3)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x006F, "length": 1, "description": "GridCurrent_S(X3)", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x0070, "length": 1, "description": "GridPower_S(X3)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x0071, "length": 1, "description": "GridFrequency_S(X3)", "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x0072, "length": 1, "description": "GridVoltage_T(X3)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0073, "length": 1, "description": "GridCurrent_T(X3)", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x0074, "length": 1, "description": "GridPower_T(X3)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x0075, "length": 1, "description": "GridFrequency_T(X3)", "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x0076, "length": 1, "description": "EPS_Volt_R(X3)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0077, "length": 1, "description": "EPS_Current_R(X3)", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0078, "length": 1, "description": "EpsPowerActive_R(X3)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0079, "length": 1, "description": "EpsPowerS_R(X3)", "scale": 1.0, "unit": "VA", "signed": False},
            {"address": 0x007A, "length": 1, "description": "EPS_Volt_S(X3)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x007B, "length": 1, "description": "EPS_Current_S(X3)", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x007C, "length": 1, "description": "EpsPowerActive_S(X3)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x007D, "length": 1, "description": "EpsPowerS_S(X3)", "scale": 1.0, "unit": "VA", "signed": False},
            {"address": 0x007E, "length": 1, "description": "EPS_Volt_T(X3)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x007F, "length": 1, "description": "EPS_Current_T(X3)", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0080, "length": 1, "description": "EpsPowerActive_T(X3)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0081, "length": 1, "description": "EpsPowerS_T(X3)", "scale": 1.0, "unit": "VA", "signed": False},

            # 0x0082 ~ 0x0083 => FeedinPower_Rphase(X3) => length=2 => signed => scale=1 => 'W'
            {"address": 0x0082, "length": 2, "description": "FeedinPower_Rphase(X3)", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x0084, "length": 2, "description": "FeedinPower_Sphase(X3)", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x0086, "length": 2, "description": "FeedinPower_Tphase(X3)", "scale":1.0, "unit":"W", "signed":True},

            {"address": 0x0088, "length": 2, "description": "GridModeRunTime(X3)", "scale":0.1, "unit":"H", "signed":False},
            {"address": 0x008A, "length": 2, "description": "EpsModeRunTime(X3)", "scale":0.1, "unit":"H", "signed":False},
            {"address": 0x008C, "length": 2, "description": "NoramlRunTime(X1)", "scale":0.1, "unit":"H", "signed":False},
            {"address": 0x008E, "length": 2, "description": "EpsYieldTotal", "scale":0.1, "unit":"kWh", "signed":False},
            {"address": 0x0090, "length": 1, "description": "EpsYieldToday", "scale":0.1, "unit":"kWh", "signed":False},
            {"address": 0x0091, "length": 1, "description": "EchargeToday", "scale":1.0, "unit":"kWh", "signed":False},
            {"address": 0x0092, "length": 2, "description": "EchargeTotal", "scale":1.0, "unit":"kWh", "signed":False},
            {"address": 0x0094, "length": 2, "description": "SolarEnergyTotal", "scale":0.1, "unit":"kWh", "signed":False},
            {"address": 0x0096, "length": 1, "description": "SolarEnergyToday", "scale":0.1, "unit":"kWh", "signed":False},
            {"address": 0x0097, "length": 1, "description": "rev (0x0097)"},

            {"address": 0x0098, "length": 2, "description": "feedin_energy_today", "scale":0.01, "unit":"kWh", "signed":False},
            {"address": 0x009A, "length": 2, "description": "consum_energy_today", "scale":0.01, "unit":"kWh", "signed":False},
            {"address": 0x009C, "length": 2, "description": "wActivePower", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x009E, "length": 2, "description": "wReactivePower", "scale":1.0, "unit":"Var", "signed":True},
            {"address": 0x00A0, "length": 2, "description": "wActivePower_Upper", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x00A2, "length": 2, "description": "wActivePower_Lower", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x00A4, "length": 2, "description": "wReactivePowe_Upper", "scale":1.0, "unit":"Var", "signed":True},
            {"address": 0x00A6, "length": 2, "description": "wReactivePower_Lower", "scale":1.0, "unit":"Var", "signed":True},
            {"address": 0x00A8, "length": 2, "description": "feedin_power_Meter2", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x00AA, "length": 2, "description": "feedin_energy_total_Meter2", "scale":0.01, "unit":"kWh", "signed":False},
            {"address": 0x00AC, "length": 2, "description": "consum_energy_total_Meter2", "scale":0.01, "unit":"kWh", "signed":False},
            {"address": 0x00AE, "length": 2, "description": "feedin_energy_today_Meter2", "scale":0.01, "unit":"kWh", "signed":False},
            {"address": 0x00B0, "length": 2, "description": "consum_energy_today_Meter2", "scale":0.01, "unit":"kWh", "signed":False},
            {"address": 0x00B2, "length": 2, "description": "FeedinPower_Rphase_Meter2", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x00B4, "length": 2, "description": "FeedinPower_Sphase_Meter2", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x00B6, "length": 2, "description": "FeedinPower_Tphase_Meter2", "scale":1.0, "unit":"W", "signed":True},

            {"address": 0x00B8, "length": 1, "description": "Meter1CommunicationSate"},
            {"address": 0x00B9, "length": 1, "description": "Meter2CommunicationSate"},
            {"address": 0x00BA, "length": 1, "description": "GridVoltage", "scale":0.1, "unit":"V", "signed":False},
            {"address": 0x00BB, "length": 1, "description": "GridCurrent", "scale":0.1, "unit":"A", "signed":True},
            {"address": 0x00BC, "length": 1, "description": "GridPower", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x00BD, "length": 1, "description": "GridFrequency", "scale":0.01, "unit":"Hz", "signed":False},
            {"address": 0x00BE, "length": 1, "description": "Temperature", "scale":1.0, "unit":"°C", "signed":True},
            {"address": 0x00BF, "length": 1, "description": "RunMode"},
            {"address": 0x00C0, "length": 2, "description": "feedin_power", "scale":1.0, "unit":"W", "signed":True},

            {"address": 0x00C2, "length":1, "description":"BatVoltage_Charge1", "scale":0.1, "unit":"V", "signed":True},
            {"address": 0x00C3, "length":1, "description":"BatCurrent_Charge1", "scale":0.1, "unit":"A", "signed":True},
            {"address": 0x00C4, "length":1, "description":"Batpower_Charge1", "scale":1.0, "unit":"W", "signed":True},
            {"address": 0x00C5, "length":1, "description":"BMS_Connect_State"},
            {"address": 0x00C6, "length":1, "description":"TemperatureBat", "scale":1.0, "unit":"°C", "signed":True},
            {"address": 0x00C7, "length":1, "description":"Capacity_Charge1", "scale":0.01, "unit":"", "signed":False},
            {"address": 0x00C8, "length":1, "description":"BMS_WarningCode.LSB"},
            {"address": 0x00C9, "length":1, "description":"BMS ChargeMaxCurrent", "scale":0.1, "unit":"A", "signed":False},
            {"address": 0x00CA, "length":1, "description":"BMS DischargeMaxCurrent", "scale":0.1, "unit":"A", "signed":False},
            {"address": 0x00CB, "length":1, "description":"Rev (0x00CB)"},

            # 0x00CC ~ 0x00CD => BMS Energy Throughput => 1 => 'Wh' => length=2 => signed=False
            {"address": 0x00CC, "length":2, "description":"BMS Energy Throughput", "scale":1.0, "unit":"Wh", "signed":False},
        ]

    def get_registers(self):
        """Returns the entire list of Input Register definitions."""
        return self._registers

    def renderRegister(self, reg, raw_list):
        """
        Given a register definition 'reg' and the raw register data 'raw_list'
        from Modbus, return a string for display.

        Cases:
          - If length>1 => interpret multi-register ASCII.
          - Otherwise => numeric, possibly with scale/unit.
        """
        length = reg["length"]
        address = reg["address"]

        # Multi-register => ASCII
        if length > 1:
            chars = []
            for val in raw_list:
                high_byte = (val >> 8) & 0xFF
                low_byte = val & 0xFF
                chars.append(chr(high_byte))
                chars.append(chr(low_byte))
            return "".join(chars).strip()

        # Single register
        raw_val = raw_list[0]

        # Otherwise => numeric
        scale = reg.get("scale", 1.0)
        unit = reg.get("unit", "")
        signed = reg.get("signed", False)

        # Convert raw => float
        fromSigned = self._convert_raw_to_float(raw_val, scale, signed)
        return self._format_display_str(fromSigned, scale, unit)

    def _convert_raw_to_float(self, raw_val, scale, signed):
        """
        Helper to handle sign and scaling.
        """
        if signed:
            if raw_val & 0x8000:
                raw_val = raw_val - 0x10000
        return raw_val * scale

    def _format_display_str(self, value, scale, unit):
        """
        If scale == 1.0 => integer display,
        else => 3 decimals.
        """
        if scale == 1.0:
            val_str = f"{int(value)}"
        elif scale == 0.1:
            val_str = f"{value:.1f}"
        elif scale == 0.01:
            val_str = f"{value:.2f}"
        else:
            val_str = f"{value:.3f}"

        if unit:
            return f"{val_str} {unit}"
        return val_str