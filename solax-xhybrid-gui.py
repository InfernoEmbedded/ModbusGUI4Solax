#!/usr/bin/env python3
import argparse
import tkinter as tk
from tkinter import ttk, messagebox

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Import definitions from the file above
from HoldingRegisterDefinitions import HoldingRegisterDefinitions

# RowTooltip for showing raw & hex data on hover
class RowTooltip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None
        self.last_row_id = None
        self.row_tooltip_data = {}
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
                raw_val, hex_val = self.row_tooltip_data[row_id]
                tip_text = f"Raw: {raw_val}\nHex: {hex_val}"
                self._show_tip(tip_text, event.x_root + 20, event.y_root + 10)

    def _on_mouse_leave(self, event):
        self._hide_tip()

    def _show_tip(self, text, x, y):
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.overrideredirect(True)
        tw.attributes("-topmost", True)
        label = tk.Label(tw, text=text, justify="left", background="#ffffe0",
                         relief="solid", borderwidth=1, font=("tahoma", 8))
        label.pack(ipadx=1)
        tw.geometry(f"+{x}+{y}")

    def _hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None


class ModbusGUI:
    def __init__(self, master, default_ip="192.168.0.100", update_interval=10):
        self.master = master
        self.master.title("Inverter Modbus Reader (renderRegister)")

        self.update_interval = update_interval

        # Connection frame
        connection_frame = ttk.LabelFrame(master, text="Connection Settings")
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(connection_frame, text="IP:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ip_entry = ttk.Entry(connection_frame, width=15)
        self.ip_entry.insert(0, default_ip)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.port_entry = ttk.Entry(connection_frame, width=6)
        self.port_entry.insert(0, "502")
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(connection_frame, text="Interval(s):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.interval_entry = ttk.Entry(connection_frame, width=5)
        self.interval_entry.insert(0, str(update_interval))
        self.interval_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(connection_frame, text="Connect", command=self.on_connect)\
            .grid(row=0, column=6, padx=5, pady=5, sticky="e")

        # Create a Notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Holding Registers tab
        self.holding_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.holding_tab, text="Holding Registers")

        # Table frame inside the holding_tab
        table_frame = ttk.Frame(self.holding_tab)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("address", "desc", "value"),
            show='headings'
        )
        self.tree.heading("address", text="Register Address")
        self.tree.heading("desc", text="Description")
        self.tree.heading("value", text="Value")

        # Prevent address/value columns from stretching:
        self.tree.column("address", width=120, anchor="e", stretch=False)
        self.tree.column("desc", width=300, anchor="w", stretch=True)
        self.tree.column("value", width=150, anchor="w", stretch=False)

        self.tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.tooltip = RowTooltip(self.tree)

        # Root window resizing
        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

        # Register definitions
        self.reg_defs = HoldingRegisterDefinitions()
        self.registers = self.reg_defs.get_registers()
        self.prev_numeric_values = {}

    def on_connect(self):
        try:
            new_int = int(self.interval_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Interval", "Please enter a valid integer.")
            return

        self.update_interval = new_int

        # Clear table
        self.tree.delete(*self.tree.get_children())
        self.tooltip.row_tooltip_data.clear()

        self.address_to_rowid = {}
        for r in self.registers:
            row_id = self.tree.insert("", "end", values=(f"0x{r['address']:04X}", r["description"], ""))
            self.address_to_rowid[r["address"]] = row_id
            # For numeric registers, track previous value
            if r["length"] == 1 and r["address"] != 0x001D:
                self.prev_numeric_values[r["address"]] = None
            else:
                self.prev_numeric_values[r["address"]] = None

        self.fetch_data()
        if self.update_interval > 0:
            self.master.after(self.update_interval * 1000, self.periodic_fetch)

    def periodic_fetch(self):
        self.fetch_data()
        self.master.after(self.update_interval * 1000, self.periodic_fetch)

    def fetch_data(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())

        client = ModbusTcpClient(host=ip, port=port)
        if not client.connect():
            messagebox.showerror("Connection Error", f"Could not connect to {ip}:{port}")
            return

        try:
            for reg in self.registers:
                row_id = self.address_to_rowid[reg["address"]]
                resp = client.read_holding_registers(
                    address=reg["address"],
                    count=reg["length"]
                )
                if resp.isError():
                    raw_str = "Error"
                    hex_str = "Error"
                    disp_str = "Error reading"
                    color_tag = "white_bg"
                else:
                    raw_list = resp.registers
                    # Build raw/hex text for tooltip
                    if len(raw_list) == 1:
                        raw_str = str(raw_list[0])
                        hex_str = f"0x{raw_list[0]:04X}"
                    else:
                        raw_str = "[" + ", ".join(str(v) for v in raw_list) + "]"
                        hex_str = "[" + ", ".join(f"0x{v:04X}" for v in raw_list) + "]"

                    # Use the new method in HoldingRegisterDefinitions
                    disp_str = self.reg_defs.renderRegister(reg, raw_list)

                    # Color tag if numeric single
                    if reg["length"] == 1 and reg["address"] != 0x001D:
                        numeric_val = self._try_parse_numeric(disp_str)
                        old_val = self.prev_numeric_values[reg["address"]]
                        if old_val is None or numeric_val is None:
                            color_tag = "white_bg"
                        else:
                            if numeric_val > old_val:
                                color_tag = "bg_green"
                            elif numeric_val < old_val:
                                color_tag = "bg_red"
                            else:
                                color_tag = "white_bg"
                        self.prev_numeric_values[reg["address"]] = numeric_val
                    else:
                        # multi or safety => always white
                        color_tag = "white_bg"
                        self.prev_numeric_values[reg["address"]] = None

                # Update row
                addr_hex = f"0x{reg['address']:04X}"
                desc = reg["description"]
                self.tree.item(row_id, values=(addr_hex, desc, disp_str))
                self._set_row_bg(row_id, color_tag)
                self.tooltip.set_row_data(row_id, raw_str, hex_str)

        except ModbusException as e:
            messagebox.showerror("Modbus Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            client.close()

    def _try_parse_numeric(self, disp_str):
        """
        Attempt to parse the displayed string as a float, ignoring unit if present.
        e.g. '230.000 V' => 230.0
        If parse fails, return None
        """
        parts = disp_str.split()
        try:
            return float(parts[0])
        except:
            return None

    def _set_row_bg(self, row_id, color_tag):
        self.tree.tag_configure('bg_green', background='LightGreen')
        self.tree.tag_configure('bg_red', background='LightSalmon')
        self.tree.tag_configure('white_bg', background='white')

        if not color_tag:
            color_tag = 'white_bg'
        self.tree.item(row_id, tags=(color_tag,))


def parse_args():
    parser = argparse.ArgumentParser(description="Modbus GUI with tab + minimal changes for column widths.")
    parser.add_argument("--host", default="192.168.0.100", help="Inverter IP")
    parser.add_argument("--interval", type=int, default=10, help="Update interval in seconds")
    return parser.parse_args()

def main():
    args = parse_args()
    root = tk.Tk()
    app = ModbusGUI(root, default_ip=args.host, update_interval=args.interval)
    root.mainloop()

if __name__ == "__main__":
    main()
