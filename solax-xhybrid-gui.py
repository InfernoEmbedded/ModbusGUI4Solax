#!/usr/bin/env python3
import argparse
import tkinter as tk
from tkinter import ttk, messagebox
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Map of safety-type codes to strings
# For codes with two meanings (X1 vs. X3), we show both.
SAFETY_TYPE_MAP = {
    0:  "VDE0126",
    1:  "ARN4105",
    2:  "AS4777_AU",
    3:  "G98/1",
    4:  "C10/11",
    5:  "OVE/ONORME8001",
    6:  "EN50438_NL",
    7:  "EN50438_DK",
    8:  "CEB",
    9:  "CEI021",
    10: "NRS097_2_1",
    11: "VDE0126_Gr_Is",
    12: "UTE_C15_712",
    13: "IEC61727",
    14: "G99/1",
    15: "VDE0126_Gr_Co",
    16: "France_VFR2014",
    17: "C15_712_is_50",
    18: "C15_712_is_60",
    19: "AS4777_NZ",
    20: "RD1699",
    21: "Chile",
    # Overlapping codes for X3 and X1 start here:
    22: "Israel (X3) / EN50438_Ireland (X1)",
    23: "Czech_CEZ (X3) / Philippines (X1)",
    24: "UNE_206 (X3) / Czech_PPDS (X1)",
    25: "EN50438_Poland (X3) / Czech_50438 (X1)",
    # X3-only codes for 26-32
    26: "EN50438_Portugal (X3)",
    27: "PEA (X3)",
    28: "MEA (X3)",
    29: "EN50438_Sweden (X3)",
    30: "Philippines (X3)",
    31: "EN50438_Slovenia (X3)",
    32: "CEI0_16 (X3)"
}

