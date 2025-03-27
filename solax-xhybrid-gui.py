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
    # Overlapping codes for X3 and X1 start here.
    22: "Israel (X3) / EN50438_Ireland (X1)",
    23: "Czech_CEZ (X3) / Philippines (X1)",
    24: "UNE_206 (X3) / Czech_PPDS (X1)",
    25: "EN50438_Poland (X3) / Czech_50438 (X1)",
    # X3-only codes from 26-32
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
        self.ip_entry.insert(0, default_ip)  # Use default IP from CLI or fallback
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
        self.tree.column("address", width=120, anchor="e")  # Right-align for numeric addresses
        self.tree.column("description", width=250, anchor="w")  # Left-align for text
        self.tree.column("value", width=100, anchor="w")  # We'll refine single vs multi with tags

        # Tag-based alignment
        self.tree.tag_configure('numeric_value', anchor='e')
        self.tree.tag_configure('text_value', anchor='w')

        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Registers of interest
        self.registers = [
            {"address": 0x0000, "length": 7, "description": "Series Number"},
            {"address": 0x0007, "length": 7, "description": "Factory Name"},
            {"address": 0x000E, "length": 7, "description": "Module Name"},
            {"address": 0x0015, "length": 1, "description": "VpvStart (Hybrid) (0.1V)"},
            {"address": 0x0016, "length": 1, "description": "TimeStart (1s)"},
            {"address": 0x0017, "length": 1, "description": "VpvHighStop (Hybrid) (0.1V)"},
            {"address": 0x0018, "length": 1, "description": "VpvLowStop (Hybrid) (0.1V)"},
            {"address": 0x0019, "length": 1, "description": "VacMinProtect (0.1V)"},
            {"address": 0x001A, "length": 1, "description": "VacMaxProtect (0.1V)"},
            {"address": 0x001B, "length": 1, "description": "FacMinProtect (0.01Hz)"},
            {"address": 0x001C, "length": 1, "description": "FacMaxProtect (0.01Hz)"},
            # The special one: Safety Type
            {"address": 0x001D, "length": 1, "description": "Safety Type (Numeric + String)"},
        ]

        # Configure window resizing
        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

    def connect_and_read(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())

        client = ModbusTcpClient(host=ip, port=port)
        if not client.connect():
            messagebox.showerror("Connection Error", f"Failed to connect to inverter at {ip}:{port}")
            return

        self.tree.delete(*self.tree.get_children())

        try:
            for reg in self.registers:
                response = client.read_holding_registers(address=reg["address"], count=reg["length"])
                if response.isError():
                    value_str = "Error reading"
                    tag = 'text_value'
                else:
                    if reg["length"] > 1:
                        # Multi-register, interpret as text
                        chars = [
                            chr((r >> 8) & 0xFF) + chr(r & 0xFF)
                            for r in response.registers
                        ]
                        value_str = "".join(chars).strip()
                        tag = 'text_value'
                    else:
                        # Single register, typically numeric
                        raw_val = response.registers[0]
                        tag = 'numeric_value'

                        # Check if it's the safety-type register
                        if reg["address"] == 0x001D:
                            # Show code plus string
                            mapped = SAFETY_TYPE_MAP.get(raw_val, "Unknown")
                            value_str = f"{raw_val} => {mapped}"
                            # We'll treat it as text for better readability
                            tag = 'text_value'
                        else:
                            value_str = str(raw_val)

                self.tree.insert(
                    "",
                    "end",
                    values=(hex(reg["address"]), reg["description"], value_str),
                    tags=(tag,)
                )
        except ModbusException as e:
            messagebox.showerror("Modbus Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            client.close()

def parse_args():
    parser = argparse.ArgumentParser(description="Inverter Modbus GUI")
    parser.add_argument("--host", default="192.168.0.100", help="Inverter IP address")
    return parser.parse_args()

def main():
    args = parse_args()
    root = tk.Tk()
    app = ModbusGUI(root, default_ip=args.host)
    root.mainloop()

if __name__ == "__main__":
    main()
