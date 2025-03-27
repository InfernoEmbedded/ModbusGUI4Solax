class SelfTestInputRegisterDefinitions:
    """
    Self-Test input registers (Function code 0x04) from the PDF section 5:
      0x0180 ~ 0x01DA

    Each entry includes:
      - address
      - length (1 for single 16-bit)
      - description (from the PDF)
      - scale + unit as appropriate
      - signed if needed (False by default)
    """

    def __init__(self):
        self._registers = [
            # 0x0180 => wSelfTest_step
            {"address": 0x0180, "length": 1, "description": "wSelfTest_step (Test Step)", 
             "scale": 1.0, "unit": "", "signed": False},
            # 0x0181 => wSelfTest_Time
            {"address": 0x0181, "length": 1, "description": "wSelfTest_Time (Remaining time of test)", 
             "scale": 1.0, "unit": "s", "signed": False},
            # 0x0182 => wSelfTest_State
            {"address": 0x0182, "length": 1, "description": "wSelfTest_State (bit flags for Ovp/Uvp/etc.)",
             "scale": 1.0, "unit": "", "signed": False},

            # 0x0183 => Ovp_Threshold_Target
            {"address": 0x0183, "length": 1, "description": "Ovp(59.S2) test threshold", 
             "scale": 0.1, "unit": "V", "signed": False},
            # 0x0184 => Ovp_Threshold_Time
            {"address": 0x0184, "length": 1, "description": "Ovp(59.S2) test time", 
             "scale": 1.0, "unit": "ms", "signed": False},
            # 0x0185 => Ovp_Outcome_Sample_R
            {"address": 0x0185, "length": 1, "description": "Ovp outcome sample(R)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0186, "length": 1, "description": "Ovp_Outcome_TripValue_R", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0187, "length": 1, "description": "Ovp_Outcome_Time_R", 
             "scale": 1.0, "unit": "ms", "signed": False},

            # 0x0188~0x018D => Ovp outcome S/T
            {"address": 0x0188, "length": 1, "description": "Ovp_Outcome_Sample_S(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0189, "length": 1, "description": "Ovp_Outcome_TripValue_S(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x018A, "length": 1, "description": "Ovp_Outcome_Time_S(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x018B, "length": 1, "description": "Ovp_Outcome_Sample_T(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x018C, "length": 1, "description": "Ovp_Outcome_TripValue_T(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x018D, "length": 1, "description": "Ovp_Outcome_Time_T(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},

            # 0x018E~0x0198 => Uvp(27.S1) outcome
            {"address": 0x018E, "length": 1, "description": "Uvp(27.S1) Threshold Target", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x018F, "length": 1, "description": "Uvp(27.S1) Threshold Time", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x0190, "length": 1, "description": "Uvp_Outcome_Sample_R", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0191, "length": 1, "description": "Uvp_Outcome_TripValue_R", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0192, "length": 1, "description": "Uvp_Outcome_Time_R", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x0193, "length": 1, "description": "Uvp_Outcome_Sample_S(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0194, "length": 1, "description": "Uvp_Outcome_TripValue_S(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0195, "length": 1, "description": "Uvp_Outcome_Time_S(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x0196, "length": 1, "description": "Uvp_Outcome_Sample_T(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0197, "length": 1, "description": "Uvp_Outcome_TripValue_T(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x0198, "length": 1, "description": "Uvp_Outcome_Time_T(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},

            # 0x0199~0x01A3 => Uvp(27.S2)
            {"address": 0x0199, "length": 1, "description": "Uvp(27.S2) Threshold Target", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x019A, "length": 1, "description": "Uvp(27.S2) Threshold Time", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x019B, "length": 1, "description": "UvpRestric_Outcome_Sample_R", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x019C, "length": 1, "description": "UvpRestric_Outcome_TripValue_R", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x019D, "length": 1, "description": "UvpRestric_Outcome_Time_R", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x019E, "length": 1, "description": "UvpRestric_Outcome_Sample_S(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x019F, "length": 1, "description": "UvpRestric_Outcome_TripValue_S(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01A0, "length": 1, "description": "UvpRestric_Outcome_Time_S(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01A1, "length": 1, "description": "UvpRestric_Outcome_Sample_T(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01A2, "length": 1, "description": "UvpRestric_Outcome_TripValue_T(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01A3, "length": 1, "description": "UvpRestric_Outcome_Time_T(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},

            # 0x01A4~0x01AE => Ofp(81>.S1)
            {"address": 0x01A4, "length": 1, "description": "Ofp(81>.S1) Threshold Target", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01A5, "length": 1, "description": "Ofp(81>.S1) Threshold Time", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01A6, "length": 1, "description": "Ofp_Outcome_Sample_R", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01A7, "length": 1, "description": "Ofp_Outcome_TripValue_R", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01A8, "length": 1, "description": "Ofp_Outcome_Time_R", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01A9, "length": 1, "description": "Ofp_Outcome_Sample_S(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01AA, "length": 1, "description": "Ofp_Outcome_TripValue_S(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01AB, "length": 1, "description": "Ofp_Outcome_Time_S(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01AC, "length": 1, "description": "Ofp_Outcome_Sample_T(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01AD, "length": 1, "description": "Ofp_Outcome_TripValue_T(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01AE, "length": 1, "description": "Ofp_Outcome_Time_T(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},

            # 0x01AF~0x01B9 => Ufp(81<.S1)
            {"address": 0x01AF, "length": 1, "description": "Ufp(81<.S1) Threshold Target", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01B0, "length": 1, "description": "Ufp(81<.S1) Threshold Time", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01B1, "length": 1, "description": "Ufp_Outcome_Sample_R", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01B2, "length": 1, "description": "Ufp_Outcome_TripValue_R", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01B3, "length": 1, "description": "Ufp_Outcome_Time_R", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01B4, "length": 1, "description": "Ufp_Outcome_Sample_S(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01B5, "length": 1, "description": "Ufp_Outcome_TripValue_S(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01B6, "length": 1, "description": "Ufp_Outcome_Time_S(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01B7, "length": 1, "description": "Ufp_Outcome_Sample_T(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01B8, "length": 1, "description": "Ufp_Outcome_TripValue_T(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01B9, "length": 1, "description": "Ufp_Outcome_Time_T(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},

            # 0x01BA~0x01C4 => Ofp2(81>.S2)
            {"address": 0x01BA, "length": 1, "description": "Ofp2(81>.S2) Threshold Target", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01BB, "length": 1, "description": "Ofp2(81>.S2) Threshold Time", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01BC, "length": 1, "description": "OfpRestric_Outcome_Sample_R", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01BD, "length": 1, "description": "OfpRestric_Outcome_TripValue_R", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01BE, "length": 1, "description": "OfpRestric_Outcome_Time_R", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01BF, "length": 1, "description": "OfpRestric_Outcome_Sample_S(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01C0, "length": 1, "description": "OfpRestric_Outcome_TripValue_S(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01C1, "length": 1, "description": "OfpRestric_Outcome_Time_S(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01C2, "length": 1, "description": "OfpRestric_Outcome_Sample_T(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01C3, "length": 1, "description": "OfpRestric_Outcome_TripValue_T(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01C4, "length": 1, "description": "OfpRestric_Outcome_Time_T(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},

            # 0x01C5~0x01CF => Ufp2(81<.S2)
            {"address": 0x01C5, "length": 1, "description": "Ufp2(81<.S2) Threshold Target", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01C6, "length": 1, "description": "Ufp2(81<.S2) Threshold Time", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01C7, "length": 1, "description": "UfpRestric_Outcome_Sample_R", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01C8, "length": 1, "description": "UfpRestric_Outcome_TripValue_R", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01C9, "length": 1, "description": "UfpRestric_Outcome_Time_R", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01CA, "length": 1, "description": "UfpRestric_Outcome_Sample_S(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01CB, "length": 1, "description": "UfpRestric_Outcome_TripValue_S(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01CC, "length": 1, "description": "UfpRestric_Outcome_Time_S(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},
            {"address": 0x01CD, "length": 1, "description": "UfpRestric_Outcome_Sample_T(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01CE, "length": 1, "description": "UfpRestric_Outcome_TripValue_T(X3)", 
             "scale": 0.01, "unit": "Hz", "signed": False},
            {"address": 0x01CF, "length": 1, "description": "UfpRestric_Outcome_Time_T(X3)", 
             "scale": 1.0, "unit": "ms", "signed": False},

            # 0x01D0~0x01DA => Ovp10(59.S1) ...
            {"address": 0x01D0, "length": 1, "description": "Ovp10(59.S1) Threshold Target", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01D1, "length": 1, "description": "Ovp10(59.S1) Threshold Time", 
             "scale": 1.0, "unit": "s", "signed": False},
            {"address": 0x01D2, "length": 1, "description": "Ovp10(59.S1) Outcome_Sample_R", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01D3, "length": 1, "description": "Ovp10(59.S1) Outcome_TripValue_R", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01D4, "length": 1, "description": "Ovp10(59.S1) Outcome_Time_R", 
             "scale": 1.0, "unit": "s", "signed": False},
            {"address": 0x01D5, "length": 1, "description": "Ovp10(59.S1) Outcome_Sample_S(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01D6, "length": 1, "description": "Ovp10(59.S1) Outcome_TripValue_S(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01D7, "length": 1, "description": "Ovp10(59.S1) Outcome_Time_S(X3)", 
             "scale": 1.0, "unit": "s", "signed": False},
            {"address": 0x01D8, "length": 1, "description": "Ovp10(59.S1) Outcome_Sample_T(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01D9, "length": 1, "description": "Ovp10(59.S1) Outcome_TripValue_T(X3)", 
             "scale": 0.1, "unit": "V", "signed": False},
            {"address": 0x01DA, "length": 1, "description": "Ovp10(59.S1) Outcome_Time_T(X3)", 
             "scale": 1.0, "unit": "s", "signed": False},
        ]

    def get_registers(self):
        """Returns the entire list of self-test input registers."""
        return self._registers

    def renderRegister(self, reg, raw_list):
        """
        For these self-test addresses:
          - single 16-bit => numeric with scale
          - length=1 => interpret as numeric
          - if length>1 (none in the doc), we'd do ASCII
        """
        length = reg["length"]
        if length > 1:
            # By default, treat multi-register as ASCII if we had any
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

        # sign logic if needed
        if signed and (raw_val & 0x8000):
            raw_val -= 0x10000

        val_f = raw_val * scale
        return self._format_display_str(val_f, scale, unit)

    def _format_display_str(self, value, scale, unit):
        """
        If scale == 1.0 => integer,
        elif scale == 0.1 => 1 decimal,
        elif scale == 0.01 => 2 decimals,
        else => 3 decimals
        """
        if scale == 1.0:
            val_str = f"{int(value)}"
        elif scale == 0.1:
            val_str = f"{value:.1f}"
        elif scale == 0.01:
            val_str = f"{value:.2f}"
        else:
            val_str = f"{value:.3f}"

        return f"{val_str} {unit}" if unit else val_str