class ModbusGUI:
    def __init__(self, master, default_ip="192.168.0.100"):
        self.master = master
        self.master.title("Inverter Modbus TCP Reader")

        # Connection frame
        connection_frame = ttk.LabelFrame(master, text="Connection Settings")
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(connection_frame, text="IP Address:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ip_entry = ttk.Entry(connection_frame, width=20)
        self.ip_entry.insert(0, default_ip)  # Use default IP or overridden via CLI
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.insert(0, "502")  # Default Modbus TCP port
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(connection_frame, text="Connect & Read", command=self.connect_and_read).grid(row=0, column=4, padx=5, pady=5)

        # Table for data display
        self.tree = ttk.Treeview(master, columns=("address", "description", "value"), show='headings')
        self.tree.heading("address", text="Register Address")
        self.tree.heading("description", text="Description")
        self.tree.heading("value", text="Value")

        # Column-level alignment
        self.tree.column("address", width=120, anchor="e")  # Right-align numeric addresses
        self.tree.column("description", width=300, anchor="w")  # Left-align text
        self.tree.column("value", width=160, anchor="w")  # We'll refine single vs multi with tags

        # Tag-based alignment
        self.tree.tag_configure('numeric_value', anchor='e')
        self.tree.tag_configure('text_value', anchor='w')

        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Complete holding register map from doc (0x0000 ~ 0x0115)
        # Group multi-register strings in a single entry
        self.registers = [

            # 0x0000 ~ 0x0006 => 7 registers => SeriesNumber (14 chars)
            {"address": 0x0000, "length": 7, "description": "SeriesNumber (14 chars)"},
            # 0x0007 ~ 0x000D => 7 => FactoryName
            {"address": 0x0007, "length": 7, "description": "FactoryName (14 chars)"},
            # 0x000E ~ 0x0014 => 7 => ModuleName
            {"address": 0x000E, "length": 7, "description": "ModuleName (14 chars)"},

            {"address": 0x0015, "length": 1, "description": "VpvStart(Hybrid) [0.1V]"},
            {"address": 0x0016, "length": 1, "description": "TimeStart [1s]"},
            {"address": 0x0017, "length": 1, "description": "VpvHighStop(Hybrid) [0.1V]"},
            {"address": 0x0018, "length": 1, "description": "VpvLowStop(Hybrid) [0.1V]"},
            {"address": 0x0019, "length": 1, "description": "VacMinProtect [0.1V]"},
            {"address": 0x001A, "length": 1, "description": "VacMaxProtect [0.1V]"},
            {"address": 0x001B, "length": 1, "description": "FacMinProtect [0.01Hz]"},
            {"address": 0x001C, "length": 1, "description": "FacMaxProtect [0.01Hz]"},

            # 0x001D => Safety type (special handling for numeric+string)
            {"address": 0x001D, "length": 1, "description": "Safety (Numeric + String)"},

            {"address": 0x001E, "length": 1, "description": "REV"},
            {"address": 0x001F, "length": 1, "description": "Grid10MinAvgProtect [0.1V]"},
            {"address": 0x0020, "length": 1, "description": "VacMinSlowProtect [0.1V]"},
            {"address": 0x0021, "length": 1, "description": "VacMaxSlowProtect [0.1V]"},
            {"address": 0x0022, "length": 1, "description": "FacMinSlowProtect [0.01Hz]"},
            {"address": 0x0023, "length": 1, "description": "FacMaxSlowProtect [0.01Hz]"},
            {"address": 0x0024, "length": 1, "description": "DciLimits [1mA]"},
            {"address": 0x0025, "length": 1, "description": "PowerLimitsPercent [0~100]"},
            {"address": 0x0026, "length": 1, "description": "PowerfactorMode"},
            {"address": 0x0027, "length": 1, "description": "PowerfactorData [0.01]"},
            {"address": 0x0028, "length": 1, "description": "UpperLimit [0.01] (Overexcite limit)"},
            {"address": 0x0029, "length": 1, "description": "LowerLimit [0.01] (Underexcite limit)"},
            {"address": 0x002A, "length": 1, "description": "PowerLow [0.01]"},
            {"address": 0x002B, "length": 1, "description": "PowerUp [0.01]"},

            # 0x002C ~ 0x007B => 80 => PowerManagerConfigData(Rev)
            {"address": 0x002C, "length": 80, "description": "PowerManagerConfigData(Rev) [80 regs]"},

            {"address": 0x007C, "length": 1, "description": "PowerManagerEnable(Rev)"},
            {"address": 0x007D, "length": 1, "description": "FirmwareVersion_InverterMaster"},

            # 0x007E ~ 0x0081 => 4 => REV
            {"address": 0x007E, "length": 4, "description": "REV"},

            {"address": 0x0082, "length": 1, "description": "FirmwareVersion_ModbusTCP_minor"},
            {"address": 0x0083, "length": 1, "description": "FirmwareVersion_Manager"},
            {"address": 0x0084, "length": 1, "description": "FirmwareVersion_Manager_Bootloader"},
            {"address": 0x0085, "length": 1, "description": "RTC-Seconds"},
            {"address": 0x0086, "length": 1, "description": "RTC-Minutes"},
            {"address": 0x0087, "length": 1, "description": "RTC-Hours"},
            {"address": 0x0088, "length": 1, "description": "RTC-Days"},
            {"address": 0x0089, "length": 1, "description": "RTC-Months"},
            {"address": 0x008A, "length": 1, "description": "RTC-Years"},
            {"address": 0x008B, "length": 1, "description": "SolarChargerUseMode (0=SelfUse,1=ForceTime,2=BackUp,3=FeedinPri)"},
            {"address": 0x008C, "length": 1, "description": "Battery_MinCapacity [1%]"},
            {"address": 0x008D, "length": 1, "description": "wBattery1_Type (0=LeadAcid,1=Li)"},
            {"address": 0x008E, "length": 1, "description": "Charge_floatVolt [0.1V]"},
            {"address": 0x008F, "length": 1, "description": "Battery_DischargeCutVoltage [0.1V]"},
            {"address": 0x0090, "length": 1, "description": "Battery_ChargeMaxCurrent [0.1A]"},
            {"address": 0x0091, "length": 1, "description": "Battery_DischargeMaxCurrent [0.1A]"},
            {"address": 0x0092, "length": 1, "description": "ChargerStartTime1_Hours [0~23]"},
            {"address": 0x0093, "length": 1, "description": "ChargerStartTime1_Min [0~59]"},
            {"address": 0x0094, "length": 1, "description": "ChargerEndTime1_Hours [0~23]"},
            {"address": 0x0095, "length": 1, "description": "ChargerEndTime1_Min [0~59]"},

            # 0x0096 ~ 0x0099 => 4 => REV
            {"address": 0x0096, "length": 4, "description": "REV"},

            {"address": 0x009A, "length": 1, "description": "ChargerStartTime2_Hours [0~23]"},
            {"address": 0x009B, "length": 1, "description": "ChargerStartTime2_Min [0~59]"},
            {"address": 0x009C, "length": 1, "description": "ChargerEndTime2_Hours [0~23]"},
            {"address": 0x009D, "length": 1, "description": "ChargerEndTime2_Min [0~59]"},

            # 0x009E ~ 0x00A1 => 4 => REV
            {"address": 0x009E, "length": 4, "description": "REV"},

            {"address": 0x00A2, "length": 1, "description": "MAC address part1 (MAC[0..1])"},
            {"address": 0x00A3, "length": 1, "description": "MAC address part2 (MAC[2..3])"},
            {"address": 0x00A4, "length": 1, "description": "MAC address part3 (MAC[4..5])"},
            {"address": 0x00A5, "length": 1, "description": "REV"},

            {"address": 0x00A6, "length": 1, "description": "ModbusPowerControl (0=off,1=on)"},
            {"address": 0x00A7, "length": 1, "description": "absorpt_voltage [0.1V]"},

            # 0x00A8 ~ 0x00AE => Possibly REV, but doc lumps partial, we keep as 7 for safety
            {"address": 0x00A8, "length": 7, "description": "REV (7 regs, partially overlaps RegistrationCode)"},
            
            # 0x00AF ~ 0x00B3 => 5 regs => Registration code(for lan) [10 chars]
            {"address": 0x00AF, "length": 5, "description": "RegistrationCode(for lan) (10 chars)"},

            {"address": 0x00B4, "length": 1, "description": "Allow_Grid_Charge (0-3)"},
            {"address": 0x00B5, "length": 1, "description": "Export control_factory limit [1W]"},
            {"address": 0x00B6, "length": 1, "description": "Export control user limit [1W]"},
            {"address": 0x00B7, "length": 1, "description": "EPS_Mute (0=off,1=on)"},
            {"address": 0x00B8, "length": 1, "description": "EPS Frequency (0=50Hz,1=60Hz)"},
            {"address": 0x00B9, "length": 1, "description": "REV"},
            {"address": 0x00BA, "length": 1, "description": "Inverter Type [1W rating]"},
            {"address": 0x00BB, "length": 1, "description": "Language(for screen) (0=English,1=German)"},
            {"address": 0x00BC, "length": 1, "description": "IP Method (0=DHCP,1=Static)"},
            {"address": 0x00BD, "length": 1, "description": "wTimeVacMin_FastAdj [1ms] (Italy)"},
            {"address": 0x00BE, "length": 1, "description": "wTimeVacMax_FastAdj [1ms] (Italy)"},
            {"address": 0x00BF, "length": 1, "description": "wTimeFacMin_FastAdj [1ms] (Italy)"},
            {"address": 0x00C0, "length": 1, "description": "wTimeFacMax_FastAdj [1ms] (Italy)"},
            {"address": 0x00C1, "length": 1, "description": "wTimeVacMin_SlowAdj [1ms] (Italy)"},
            {"address": 0x00C2, "length": 1, "description": "wTimeVacMax_SlowAdj [1ms] (Italy)"},
            {"address": 0x00C3, "length": 1, "description": "wTimeFacMin_SlowAdj [1ms] (Italy)"},
            {"address": 0x00C4, "length": 1, "description": "wTimeFacMax_SlowAdj [1ms] (Italy)"},
            {"address": 0x00C5, "length": 1, "description": "TestStep SelfTest"},
            {"address": 0x00C6, "length": 1, "description": "OvpValue(59.S2) [0.1V]"},
            {"address": 0x00C7, "length": 1, "description": "OvpTime(59.S2) [1ms]"},
            {"address": 0x00C8, "length": 1, "description": "UvpValue(27.S1) [0.1V]"},
            {"address": 0x00C9, "length": 1, "description": "UvpTime(27.S1) [1ms]"},
            {"address": 0x00CA, "length": 1, "description": "OfpValue(81>.S1) [0.01Hz]"},
            {"address": 0x00CB, "length": 1, "description": "OfpTime(81>.S1) [1ms]"},
            {"address": 0x00CC, "length": 1, "description": "UfpValue(81<.S1) [0.01Hz]"},
            {"address": 0x00CD, "length": 1, "description": "UfpTime(81<.S1) [1ms]"},
            {"address": 0x00CE, "length": 1, "description": "SelfTestOvp10mAvgVal(59.S1) [0.1V]"},
            {"address": 0x00CF, "length": 1, "description": "SelfTestOvp10mAvgTime(59.S1) [1s]"},
            {"address": 0x00D0, "length": 1, "description": "SelfTestOfpVal_Restrictive(81>.S2) [0.01Hz]"},
            {"address": 0x00D1, "length": 1, "description": "SelfTestOfpTime_Restrictive(81>.S2) [1ms]"},
            {"address": 0x00D2, "length": 1, "description": "SelfTestUfpVal_Restrictive(81<.S2) [0.01Hz]"},
            {"address": 0x00D3, "length": 1, "description": "SelfTestUfpTime_Restrictive(81<.S2) [1ms]"},
            {"address": 0x00D4, "length": 1, "description": "SelfTest_UvpRestrictive_Val(27.S2) [0.1V]"},
            {"address": 0x00D5, "length": 1, "description": "SelfTest_UvpRestrictive_Time(27.S2) [1ms]"},
            {"address": 0x00D6, "length": 1, "description": "SelfTest_Time [1s]"},
            {"address": 0x00D7, "length": 1, "description": "REV"},
            {"address": 0x00D8, "length": 1, "description": "PfLockInPoint [105~110]"},
            {"address": 0x00D9, "length": 1, "description": "PfLockOutPoint [98~90]"},
            {"address": 0x00DA, "length": 1, "description": "wInverter_OutPut_Switch (1=ON,0=Off)"},
            {"address": 0x00DB, "length": 1, "description": "FreqSetPoint [0.01Hz] OverFreq drop"},
            {"address": 0x00DC, "length": 1, "description": "FreqDroopRate [1%]"},
            {"address": 0x00DD, "length": 1, "description": "FreDroopDelayTime [1ms]"},
            {"address": 0x00DE, "length": 1, "description": "QuVrateUp [1%]"},
            {"address": 0x00DF, "length": 1, "description": "QuVrateLow [1%]"},

            {"address": 0x00E0, "length": 19, "description": "REV (covers 0x00E0 ~ 0x00F2)"},

            {"address": 0x00F3, "length": 1, "description": "wPowerLimitGra [0.0001]"},
            {"address": 0x00F4, "length": 1, "description": "VoltResponse_V2 [0.1V]"},
            {"address": 0x00F5, "length": 1, "description": "VoltResponse_V3 [0.1V]"},
            {"address": 0x00F6, "length": 1, "description": "VoltResponse_V4 [0.1V]"},
            {"address": 0x00F7, "length": 1, "description": "VoltResponse_Ratio1 [0.01]"},
            {"address": 0x00F8, "length": 1, "description": "VoltResponse_Ratio4 [0.01]"},
            {"address": 0x00F9, "length": 1, "description": "PUFuncEnable (0=off,1=on)"},
            {"address": 0x00FA, "length": 1, "description": "Qpower_set [1Var]"},
            {"address": 0x00FB, "length": 1, "description": "bQpower_set_Max [1Var]"},
            {"address": 0x00FC, "length": 1, "description": "bQpower_set_Min [1Var]"},

            {"address": 0x00FD, "length": 1, "description": "BackUp_GridChargeEN (0=off,1=on)"},
            {"address": 0x00FE, "length": 1, "description": "BackUp_chr_Strat_H [Hour]"},
            {"address": 0x00FF, "length": 1, "description": "BackUp_chr_Strat_M [Min]"},
            {"address": 0x0100, "length": 1, "description": "BackUp_chr_End_H [Hour]"},
            {"address": 0x0101, "length": 1, "description": "BackUp_chr_End_M [Min]"},

            {"address": 0x0102, "length": 1, "description": "wAS4777PowerManagerEnable (0=off,1=on)"},
            {"address": 0x0103, "length": 1, "description": "CloudControlEN (0=off,1=on)"},
            {"address": 0x0104, "length": 1, "description": "wGlobalMPPTFuncEnable(X1) (0=off,1=on)"},
            {"address": 0x0105, "length": 1, "description": "Grid service(X3) (0=off,1=on)"},
            {"address": 0x0106, "length": 1, "description": "PhasePowerBalance(X3) (0=off,1=on)"},
            {"address": 0x0107, "length": 1, "description": "wMachineStyle (0=X-Hybrid,1=X-Retrofit)"},
            {"address": 0x0108, "length": 1, "description": "MeterFunction (0=off,1=on)"},
            {"address": 0x0109, "length": 1, "description": "Meter1ID [1~200]"},
            {"address": 0x010A, "length": 1, "description": "Meter2ID [1~200]"},
            {"address": 0x010B, "length": 1, "description": "PowerControl_timeout [5~65535s or 65535=disable check]"},
            {"address": 0x010C, "length": 1, "description": "EPS_AutoRestart (0=off,1=on)"},
            {"address": 0x010D, "length": 1, "description": "EPS_MinEscVolt [1V]"},
            {"address": 0x010E, "length": 1, "description": "EPS_MinEscSoc [1%]"},

            {"address": 0x010F, "length": 1, "description": "ForceTimeUse_P1_MaxCapacity [1%]"},
            {"address": 0x0110, "length": 1, "description": "ForceTimeUse_P2_MaxCapacity [1%]"},
            {"address": 0x0111, "length": 1, "description": "DischCutOffPoint_DifferentEN (0=off,1=on)"},
            {"address": 0x0112, "length": 1, "description": "DischCutOffCapacity_GridMode [1%]"},
            {"address": 0x0113, "length": 1, "description": "DischCutOffVoltage_GridMode [0.1V]"},
            {"address": 0x0114, "length": 1, "description": "wEarthDetectEn(X3) (0=off,1=on)"},
            {"address": 0x0115, "length": 1, "description": "CTMeterSetting(X1) (0=Meter,1=CT)"},

        ]

        # Make the window resize-friendly
        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

    def connect_and_read(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())

        client = ModbusTcpClient(host=ip, port=port)
        if not client.connect():
            messagebox.showerror("Connection Error", f"Failed to connect to inverter at {ip}:{port}")
            return

        self.tree.delete(*self.tree.get_children())  # Clear existing rows

        try:
            for reg in self.registers:
                response = client.read_holding_registers(address=reg["address"], count=reg["length"])
                if response.isError():
                    # On read error, show a text result
                    value_str = "Error reading"
                    tag = 'text_value'
                else:
                    if reg["length"] > 1:
                        # Multi-register read → interpret as text (e.g., strings or reserved blocks)
                        # This is how many models store ASCII
                        raw_list = response.registers
                        chars = []
                        for val in raw_list:
                            high_byte = (val >> 8) & 0xFF
                            low_byte = val & 0xFF
                            chars.append(chr(high_byte))
                            chars.append(chr(low_byte))
                        value_str = "".join(chars).strip()
                        tag = 'text_value'
                    else:
                        # Single register → numeric
                        raw_val = response.registers[0]
                        # If it's the safety register (0x001D), display both code & string
                        if reg["address"] == 0x001D:
                            mapped = SAFETY_TYPE_MAP.get(raw_val, "Unknown")
                            value_str = f"{raw_val} => {mapped}"
                            tag = 'text_value'
                        else:
                            value_str = str(raw_val)
                            tag = 'numeric_value'

                self.tree.insert(
                    "",
                    "end",
                    values=(f"0x{reg['address']:04X}", reg["description"], value_str),
                    tags=(tag,)
                )

        except ModbusException as e:
            messagebox.showerror("Modbus Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            client.close()

def parse_args():
    parser = argparse.ArgumentParser(description="Inverter Modbus GUI (All Holding Registers)")
    parser.add_argument("--host", default="192.168.0.100", help="Inverter IP address")
    return parser.parse_args()

def main():
    args = parse_args()
    root = tk.Tk()
    app = ModbusGUI(root, default_ip=args.host)
    root.mainloop()

if __name__ == "__main__":
    main()
