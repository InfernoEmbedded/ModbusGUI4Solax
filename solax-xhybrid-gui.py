#!/usr/bin/env python3
import argparse
import tkinter as tk
from tkinter import ttk, messagebox

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Import your separate holding register definitions
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
# Helper Functions
###############################################################################
def to_signed_16(val: int) -> int:
    """Interpret 0..65535 as -32768..32767 if sign bit is set."""
    if val & 0x8000:
        return val - 0x10000
    return val

def format_scaled_value(raw_val: int, scale: float, signed: bool) -> float:
    """Convert raw (uint16) to signed/unsigned int, then scale to float."""
    val_int = to_signed_16(raw_val) if signed else raw_val
    return val_int * scale

def format_display_str(value: float, unit: str) -> str:
    """Convert float to string, e.g. 230.0 => '230.000 V'."""
    if unit:
        return f"{value:.3f} {unit}"
    return f"{value:.3f}"

###############################################################################
# RowTooltip: show raw & hex data for each row on hover
###############################################################################
class RowTooltip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None
        self.last_row_id = None
        self.row_tooltip_data = {}  # row_id => (raw_text, hex_text)

        self.widget.bind("<Motion>", self._on_mouse_move)
        self.widget.bind("<Leave>", self._on_mouse_leave)

    def set_row_data(self, row_id, raw_text, hex_text):
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
                raw_str, hex_str = self.row_tooltip_data[row_id]
                tip_text = f"Raw: {raw_str}\nHex: {hex_str}"
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
# Main GUI with 'Holding Registers' tab
###############################################################################
class ModbusGUI:
    def __init__(self, master, default_ip="192.168.0.100", update_interval=10):
        self.master = master
        self.master.title("Inverter Modbus Reader (Tabs)")

        self.update_interval = update_interval

        ######################
        # 1) Connection Frame
        ######################
        connection_frame = ttk.LabelFrame(master, text="Connection Settings")
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # IP & Port
        ttk.Label(connection_frame, text="IP Address:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ip_entry = ttk.Entry(connection_frame, width=15)
        self.ip_entry.insert(0, default_ip)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.port_entry = ttk.Entry(connection_frame, width=6)
        self.port_entry.insert(0, "502")
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        # Interval
        ttk.Label(connection_frame, text="Update Interval (s):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.interval_entry = ttk.Entry(connection_frame, width=6)
        self.interval_entry.insert(0, str(update_interval))
        self.interval_entry.grid(row=1, column=1, padx=5, pady=5)

        # Connect button
        ttk.Button(connection_frame, text="Connect", command=self.on_connect)\
            .grid(row=1, column=3, padx=5, pady=5, sticky="e")

        ###########################
        # 2) Notebook for tabs
        ###########################
        self.notebook = ttk.Notebook(master)
        self.notebook.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Create a frame for the 'Holding Registers' tab
        self.holding_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.holding_tab, text="Holding Registers")

        # Inside the holding_tab, place the Treeview + scrollbar
        # We'll store the table in a subframe
        table_frame = ttk.Frame(self.holding_tab)
        table_frame.pack(fill="both", expand=True)

        cols = ("address", "description", "value")
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings')
        self.tree.heading("address", text="Register Address")
        self.tree.heading("description", text="Description")
        self.tree.heading("value", text="Value")

        self.tree.column("address", width=140, anchor="e")
        self.tree.column("description", width=320, anchor="w")
        self.tree.column("value", width=220, anchor="w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Layout: Table left, scrollbar on right
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # RowTooltip
        self.tooltip = RowTooltip(self.tree)

        ######################
        # 3) Resizing
        ######################
        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

        ######################
        # 4) Holding registers
        ######################
        self.register_defs = HoldingRegisterDefinitions()
        self.registers = self.register_defs.get_registers()

        # Track numeric changes
        self.prev_numeric_values = {}

    def on_connect(self):
        """User clicked 'Connect'."""
        # Parse new interval
        try:
            new_interval = int(self.interval_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Interval", "Please enter a valid integer for the update interval.")
            return
        self.update_interval = new_interval

        # Clear table & tooltips
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.tooltip.row_tooltip_data.clear()

        # Insert empty rows
        self.address_to_rowid = {}
        for reg in self.registers:
            addr_hex = f"0x{reg['address']:04X}"
            desc = reg["description"]
            row_id = self.tree.insert("", "end", values=(addr_hex, desc, ""))
            self.address_to_rowid[reg["address"]] = row_id
            self.prev_numeric_values[reg["address"]] = None

        # Initial read
        self.fetch_data()

        # If interval>0, schedule periodic
        if self.update_interval > 0:
            self.master.after(self.update_interval * 1000, self.periodic_fetch)

    def periodic_fetch(self):
        """Called periodically if update_interval>0."""
        self.fetch_data()
        self.master.after(self.update_interval * 1000, self.periodic_fetch)

    def fetch_data(self):
        """Reads registers, updates table, sets color for changes, etc."""
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())

        client = ModbusTcpClient(host=ip, port=port)
        if not client.connect():
            messagebox.showerror("Connection Error", f"Failed to connect to {ip}:{port}")
            return

        try:
            for reg in self.registers:
                row_id = self.address_to_rowid[reg["address"]]
                resp = client.read_holding_registers(address=reg["address"], count=reg["length"])
                if resp.isError():
                    raw_str, hex_str = ("Error", "Error")
                    display_str = "Error reading"
                    color_tag = "white_bg"
                else:
                    raw_list = resp.registers
                    if len(raw_list) == 1:
                        # Single numeric or special
                        raw_str = str(raw_list[0])
                        hex_str = f"0x{raw_list[0]:04X}"

                        if reg["address"] == 0x001D:
                            # Safety Type
                            raw_val = raw_list[0]
                            mapped = SAFETY_TYPE_MAP.get(raw_val, "Unknown")
                            display_str = f"{raw_val} => {mapped}"
                            color_tag = "white_bg"
                            self.prev_numeric_values[reg["address"]] = None
                        else:
                            raw_val = raw_list[0]
                            scale = reg.get("scale", 1.0)
                            unit  = reg.get("unit", "")
                            signed= reg.get("signed", False)

                            new_val = format_scaled_value(raw_val, scale, signed)
                            display_str = format_display_str(new_val, unit)

                            old_val = self.prev_numeric_values[reg["address"]]
                            if old_val is None:
                                color_tag = "white_bg"
                            else:
                                if new_val > old_val:
                                    color_tag = "bg_green"
                                elif new_val < old_val:
                                    color_tag = "bg_red"
                                else:
                                    color_tag = "white_bg"

                            self.prev_numeric_values[reg["address"]] = new_val

                    else:
                        # Multi => ASCII text
                        raw_str = "[" + ", ".join(str(x) for x in raw_list) + "]"
                        hex_str = "[" + ", ".join(f"0x{x:04X}" for x in raw_list) + "]"

                        # Convert to ASCII
                        chars = []
                        for val in raw_list:
                            high = (val >> 8) & 0xFF
                            low  = val & 0xFF
                            chars.append(chr(high))
                            chars.append(chr(low))
                        display_str = "".join(chars).strip()
                        color_tag = "white_bg"
                        self.prev_numeric_values[reg["address"]] = None

                # Update row
                addr_hex = f"0x{reg['address']:04X}"
                desc = reg["description"]
                self.tree.item(row_id, values=(addr_hex, desc, display_str))

                # Color
                self._set_row_bg(row_id, color_tag)

                # Tooltip
                self.tooltip.set_row_data(row_id, raw_str, hex_str)

        except ModbusException as e:
            messagebox.showerror("Modbus Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            client.close()

    def _set_row_bg(self, row_id, color_tag):
        self.tree.tag_configure('bg_green', background='LightGreen')
        self.tree.tag_configure('bg_red', background='LightSalmon')
        self.tree.tag_configure('white_bg', background='white')
        if not color_tag:
            color_tag = 'white_bg'
        self.tree.item(row_id, tags=(color_tag,))


def parse_args():
    parser = argparse.ArgumentParser(description="Modbus GUI with 'Holding Registers' tab.")
    parser.add_argument("--host", default="192.168.0.100", help="Inverter IP address")
    parser.add_argument("--interval", type=int, default=10,
                        help="Default update interval in seconds (GUI override).")
    return parser.parse_args()

def main():
    args = parse_args()
    root = tk.Tk()
    app = ModbusGUI(root, default_ip=args.host, update_interval=args.interval)
    root.mainloop()

if __name__ == "__main__":
    main()
