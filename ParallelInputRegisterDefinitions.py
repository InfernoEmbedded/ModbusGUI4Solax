class ParallelInputRegisterDefinitions:
    """
    Parallel input registers (Function code 0x04), addresses 0x01DD ~ 0x0284.
    Based on section "6. Read Input Register(Parallel State)" in the PDF.
    """

    def __init__(self):
        self._registers = [
            # 0x01DD => SystemInvNum (1)
            {"address": 0x01DD, "length": 1, "description": "SystemInvNum", "scale": 1.0, "unit": "", "signed": False},

            # 0x01DE ~ 0x01DF => Rev
            {"address": 0x01DE, "length": 1, "description": "Rev(0x01DE)"},
            {"address": 0x01DF, "length": 1, "description": "Rev(0x01DF)"},

            # 0x01E0 => InvActivePower_R_All => int32 => 2 regs => scale=1 => "W" => signed
            {"address": 0x01E0, "length": 2, "description": "InvActivePower_R_All", "scale": 1.0, "unit": "W", "signed": True},

            # 0x01E2 => InvActivePower_S_All => also 2 regs => ...
            {"address": 0x01E2, "length": 2, "description": "InvActivePower_S_All", "scale": 1.0, "unit": "W", "signed": True},

            # 0x01E4 => InvActivePower_T_All => ...
            {"address": 0x01E4, "length": 2, "description": "InvActivePower_T_All", "scale": 1.0, "unit": "W", "signed": True},

            # 0x01E6 => InvReactiveOrApparentPower_R_All => 2 regs => 1VA => possibly signed or not?
            {"address": 0x01E6, "length": 2, "description": "InvReactiveOrApparentPower_R_All", "scale": 1.0, "unit": "VA", "signed": True},
            {"address": 0x01E8, "length": 2, "description": "InvReactiveOrApparentPower_S_All", "scale": 1.0, "unit": "VA", "signed": True},
            {"address": 0x01EA, "length": 2, "description": "InvReactiveOrApparentPower_T_All", "scale": 1.0, "unit": "VA", "signed": True},

            # 0x01EC => InvCurrent_R_All => 0.1A => 2 regs => int32 => possibly signed => doc says "0.1A int32"
            {"address": 0x01EC, "length": 2, "description": "InvCurrent_R_All", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x01EE, "length": 2, "description": "InvCurrent_S_All", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x01F0, "length": 2, "description": "InvCurrent_T_All", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x01F2, "length": 2, "description": "PvPower_ChannelA_All", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x01F4, "length": 2, "description": "PvPower_ChannelB_All", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x01F6, "length": 2, "description": "PvCurrent_ChannelA_All", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x01F8, "length": 2, "description": "PvCurrent_ChannelB_All", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x01FA, "length": 2, "description": "BatPower_All", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x01FC, "length": 2, "description": "BatCurrent_All", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x01FE, "length": 2, "description": "ChargePowerLimit_All", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x0200, "length": 2, "description": "DischargePowerLimit_All", "scale": 1.0, "unit": "W", "signed": True},

            # 0x0202~0x0203 => Rev
            {"address": 0x0202, "length": 1, "description": "Rev(0x0202)"},
            {"address": 0x0203, "length": 1, "description": "Rev(0x0203)"},

            # 0x0204 => slave1 data => InvActivePower_R
            {"address": 0x0204, "length": 1, "description": "InvActivePower_R (slave1 data)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x0205, "length": 1, "description": "InvActivePower_S (slave1 data)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x0206, "length": 1, "description": "InvActivePower_T (slave1 data)", "scale": 1.0, "unit": "W", "signed": True},

            {"address": 0x0207, "length": 1, "description": "InvReactiveOrApparentPower_R", "scale": 1.0, "unit": "VA", "signed": True},
            {"address": 0x0208, "length": 1, "description": "InvReactiveOrApparentPower_S", "scale": 1.0, "unit": "VA", "signed": True},
            {"address": 0x0209, "length": 1, "description": "InvReactiveOrApparentPower_T", "scale": 1.0, "unit": "VA", "signed": True},

            {"address": 0x020A, "length": 1, "description": "InvCurrent_R", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x020B, "length": 1, "description": "InvCurrent_S", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x020C, "length": 1, "description": "InvCurrent_T", "scale": 0.1, "unit": "A", "signed": True},

            {"address": 0x020D, "length": 1, "description": "PvPower_ChannelA", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x020E, "length": 1, "description": "PvPower_ChannelB", "scale": 1.0, "unit": "W", "signed": False},

            {"address": 0x020F, "length": 1, "description": "PvVoltage_ChannelA", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0210, "length": 1, "description": "PvVoltage_ChannelB", "scale": 0.1, "unit": "V", "signed": False},

            {"address": 0x0211, "length": 1, "description": "PvCurrent_ChannelA", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0212, "length": 1, "description": "PvCurrent_ChannelB", "scale": 0.1, "unit": "A", "signed": False},

            {"address": 0x0213, "length": 1, "description": "BatPower", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0214, "length": 1, "description": "BatVoltage", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0215, "length": 1, "description": "BatCurrent", "scale": 0.1, "unit": "A", "signed": False},

            {"address": 0x0216, "length": 1, "description": "ChargePowerLimit", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0217, "length": 1, "description": "DischargePowerLimit", "scale": 1.0, "unit": "W", "signed": False},

            {"address": 0x0218, "length": 1, "description": "BatFaultMessage", "scale": 1.0, "unit": "", "signed": False},
            {"address": 0x0219, "length": 1, "description": "BatCapacity", "scale": 1.0, "unit": "%", "signed": False},

            # 0x021A~0x021B => Rev
            {"address": 0x021A, "length": 1, "description": "Rev(0x021A)"},
            {"address": 0x021B, "length": 1, "description": "Rev(0x021B)"},

            # 0x021C~0x021D => Rev
            {"address": 0x021C, "length": 1, "description": "Rev(0x021C)"},
            {"address": 0x021D, "length": 1, "description": "Rev(0x021D)"},

            # 0x021E => slave2 data => same pattern
            {"address": 0x021E, "length": 1, "description": "InvActivePower_R (slave2 data)", "scale": 1.0, "unit": "W", "signed": True},
            # slave2 data: 0x021E ~ 0x0237
            {"address": 0x021E, "length": 1, "description": "InvActivePower_R (slave2)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x021F, "length": 1, "description": "InvActivePower_S (slave2)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x0220, "length": 1, "description": "InvActivePower_T (slave2)", "scale": 1.0, "unit": "W", "signed": True},

            {"address": 0x0221, "length": 1, "description": "InvReactiveOrApparentPower_R (slave2)", "scale": 1.0, "unit": "VA", "signed": True},
            {"address": 0x0222, "length": 1, "description": "InvReactiveOrApparentPower_S (slave2)", "scale": 1.0, "unit": "VA", "signed": True},
            {"address": 0x0223, "length": 1, "description": "InvReactiveOrApparentPower_T (slave2)", "scale": 1.0, "unit": "VA", "signed": True},

            {"address": 0x0224, "length": 1, "description": "InvCurrent_R (slave2)", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x0225, "length": 1, "description": "InvCurrent_S (slave2)", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x0226, "length": 1, "description": "InvCurrent_T (slave2)", "scale": 0.1, "unit": "A", "signed": True},

            {"address": 0x0227, "length": 1, "description": "PvPower_ChannelA (slave2)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0228, "length": 1, "description": "PvPower_ChannelB (slave2)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0229, "length": 1, "description": "PvVoltage_ChannelA (slave2)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x022A, "length": 1, "description": "PvVoltage_ChannelB (slave2)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x022B, "length": 1, "description": "PvCurrent_ChannelA (slave2)", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x022C, "length": 1, "description": "PvCurrent_ChannelB (slave2)", "scale": 0.1, "unit": "A", "signed": False},

            {"address": 0x022D, "length": 1, "description": "BatPower (slave2)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x022E, "length": 1, "description": "BatVoltage (slave2)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x022F, "length": 1, "description": "BatCurrent (slave2)", "scale": 0.1, "unit": "A", "signed": False},

            {"address": 0x0230, "length": 1, "description": "ChargePowerLimit (slave2)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0231, "length": 1, "description": "DischargePowerLimit (slave2)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0232, "length": 1, "description": "BatFaultMessage (slave2)", "scale": 1.0, "unit": "", "signed": False},
            {"address": 0x0233, "length": 1, "description": "BatCapacity (slave2)", "scale": 1.0, "unit": "%", "signed": False},

            {"address": 0x0234, "length": 1, "description": "Rev(0x0234)"},
            {"address": 0x0235, "length": 1, "description": "Rev(0x0235)"},
            {"address": 0x0236, "length": 1, "description": "Rev(0x0236)"},
            {"address": 0x0237, "length": 1, "description": "Rev(0x0237)"},

            # Slave3 => 0x0238 ~ 0x0251
            {"address": 0x0238, "length": 1, "description": "InvActivePower_R (slave3)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x0239, "length": 1, "description": "InvActivePower_S (slave3)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x023A, "length": 1, "description": "InvActivePower_T (slave3)", "scale": 1.0, "unit": "W", "signed": True},
            {"address": 0x023B, "length": 1, "description": "InvReactiveOrApparentPower_R (slave3)", "scale": 1.0, "unit": "VA", "signed": True},
            {"address": 0x023C, "length": 1, "description": "InvReactiveOrApparentPower_S (slave3)", "scale": 1.0, "unit": "VA", "signed": True},
            {"address": 0x023D, "length": 1, "description": "InvReactiveOrApparentPower_T (slave3)", "scale": 1.0, "unit": "VA", "signed": True},
            {"address": 0x023E, "length": 1, "description": "InvCurrent_R (slave3)", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x023F, "length": 1, "description": "InvCurrent_S (slave3)", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x0240, "length": 1, "description": "InvCurrent_T (slave3)", "scale": 0.1, "unit": "A", "signed": True},
            {"address": 0x0241, "length": 1, "description": "PvPower_ChannelA (slave3)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0242, "length": 1, "description": "PvPower_ChannelB (slave3)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0243, "length": 1, "description": "PvVoltage_ChannelA (slave3)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0244, "length": 1, "description": "PvVoltage_ChannelB (slave3)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0245, "length": 1, "description": "PvCurrent_ChannelA (slave3)", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0246, "length": 1, "description": "PvCurrent_ChannelB (slave3)", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x0247, "length": 1, "description": "BatPower (slave3)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x0248, "length": 1, "description": "BatVoltage (slave3)", "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0249, "length": 1, "description": "BatCurrent (slave3)", "scale": 0.1, "unit": "A", "signed": False},
            {"address": 0x024A, "length": 1, "description": "ChargePowerLimit (slave3)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x024B, "length": 1, "description": "DischargePowerLimit (slave3)", "scale": 1.0, "unit": "W", "signed": False},
            {"address": 0x024C, "length": 1, "description": "BatFaultMessage (slave3)"},
            {"address": 0x024D, "length": 1, "description": "BatCapacity (slave3)", "scale": 1.0, "unit": "%", "signed": False},
            {"address": 0x024E, "length": 1, "description": "Rev(0x024E)"},
            {"address": 0x024F, "length": 1, "description": "Rev(0x024F)"},
            {"address": 0x0250, "length": 1, "description": "Rev(0x0250)"},
            {"address": 0x0251, "length": 1, "description": "Rev(0x0251)"},

            { "address": 0x0252, "length": 1, "description": "InvActivePower_R (slave4)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x0253, "length": 1, "description": "InvActivePower_S (slave4)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x0254, "length": 1, "description": "InvActivePower_T (slave4)", "scale": 1.0, "unit": "W", "signed": True },

            { "address": 0x0255, "length": 1, "description": "InvReactiveOrApparentPower_R (slave4)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x0256, "length": 1, "description": "InvReactiveOrApparentPower_S (slave4)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x0257, "length": 1, "description": "InvReactiveOrApparentPower_T (slave4)", "scale": 1.0, "unit": "VA", "signed": True },

            { "address": 0x0258, "length": 1, "description": "InvCurrent_R (slave4)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x0259, "length": 1, "description": "InvCurrent_S (slave4)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x025A, "length": 1, "description": "InvCurrent_T (slave4)", "scale": 0.1, "unit": "A", "signed": True },

            { "address": 0x025B, "length": 1, "description": "PvPower_ChannelA (slave4)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x025C, "length": 1, "description": "PvPower_ChannelB (slave4)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x025D, "length": 1, "description": "PvVoltage_ChannelA (slave4)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x025E, "length": 1, "description": "PvVoltage_ChannelB (slave4)", "scale": 0.1, "unit": "V", "signed": False },

            { "address": 0x025F, "length": 1, "description": "PvCurrent_ChannelA (slave4)", "scale": 0.1, "unit": "A", "signed": False },
            { "address": 0x0260, "length": 1, "description": "PvCurrent_ChannelB (slave4)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x0261, "length": 1, "description": "BatPower (slave4)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x0262, "length": 1, "description": "BatVoltage (slave4)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x0263, "length": 1, "description": "BatCurrent (slave4)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x0264, "length": 1, "description": "ChargePowerLimit (slave4)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x0265, "length": 1, "description": "DischargePowerLimit (slave4)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x0266, "length": 1, "description": "BatFaultMessage (slave4)" },
            { "address": 0x0267, "length": 1, "description": "BatCapacity (slave4)", "scale": 1.0, "unit": "%", "signed": False },

            { "address": 0x0268, "length": 1, "description": "Rev(0x0268)" },
            { "address": 0x0269, "length": 1, "description": "Rev(0x0269)" },
            { "address": 0x026A, "length": 1, "description": "Rev(0x026A)" },
            { "address": 0x026B, "length": 1, "description": "Rev(0x026B)" },

            { "address": 0x026C, "length": 1, "description": "InvActivePower_R (slave5)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x026D, "length": 1, "description": "InvActivePower_S (slave5)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x026E, "length": 1, "description": "InvActivePower_T (slave5)", "scale": 1.0, "unit": "W", "signed": True },

            { "address": 0x026F, "length": 1, "description": "InvReactiveOrApparentPower_R (slave5)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x0270, "length": 1, "description": "InvReactiveOrApparentPower_S (slave5)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x0271, "length": 1, "description": "InvReactiveOrApparentPower_T (slave5)", "scale": 1.0, "unit": "VA", "signed": True },

            { "address": 0x0272, "length": 1, "description": "InvCurrent_R (slave5)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x0273, "length": 1, "description": "InvCurrent_S (slave5)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x0274, "length": 1, "description": "InvCurrent_T (slave5)", "scale": 0.1, "unit": "A", "signed": True },

            { "address": 0x0275, "length": 1, "description": "PvPower_ChannelA (slave5)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x0276, "length": 1, "description": "PvPower_ChannelB (slave5)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x0277, "length": 1, "description": "PvVoltage_ChannelA (slave5)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x0278, "length": 1, "description": "PvVoltage_ChannelB (slave5)", "scale": 0.1, "unit": "V", "signed": False },

            { "address": 0x0279, "length": 1, "description": "PvCurrent_ChannelA (slave5)", "scale": 0.1, "unit": "A", "signed": False },
            { "address": 0x027A, "length": 1, "description": "PvCurrent_ChannelB (slave5)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x027B, "length": 1, "description": "BatPower (slave5)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x027C, "length": 1, "description": "BatVoltage (slave5)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x027D, "length": 1, "description": "BatCurrent (slave5)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x027E, "length": 1, "description": "ChargePowerLimit (slave5)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x027F, "length": 1, "description": "DischargePowerLimit (slave5)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x0280, "length": 1, "description": "BatFaultMessage (slave5)" },
            { "address": 0x0281, "length": 1, "description": "BatCapacity (slave5)", "scale": 1.0, "unit": "%", "signed": False },

            { "address": 0x0282, "length": 1, "description": "Rev(0x0282)" },
            { "address": 0x0283, "length": 1, "description": "Rev(0x0283)" },
            { "address": 0x0284, "length": 1, "description": "Rev(0x0284)" },

            { "address": 0x0286, "length": 1, "description": "InvActivePower_R (slave6)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x0287, "length": 1, "description": "InvActivePower_S (slave6)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x0288, "length": 1, "description": "InvActivePower_T (slave6)", "scale": 1.0, "unit": "W", "signed": True },

            { "address": 0x0289, "length": 1, "description": "InvReactiveOrApparentPower_R (slave6)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x028A, "length": 1, "description": "InvReactiveOrApparentPower_S (slave6)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x028B, "length": 1, "description": "InvReactiveOrApparentPower_T (slave6)", "scale": 1.0, "unit": "VA", "signed": True },

            { "address": 0x028C, "length": 1, "description": "InvCurrent_R (slave6)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x028D, "length": 1, "description": "InvCurrent_S (slave6)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x028E, "length": 1, "description": "InvCurrent_T (slave6)", "scale": 0.1, "unit": "A", "signed": True },

            { "address": 0x028F, "length": 1, "description": "PvPower_ChannelA (slave6)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x0290, "length": 1, "description": "PvPower_ChannelB (slave6)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x0291, "length": 1, "description": "PvVoltage_ChannelA (slave6)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x0292, "length": 1, "description": "PvVoltage_ChannelB (slave6)", "scale": 0.1, "unit": "V", "signed": False },

            { "address": 0x0293, "length": 1, "description": "PvCurrent_ChannelA (slave6)", "scale": 0.1, "unit": "A", "signed": False },
            { "address": 0x0294, "length": 1, "description": "PvCurrent_ChannelB (slave6)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x0295, "length": 1, "description": "BatPower (slave6)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x0296, "length": 1, "description": "BatVoltage (slave6)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x0297, "length": 1, "description": "BatCurrent (slave6)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x0298, "length": 1, "description": "ChargePowerLimit (slave6)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x0299, "length": 1, "description": "DischargePowerLimit (slave6)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x029A, "length": 1, "description": "BatFaultMessage (slave6)" },
            { "address": 0x029B, "length": 1, "description": "BatCapacity (slave6)", "scale": 1.0, "unit": "%", "signed": False },

            { "address": 0x029C, "length": 1, "description": "Rev(0x029C)" },
            { "address": 0x029D, "length": 1, "description": "Rev(0x029D)" },
            { "address": 0x029E, "length": 1, "description": "Rev(0x029E)" },
            { "address": 0x029F, "length": 1, "description": "Rev(0x029F)" },

            { "address": 0x02A0, "length": 1, "description": "InvActivePower_R (slave7)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x02A1, "length": 1, "description": "InvActivePower_S (slave7)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x02A2, "length": 1, "description": "InvActivePower_T (slave7)", "scale": 1.0, "unit": "W", "signed": True },

            { "address": 0x02A3, "length": 1, "description": "InvReactiveOrApparentPower_R (slave7)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x02A4, "length": 1, "description": "InvReactiveOrApparentPower_S (slave7)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x02A5, "length": 1, "description": "InvReactiveOrApparentPower_T (slave7)", "scale": 1.0, "unit": "VA", "signed": True },

            { "address": 0x02A6, "length": 1, "description": "InvCurrent_R (slave7)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x02A7, "length": 1, "description": "InvCurrent_S (slave7)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x02A8, "length": 1, "description": "InvCurrent_T (slave7)", "scale": 0.1, "unit": "A", "signed": True },

            { "address": 0x02A9, "length": 1, "description": "PvPower_ChannelA (slave7)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x02AA, "length": 1, "description": "PvPower_ChannelB (slave7)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x02AB, "length": 1, "description": "PvVoltage_ChannelA (slave7)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x02AC, "length": 1, "description": "PvVoltage_ChannelB (slave7)", "scale": 0.1, "unit": "V", "signed": False },

            { "address": 0x02AD, "length": 1, "description": "PvCurrent_ChannelA (slave7)", "scale": 0.1, "unit": "A", "signed": False },
            { "address": 0x02AE, "length": 1, "description": "PvCurrent_ChannelB (slave7)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x02AF, "length": 1, "description": "BatPower (slave7)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x02B0, "length": 1, "description": "BatVoltage (slave7)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x02B1, "length": 1, "description": "BatCurrent (slave7)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x02B2, "length": 1, "description": "ChargePowerLimit (slave7)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x02B3, "length": 1, "description": "DischargePowerLimit (slave7)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x02B4, "length": 1, "description": "BatFaultMessage (slave7)" },
            { "address": 0x02B5, "length": 1, "description": "BatCapacity (slave7)", "scale": 1.0, "unit": "%", "signed": False },

            { "address": 0x02B6, "length": 1, "description": "Rev(0x02B6)" },
            { "address": 0x02B7, "length": 1, "description": "Rev(0x02B7)" },
            { "address": 0x02B8, "length": 1, "description": "Rev(0x02B8)" },
            { "address": 0x02B9, "length": 1, "description": "Rev(0x02B9)" },

            { "address": 0x02BA, "length": 1, "description": "InvActivePower_R (slave8)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x02BB, "length": 1, "description": "InvActivePower_S (slave8)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x02BC, "length": 1, "description": "InvActivePower_T (slave8)", "scale": 1.0, "unit": "W", "signed": True },

            { "address": 0x02BD, "length": 1, "description": "InvReactiveOrApparentPower_R (slave8)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x02BE, "length": 1, "description": "InvReactiveOrApparentPower_S (slave8)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x02BF, "length": 1, "description": "InvReactiveOrApparentPower_T (slave8)", "scale": 1.0, "unit": "VA", "signed": True },

            { "address": 0x02C0, "length": 1, "description": "InvCurrent_R (slave8)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x02C1, "length": 1, "description": "InvCurrent_S (slave8)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x02C2, "length": 1, "description": "InvCurrent_T (slave8)", "scale": 0.1, "unit": "A", "signed": True },

            { "address": 0x02C3, "length": 1, "description": "PvPower_ChannelA (slave8)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x02C4, "length": 1, "description": "PvPower_ChannelB (slave8)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x02C5, "length": 1, "description": "PvVoltage_ChannelA (slave8)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x02C6, "length": 1, "description": "PvVoltage_ChannelB (slave8)", "scale": 0.1, "unit": "V", "signed": False },

            { "address": 0x02C7, "length": 1, "description": "PvCurrent_ChannelA (slave8)", "scale": 0.1, "unit": "A", "signed": False },
            { "address": 0x02C8, "length": 1, "description": "PvCurrent_ChannelB (slave8)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x02C9, "length": 1, "description": "BatPower (slave8)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x02CA, "length": 1, "description": "BatVoltage (slave8)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x02CB, "length": 1, "description": "BatCurrent (slave8)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x02CC, "length": 1, "description": "ChargePowerLimit (slave8)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x02CD, "length": 1, "description": "DischargePowerLimit (slave8)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x02CE, "length": 1, "description": "BatFaultMessage (slave8)" },
            { "address": 0x02CF, "length": 1, "description": "BatCapacity (slave8)", "scale": 1.0, "unit": "%", "signed": False },

            { "address": 0x02D0, "length": 1, "description": "Rev(0x02D0)" },
            { "address": 0x02D1, "length": 1, "description": "Rev(0x02D1)" },
            { "address": 0x02D2, "length": 1, "description": "Rev(0x02D2)" },
            { "address": 0x02D3, "length": 1, "description": "Rev(0x02D3)" },

            { "address": 0x02D4, "length": 1, "description": "InvActivePower_R (slave9)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x02D5, "length": 1, "description": "InvActivePower_S (slave9)", "scale": 1.0, "unit": "W", "signed": True },
            { "address": 0x02D6, "length": 1, "description": "InvActivePower_T (slave9)", "scale": 1.0, "unit": "W", "signed": True },

            { "address": 0x02D7, "length": 1, "description": "InvReactiveOrApparentPower_R (slave9)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x02D8, "length": 1, "description": "InvReactiveOrApparentPower_S (slave9)", "scale": 1.0, "unit": "VA", "signed": True },
            { "address": 0x02D9, "length": 1, "description": "InvReactiveOrApparentPower_T (slave9)", "scale": 1.0, "unit": "VA", "signed": True },

            { "address": 0x02DA, "length": 1, "description": "InvCurrent_R (slave9)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x02DB, "length": 1, "description": "InvCurrent_S (slave9)", "scale": 0.1, "unit": "A", "signed": True },
            { "address": 0x02DC, "length": 1, "description": "InvCurrent_T (slave9)", "scale": 0.1, "unit": "A", "signed": True },

            { "address": 0x02DD, "length": 1, "description": "PvPower_ChannelA (slave9)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x02DE, "length": 1, "description": "PvPower_ChannelB (slave9)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x02DF, "length": 1, "description": "PvVoltage_ChannelA (slave9)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x02E0, "length": 1, "description": "PvVoltage_ChannelB (slave9)", "scale": 0.1, "unit": "V", "signed": False },

            { "address": 0x02E1, "length": 1, "description": "PvCurrent_ChannelA (slave9)", "scale": 0.1, "unit": "A", "signed": False },
            { "address": 0x02E2, "length": 1, "description": "PvCurrent_ChannelB (slave9)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x02E3, "length": 1, "description": "BatPower (slave9)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x02E4, "length": 1, "description": "BatVoltage (slave9)", "scale": 0.1, "unit": "V", "signed": False },
            { "address": 0x02E5, "length": 1, "description": "BatCurrent (slave9)", "scale": 0.1, "unit": "A", "signed": False },

            { "address": 0x02E6, "length": 1, "description": "ChargePowerLimit (slave9)", "scale": 1.0, "unit": "W", "signed": False },
            { "address": 0x02E7, "length": 1, "description": "DischargePowerLimit (slave9)", "scale": 1.0, "unit": "W", "signed": False },

            { "address": 0x02E8, "length": 1, "description": "BatFaultMessage (slave9)" },
            { "address": 0x02E9, "length": 1, "description": "BatCapacity (slave9)", "scale": 1.0, "unit": "%", "signed": False },

            { "address": 0x02EA, "length": 1, "description": "Rev(0x02EA)" },
            { "address": 0x02EB, "length": 1, "description": "Rev(0x02EB)" },
            { "address": 0x02EC, "length": 1, "description": "Rev(0x02EC)" },
            { "address": 0x02ED, "length": 1, "description": "Rev(0x02ED)" },
        ]

    def get_registers(self):
        return self._registers

    def renderRegister(self, reg, raw_list):
        """
        Similar to your existing input classes: 
          - If length>1 => treat as ASCII by default 
          - If length=1 => numeric with scale/unit
        """
        length = reg["length"]
        if length > 1:
            # By default, interpret as ASCII
            chars = []
            for val in raw_list:
                high_byte = (val >> 8) & 0xFF
                low_byte = val & 0xFF
                chars.append(chr(high_byte))
                chars.append(chr(low_byte))
            return "".join(chars).strip()

        # single
        raw_val = raw_list[0]
        scale = reg.get("scale", 1.0)
        unit = reg.get("unit", "")
        signed = reg.get("signed", False)

        if signed and (raw_val & 0x8000):
            raw_val -= 0x10000

        val = raw_val * scale
        return self._format_display_str(val, scale, unit)

    def _format_display_str(self, value, scale, unit):
        """
        If scale == 1.0 => integer 
        elif scale==0.1 => 1 decimal, etc...
        For consistency with your code:
        """
        if scale == 1.0:
            val_str = f"{int(value)}"
        elif abs(scale - 0.1) < 1e-9:
            val_str = f"{value:.1f}"
        elif abs(scale - 0.01) < 1e-9:
            val_str = f"{value:.2f}"
        else:
            val_str = f"{value:.3f}"

        if unit:
            return f"{val_str} {unit}"
        return val_str
