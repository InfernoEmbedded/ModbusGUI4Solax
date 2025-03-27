#!/usr/bin/env python3
import argparse
import tkinter as tk
from tkinter import ttk, messagebox

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Import the separate holding register definitions
from HoldingRegisterDefinitions import HoldingRegisterDefinitions


###############################################################################
# Safety type mappings for register 0x001D (numeric => textual).
###############################################################################
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
    22: "Israel (X3) / EN50438_Ireland (X1)",
    23: "Czech_CEZ (X3) / Philippines (X1)",
    24: "UNE_206 (X3) / Czech_PPDS (X1)",
    25: "EN50438_Poland (X3) / Czech_50438 (X1)",
    26: "EN50438_Portugal (X3)",
    27: "PEA (X3)",
    28: "MEA (X3)",
    29: "EN50438_Sweden (X3)",
    30: "Philippines (X3)",
    31: "EN50438_Slovenia (X3)",
    32: "CEI0_16 (X3)"
}

###############################################################################
# Helper functions
###############################################################################
def to_signed_16(val: int) -> int:
    """Interpret 0..65535 as -32768..32767 if sign bit is set."""
    if val & 0x8000:
        return val - 0x10000
    return val

def format_scaled_value(raw_val: int, scale: float, unit: str, signed: bool) -> str:
    """Scale and format a single numeric register value, e.g. '230.0 V' or '-10.0 A'."""
    val_int = to_signed_16(raw_val) if signed else raw_val
    scaled = val_int * scale
    return f"{scaled:.3f} {unit}".strip() if unit else f"{scaled:.3f}"


###############################################################################
# A lightweight RowTooltip class to show raw+hex data in a tooltip on hover
###############################################################################
class RowTooltip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None
        self.last_row_id = None

        # Dict mapping row_id => (raw_text, hex_text)
        self.row_tooltip_data = {}

        # Bind events
        self.widget.bind("<Motion>", self._on_mouse_move)
        self.widget.bind("<Leave>", self._on_mouse_leave)

    def set_row_data(self, row_id, raw_text, hex_text):
        """Store raw & hex data for a given Treeview row ID."""
        self.row_tooltip_data[row_id] = (raw_text, hex_text)

    def _on_mouse_move(self, event):
        row_id = self.widget.identify_row(event.y)
        if not row_id:
            self._hide_tip()
            return

        if row_id != self.last_row_id:
            self.last_row_id = row_id
            self._hide_tip()

            if row_id in self.row_tooltip_data:
                raw_val, hex_val = self.row_tooltip_data[row_id]
                tip_text = f"Raw: {raw_val}\nHex: {hex_val}"
                self._show_tip(tip_text, event.x_root + 20, event.y_root + 10)

    def _on_mouse_leave(self, event):
        self._hide_tip()

    def _show_tip(self, text, x, y):
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.overrideredirect(True)
        tw.attributes("-topmost", True)
        label = tk.Label(
            tw, text=text, justify="left", background="#ffffe0",
            relief="solid", borderwidth=1, font=("tahoma", 8)
        )
        label.pack(ipadx=1)
        tw.geometry(f"+{x}+{y}")

    def _hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None


###############################################################################
# Main GUI class
###############################################################################
class ModbusGUI:
    def __init__(self, master, default_ip="192.168.0.100"):
        self.master = master
        self.master.title("Inverter Modbus TCP Reader - Scroll + Tooltip")

        ######################
        # 1) Connection Frame
        ######################
        connection_frame = ttk.LabelFrame(master, text="Connection Settings")
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(connection_frame, text="IP Address:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ip_entry = ttk.Entry(connection_frame, width=20)
        self.ip_entry.insert(0, default_ip)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.insert(0, "502")
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(connection_frame, text="Connect & Read", command=self.connect_and_read)\
            .grid(row=0, column=4, padx=5, pady=5)

        ######################
        # 2) Table + scrollbar
        ######################
        table_frame = ttk.Frame(master)
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        cols = ("address", "description", "value")
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings')
        self.tree.heading("address", text="Register Address")
        self.tree.heading("description", text="Description")
        self.tree.heading("value", text="Value")

        self.tree.column("address", width=140, anchor="e")
        self.tree.column("description", width=320, anchor="w")
        self.tree.column("value", width=220, anchor="w")

        # Vertical scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # RowTooltip for raw+hex data on hover
        self.tooltip = RowTooltip(self.tree)

        ######################
        # 3) Window resizing
        ######################
        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

        ######################
        # 4) Holding registers
        ######################
        self.register_defs = HoldingRegisterDefinitions()
        self.registers = self.register_defs.get_registers()

    def connect_and_read(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())

        client = ModbusTcpClient(host=ip, port=port)
        if not client.connect():
            messagebox.showerror("Connection Error", f"Failed to connect to {ip}:{port}")
            return

        self.tree.delete(*self.tree.get_children())
        self.tooltip.row_tooltip_data.clear()

        try:
            for reg in self.registers:
                resp = client.read_holding_registers(address=reg["address"], count=reg["length"])
                if resp.isError():
                    raw_str  = "Error"
                    hex_str  = "Error"
                    display_str = "Error reading"
                else:
                    raw_list = resp.registers

                    # Build raw decimal string
                    if len(raw_list) == 1:
                        raw_str = str(raw_list[0])
                        hex_str = f"0x{raw_list[0]:04X}"
                    else:
                        raw_str = "[" + ", ".join(str(x) for x in raw_list) + "]"
                        hex_str = "[" + ", ".join(f"0x{x:04X}" for x in raw_list) + "]"

                    # Build the decorated or scaled display
                    if reg["length"] > 1:
                        # multi-register => interpret as ASCII text
                        chars = []
                        for val in raw_list:
                            high_byte = (val >> 8) & 0xFF
                            low_byte = val & 0xFF
                            chars.append(chr(high_byte))
                            chars.append(chr(low_byte))
                        display_str = "".join(chars).strip()
                    else:
                        # single register => numeric or special
                        raw_val = raw_list[0]
                        if reg["address"] == 0x001D:
                            mapped = SAFETY_TYPE_MAP.get(raw_val, "Unknown")
                            display_str = f"{raw_val} => {mapped}"
                        else:
                            scale = reg.get("scale", 1.0)
                            unit  = reg.get("unit", "")
                            signed= reg.get("signed", False)
                            if "scale" in reg or "unit" in reg:
                                display_str = format_scaled_value(raw_val, scale, unit, signed)
                            else:
                                display_str = str(raw_val)

                # Insert row
                addr_hex = f"0x{reg['address']:04X}"
                desc = reg["description"]
                row_id = self.tree.insert("", "end", values=(addr_hex, desc, display_str))

                # Attach raw & hex to tooltip data
                self.tooltip.set_row_data(row_id, raw_str, hex_str)

        except ModbusException as e:
            messagebox.showerror("Modbus Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            client.close()


def parse_args():
    parser = argparse.ArgumentParser(description="Modbus GUI with tooltip for raw+hex data, plus vertical scrollbar.")
    parser.add_argument("--host", default="192.168.0.100", help="Inverter IP address")
    return parser.parse_args()

def main():
    args = parse_args()
    root = tk.Tk()
    app = ModbusGUI(root, default_ip=args.host)
    root.mainloop()

if __name__ == "__main__":
    main()
