class HoldingRegisterDefinitions:
    """
    Encapsulates all known holding registers from 0x0000 to 0x0115.
    Each entry is a dict:
      {
        'address': 0x0000,
        'length': 7,
        'description': 'some text',
        'scale': (float),
        'unit': (str),
        'signed': (bool)
      }
    'scale', 'unit', 'signed' are optional, used for single-register numeric scaling.
    'length' > 1 => multi-register ASCII text block or reserved data.
    """

    def __init__(self):
        self._registers = [

            # Multi-register ASCII blocks
            {"address": 0x0000, "length": 7, "description": "SeriesNumber (14 chars)"},
            {"address": 0x0007, "length": 7, "description": "FactoryName (14 chars)"},
            {"address": 0x000E, "length": 7, "description": "ModuleName (14 chars)"},

            # Single registers with scaling or special logic
            {"address": 0x0015, "length": 1, "description": "VpvStart(Hybrid)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0016, "length": 1, "description": "TimeStart", "scale": 1.0, "unit": "s", "signed": False},
            {"address": 0x0017, "length": 1, "description": "VpvHighStop(Hybrid)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0018, "length": 1, "description": "VpvLowStop(Hybrid)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0019, "length": 1, "description": "VacMinProtect", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x001A, "length": 1, "description": "VacMaxProtect", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x001B, "length": 1, "description": "FacMinProtect", "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x001C, "length": 1, "description": "FacMaxProtect", "scale": 0.01, "unit": "Hz", "signed": False},
            # 0x001D => Safety Type (mapped in code)
            {"address": 0x001D, "length": 1, "description": "Safety Type (Numeric + String)"},

            {"address": 0x001E, "length": 1, "description": "REV"},
            {"address": 0x001F, "length": 1, "description": "Grid10MinAvgProtect", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0020, "length": 1, "description": "VacMinSlowProtect", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0021, "length": 1, "description": "VacMaxSlowProtect", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0022, "length": 1, "description": "FacMinSlowProtect", "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x0023, "length": 1, "description": "FacMaxSlowProtect", "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x0024, "length": 1, "description": "DciLimits", "scale": 1.0, "unit": "mA", "signed": False},
            {"address": 0x0025, "length": 1, "description": "PowerLimitsPercent", "scale": 1.0, "unit": "%", "signed": False},
            {"address": 0x0026, "length": 1, "description": "PowerfactorMode"},
            {"address": 0x0027, "length": 1, "description": "PowerfactorData", "scale": 0.01, "unit": "", "signed": False},
            {"address": 0x0028, "length": 1, "description": "UpperLimit(Overexcite)", "scale": 0.01, "unit": "", "signed": False},
            {"address": 0x0029, "length": 1, "description": "LowerLimit(Underexcite)", "scale": 0.01, "unit": "", "signed": False},
            {"address": 0x002A, "length": 1, "description": "PowerLow", "scale": 0.01, "unit": "", "signed": False},
            {"address": 0x002B, "length": 1, "description": "PowerUp", "scale": 0.01, "unit": "", "signed": False},

            # 0x002C ~ 0x007B => 80 => multi
            {"address": 0x002C, "length": 80, "description": "PowerManagerConfigData(80 regs)"},

            {"address": 0x007C, "length": 1, "description": "PowerManagerEnable"},
            {"address": 0x007D, "length": 1, "description": "FirmwareVersion_InverterMaster"},
            {"address": 0x007E, "length": 4, "description": "REV(0x007E~0x0081)"},

            {"address": 0x0082, "length": 1, "description": "FirmwareVersion_ModbusTCP_minor"},
            {"address": 0x0083, "length": 1, "description": "FirmwareVersion_Manager"},
            {"address": 0x0084, "length": 1, "description": "FirmwareVersion_Manager_Bootloader"},
            {"address": 0x0085, "length": 1, "description": "RTC-Seconds", "scale": 1.0, "unit": "sec", "signed": False},
            {"address": 0x0086, "length": 1, "description": "RTC-Minutes", "scale": 1.0, "unit": "min", "signed": False},
            {"address": 0x0087, "length": 1, "description": "RTC-Hours",   "scale": 1.0, "unit": "h",   "signed": False},
            {"address": 0x0088, "length": 1, "description": "RTC-Days",    "scale": 1.0, "unit": "day", "signed": False},
            {"address": 0x0089, "length": 1, "description": "RTC-Months",  "scale": 1.0, "unit": "mon", "signed": False},
            {"address": 0x008A, "length": 1, "description": "RTC-Years",   "scale": 1.0, "unit": "year","signed": False},

            {"address": 0x008B, "length": 1, "description": "SolarChargerUseMode"},
            {"address": 0x008C, "length": 1, "description": "Battery_MinCapacity", "scale": 1.0, "unit": "%", "signed": False},
            {"address": 0x008D, "length": 1, "description": "wBattery1_Type"},
            {"address": 0x008E, "length": 1, "description": "Charge_floatVolt", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x008F, "length": 1, "description": "Battery_DischargeCutVoltage", "scale": 0.1, "unit": "V", "signed": False},

            {"address": 0x0090, "length": 1, "description": "Battery_ChargeMaxCurrent",    "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0091, "length": 1, "description": "Battery_DischargeMaxCurrent", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0092, "length": 1, "description": "ChargerStartTime1_Hours",     "scale": 1.0,"unit": "h","signed": False},
            {"address": 0x0093, "length": 1, "description": "ChargerStartTime1_Min",       "scale": 1.0,"unit": "min","signed":False},
            {"address": 0x0094, "length": 1, "description": "ChargerEndTime1_Hours",       "scale": 1.0,"unit": "h","signed":False},
            {"address": 0x0095, "length": 1, "description": "ChargerEndTime1_Min",         "scale": 1.0,"unit": "min","signed":False},

            {"address": 0x0096, "length": 4, "description": "REV(0x0096~0x0099)"},
            {"address": 0x009A, "length": 1, "description": "ChargerStartTime2_Hours", "scale": 1.0,"unit": "h","signed":False},
            {"address": 0x009B, "length": 1, "description": "ChargerStartTime2_Min",   "scale": 1.0,"unit": "min","signed":False},
            {"address": 0x009C, "length": 1, "description": "ChargerEndTime2_Hours",  "scale": 1.0,"unit": "h","signed":False},
            {"address": 0x009D, "length": 1, "description": "ChargerEndTime2_Min",    "scale": 1.0,"unit": "min","signed":False},

            {"address": 0x009E, "length": 4, "description": "REV(0x009E~0x00A1)"},
            {"address": 0x00A2, "length": 1, "description": "MAC address part1"},
            {"address": 0x00A3, "length": 1, "description": "MAC address part2"},
            {"address": 0x00A4, "length": 1, "description": "MAC address part3"},
            {"address": 0x00A5, "length": 1, "description": "REV(0x00A5)"},
            {"address": 0x00A6, "length": 1, "description": "ModbusPowerControl"},
            {"address": 0x00A7, "length": 1, "description": "absorpt_voltage","scale":0.1,"unit":"V","signed":False},

            {"address": 0x00A8, "length": 7, "description": "REV(0x00A8~0x00AE)"},
            {"address": 0x00AF, "length": 5, "description": "Registration code(10 chars)"},

            {"address": 0x00B4, "length": 1, "description": "Allow_Grid_Charge"},
            {"address": 0x00B5, "length": 1, "description": "Export control_factory limit", "scale":1.0,"unit":"W","signed":False},
            {"address": 0x00B6, "length": 1, "description": "Export control user limit",    "scale":1.0,"unit":"W","signed":False},
            {"address": 0x00B7, "length": 1, "description": "EPS_Mute"},
            {"address": 0x00B8, "length": 1, "description": "EPS Frequency"},
            {"address": 0x00B9, "length": 1, "description": "REV(0x00B9)"},
            {"address": 0x00BA, "length": 1, "description": "Inverter Type", "scale":1.0,"unit":"W","signed":False},
            {"address": 0x00BB, "length": 1, "description": "Language(for screen)"},
            {"address": 0x00BC, "length": 1, "description": "IP Method"},
            {"address": 0x00BD, "length": 1, "description": "wTimeVacMin_FastAdj", "scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00BE, "length": 1, "description": "wTimeVacMax_FastAdj", "scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00BF, "length": 1, "description": "wTimeFacMin_FastAdj", "scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00C0, "length": 1, "description": "wTimeFacMax_FastAdj", "scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00C1, "length": 1, "description": "wTimeVacMin_SlowAdj","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00C2, "length": 1, "description": "wTimeVacMax_SlowAdj","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00C3, "length": 1, "description": "wTimeFacMin_SlowAdj","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00C4, "length": 1, "description": "wTimeFacMax_SlowAdj","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00C5, "length": 1, "description": "TestStep(SelfTest enum)"},
            {"address": 0x00C6, "length": 1, "description": "OvpValue(59.S2)","scale":0.1,"unit":"V","signed":False},
            {"address": 0x00C7, "length": 1, "description": "OvpTime(59.S2)","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00C8, "length": 1, "description": "UvpValue(27.S1)","scale":0.1,"unit":"V","signed":False},
            {"address": 0x00C9, "length": 1, "description": "UvpTime(27.S1)","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00CA, "length": 1, "description": "OfpValue(81>.S1)","scale":0.01,"unit":"Hz","signed":False},
            {"address": 0x00CB, "length": 1, "description": "OfpTime(81>.S1)","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00CC, "length": 1, "description": "UfpValue(81<.S1)","scale":0.01,"unit":"Hz","signed":False},
            {"address": 0x00CD, "length": 1, "description": "UfpTime(81<.S1)","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00CE, "length": 1, "description": "SelfTestOvp10mAvgVal(59.S1)","scale":0.1,"unit":"V","signed":False},
            {"address": 0x00CF, "length": 1, "description": "SelfTestOvp10mAvgTime(59.S1)","scale":1.0,"unit":"s","signed":False},
            {"address": 0x00D0, "length": 1, "description": "SelfTestOfpVal_Restrictive(81>.S2)","scale":0.01,"unit":"Hz","signed":False},
            {"address": 0x00D1, "length": 1, "description": "SelfTestOfpTime_Restrictive(81>.S2)","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00D2, "length": 1, "description": "SelfTestUfpVal_Restrictive(81<.S2)","scale":0.01,"unit":"Hz","signed":False},
            {"address": 0x00D3, "length": 1, "description": "SelfTestUfpTime_Restrictive(81<.S2)","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00D4, "length": 1, "description": "SelfTest_UvpRestrictive_Val(27.S2)","scale":0.1,"unit":"V","signed":False},
            {"address": 0x00D5, "length": 1, "description": "SelfTest_UvpRestrictive_Time(27.S2)","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00D6, "length": 1, "description": "SelfTest_Time","scale":1.0,"unit":"s","signed":False},
            {"address": 0x00D7, "length": 1, "description": "REV(0x00D7)"},
            {"address": 0x00D8, "length": 1, "description": "PfLockInPoint"},
            {"address": 0x00D9, "length": 1, "description": "PfLockOutPoint"},
            {"address": 0x00DA, "length": 1, "description": "wInverter_OutPut_Switch"},
            {"address": 0x00DB, "length": 1, "description": "FreqSetPoint","scale":0.01,"unit":"Hz","signed":False},
            {"address": 0x00DC, "length": 1, "description": "FreqDroopRate","scale":1.0,"unit":"%","signed":False},
            {"address": 0x00DD, "length": 1, "description": "FreDroopDelayTime","scale":1.0,"unit":"ms","signed":False},
            {"address": 0x00DE, "length": 1, "description": "QuVrateUp","scale":1.0,"unit":"%","signed":False},
            {"address": 0x00DF, "length": 1, "description": "QuVrateLow","scale":1.0,"unit":"%","signed":False},

            {"address": 0x00E0, "length": 19, "description": "REV(0x00E0~0x00F2)"},

            {"address": 0x00F3, "length": 1, "description": "wPowerLimitGra","scale":0.0001,"unit":"","signed":False},
            {"address": 0x00F4, "length": 1, "description": "VoltResponse_V2","scale":0.1,"unit":"V","signed":False},
            {"address": 0x00F5, "length": 1, "description": "VoltResponse_V3","scale":0.1,"unit":"V","signed":False},
            {"address": 0x00F6, "length": 1, "description": "VoltResponse_V4","scale":0.1,"unit":"V","signed":False},
            {"address": 0x00F7, "length": 1, "description": "VoltResponse_Ratio1","scale":0.01,"unit":"","signed":False},
            {"address": 0x00F8, "length": 1, "description": "VoltResponse_Ratio4","scale":0.01,"unit":"","signed":False},
            {"address": 0x00F9, "length": 1, "description": "PUFuncEnable"},
            {"address": 0x00FA, "length": 1, "description": "Qpower_set","scale":1.0,"unit":"Var","signed":False},
            {"address": 0x00FB, "length": 1, "description": "bQpower_set_Max","scale":1.0,"unit":"Var","signed":False},
            {"address": 0x00FC, "length": 1, "description": "bQpower_set_Min","scale":1.0,"unit":"Var","signed":False},

            {"address": 0x00FD, "length": 1, "description": "BackUp_GridChargeEN"},
            {"address": 0x00FE, "length": 1, "description": "BackUp_chr_Strat_H","scale":1.0,"unit":"h","signed":False},
            {"address": 0x00FF, "length": 1, "description": "BackUp_chr_Strat_M","scale":1.0,"unit":"min","signed":False},
            {"address": 0x0100, "length": 1, "description": "BackUp_chr_End_H","scale":1.0,"unit":"h","signed":False},
            {"address": 0x0101, "length": 1, "description": "BackUp_chr_End_M","scale":1.0,"unit":"min","signed":False},

            {"address": 0x0102, "length": 1, "description": "wAS4777PowerManagerEnable"},
            {"address": 0x0103, "length": 1, "description": "CloudControlEN"},
            {"address": 0x0104, "length": 1, "description": "wGlobalMPPTFuncEnable(X1)"},
            {"address": 0x0105, "length": 1, "description": "Grid service(X3)"},
            {"address": 0x0106, "length": 1, "description": "PhasePowerBalance(X3)"},
            {"address": 0x0107, "length": 1, "description": "wMachineStyle"},
            {"address": 0x0108, "length": 1, "description": "MeterFunction"},
            {"address": 0x0109, "length": 1, "description": "Meter1ID","scale":1.0,"unit":"","signed":False},
            {"address": 0x010A, "length": 1, "description": "Meter2ID","scale":1.0,"unit":"","signed":False},
            {"address": 0x010B, "length": 1, "description": "PowerControl_timeout","scale":1.0,"unit":"s","signed":False},
            {"address": 0x010C, "length": 1, "description": "EPS_AutoRestart"},
            {"address": 0x010D, "length": 1, "description": "EPS_MinEscVolt","scale":1.0,"unit":"V","signed":False},
            {"address": 0x010E, "length": 1, "description": "EPS_MinEscSoc","scale":1.0,"unit":"%","signed":False},
            {"address": 0x010F, "length": 1, "description": "ForceTimeUse_P1_MaxCapacity","scale":1.0,"unit":"%","signed":False},
            {"address": 0x0110, "length": 1, "description": "ForceTimeUse_P2_MaxCapacity","scale":1.0,"unit":"%","signed":False},
            {"address": 0x0111, "length": 1, "description": "DischCutOffPoint_DifferentEN"},
            {"address": 0x0112, "length": 1, "description": "DischCutOffCapacity_GridMode","scale":1.0,"unit":"%","signed":False},
            {"address": 0x0113, "length": 1, "description": "DischCutOffVoltage_GridMode","scale":0.1,"unit":"V","signed":False},
            {"address": 0x0114, "length": 1, "description": "wEarthDetectEn(X3)"},
            {"address": 0x0115, "length": 1, "description": "CTMeterSetting(X1)"},
        ]

    def get_registers(self):
        """Return the entire list of holding register definitions."""
        return self._registers
