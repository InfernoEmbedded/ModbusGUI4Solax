#!/usr/bin/env python3
import argparse
import tkinter as tk
from tkinter import ttk, messagebox

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from HoldingRegisterDefinitions import HoldingRegisterDefinitions
from InputRegisterDefinitions import InputRegisterDefinitions
from SelfTestInputRegisterDefinitions import SelfTestInputRegisterDefinitions
from ParallelInputRegisterDefinitions import ParallelInputRegisterDefinitions

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
    def __init__(self, master, default_ip="192.168.0.100", default_port="502", update_interval=10):
        self.master = master
        self.master.title("Solax X1/X3 Hybrid Inverter Modbus GUI")

        self.update_interval = update_interval
        self.invalid_parallel_registers = set()

        # Connection frame
        connection_frame = ttk.LabelFrame(master, text="Connection Settings")
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(connection_frame, text="IP:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ip_entry = ttk.Entry(connection_frame, width=15)
        self.ip_entry.insert(0, default_ip)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.port_entry = ttk.Entry(connection_frame, width=6)
        self.port_entry.insert(0, default_port)
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(connection_frame, text="Interval(s):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.interval_entry = ttk.Entry(connection_frame, width=5)
        self.interval_entry.insert(0, str(update_interval))
        self.interval_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(connection_frame, text="Connect", command=self.on_connect)\
            .grid(row=0, column=6, padx=5, pady=5, sticky="e")

        # Notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.holding_tab = self.create_tab("Holding Registers")
        self.input_tab = self.create_tab("Input Registers")
        self.selftest_tab = self.create_tab("Self Test Registers")
        self.parallel_tab = self.create_tab("Parallel Registers")

        # Create treeviews in each tab
        self.tree = self.create_register_table(self.holding_tab)
        self.tooltip = RowTooltip(self.tree)

        self.tree_input = self.create_register_table(self.input_tab)
        self.tooltip_input = RowTooltip(self.tree_input)

        self.tree_test = self.create_register_table(self.selftest_tab)
        self.tooltip_test = RowTooltip(self.tree_test)

        self.tree_parallel = self.create_register_table(self.parallel_tab)
        self.tooltip_parallel = RowTooltip(self.tree_parallel)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

        # Register definitions
        self.holding_defs = HoldingRegisterDefinitions()
        self.holding_registers = self.holding_defs.get_registers()

        self.input_defs = InputRegisterDefinitions()
        self.input_registers = self.input_defs.get_registers()

        self.selftest_defs = SelfTestInputRegisterDefinitions()
        self.selftest_registers = self.selftest_defs.get_registers()

        self.parallel_defs = ParallelInputRegisterDefinitions()
        self.parallel_registers = self.parallel_defs.get_registers()

        # Dictionaries to track row IDs and previous numeric values
        self.prev_numeric_values = {}
        self.prev_numeric_values_input = {}
        self.prev_numeric_values_test = {}
        self.prev_numeric_values_parallel = {}

    def create_tab(self, title):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)
        return tab

    def create_register_table(self, parent, columns=("address", "desc", "value"), widths=(120, 300, 150)):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, width in zip(columns, widths):
            tree.heading(col, text=col.capitalize())
            anchor = "e" if col == "address" else "w"
            stretch = False if col in ("address", "value") else True
            tree.column(col, width=width, anchor=anchor, stretch=stretch)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        return tree

    def get_modbus_client(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())
        client = ModbusTcpClient(host=ip, port=port)
        if not client.connect():
            raise ConnectionError(f"Could not connect to {ip}:{port}")
        return client

    def format_raw_list(self, raw_list):
        if len(raw_list) == 1:
            raw_str = str(raw_list[0])
            hex_str = f"0x{raw_list[0]:04X}"
        else:
            raw_str = "[" + ", ".join(str(v) for v in raw_list) + "]"
            hex_str = "[" + ", ".join(f"0x{v:04X}" for v in raw_list) + "]"
        return raw_str, hex_str

    def determine_color(self, reg, disp_str, prev_values):
        if reg["length"] == 1:
            try:
                numeric_val = float(disp_str.split()[0])
            except:
                numeric_val = None
            old_val = prev_values.get(reg["address"])
            if old_val is None or numeric_val is None:
                color_tag = "white_bg"
            else:
                color_tag = "bg_green" if numeric_val > old_val else ("bg_red" if numeric_val < old_val else "white_bg")
            prev_values[reg["address"]] = numeric_val
        else:
            color_tag = "white_bg"
            prev_values[reg["address"]] = None
        return color_tag

    def set_row_bg(self, tree_widget, row_id, color_tag):
        tree_widget.tag_configure('bg_green', background='LightGreen')
        tree_widget.tag_configure('bg_red', background='LightSalmon')
        tree_widget.tag_configure('white_bg', background='white')
        tree_widget.item(row_id, tags=(color_tag,))

    def fetch_and_update(self, reg_list, tree, address_to_rowid, prev_values, defs_obj, read_func):
        try:
            client = self.get_modbus_client()
            for reg in reg_list:
                row_id = address_to_rowid[reg["address"]]
                resp = read_func(client, reg["address"], reg["length"])
                if resp.isError():
                    raw_str, hex_str = "Error", "Error"
                    disp_str = "Error reading"
                    color_tag = "white_bg"
                else:
                    raw_list = resp.registers
                    raw_str, hex_str = self.format_raw_list(raw_list)
                    disp_str = defs_obj.render_register(reg, raw_list)
                    color_tag = self.determine_color(reg, disp_str, prev_values)
                tree.item(row_id, values=(f"0x{reg['address']:04X}", reg["description"], disp_str))
                self.set_row_bg(tree, row_id, color_tag)
                if tree == self.tree:
                    self.tooltip.set_row_data(row_id, raw_str, hex_str)
                elif tree == self.tree_input:
                    self.tooltip_input.set_row_data(row_id, raw_str, hex_str)
                elif tree == self.tree_test:
                    self.tooltip_test.set_row_data(row_id, raw_str, hex_str)
            client.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_holding_data(self):
        self.fetch_and_update(
            self.holding_registers,
            self.tree,
            self.address_to_rowid,
            self.prev_numeric_values,
            self.holding_defs,
            lambda client, addr, count: client.read_holding_registers(address=addr, count=count)
        )

    def fetch_data_input(self):
        self.fetch_and_update(
            self.input_registers,
            self.tree_input,
            self.address_to_rowid_input,
            self.prev_numeric_values_input,
            self.input_defs,
            lambda client, addr, count: client.read_input_registers(address=addr, count=count)
        )

    def fetch_data_selftest(self):
        self.fetch_and_update(
            self.selftest_registers,
            self.tree_test,
            self.address_to_rowid_test,
            self.prev_numeric_values_test,
            self.selftest_defs,
            lambda client, addr, count: client.read_input_registers(address=addr, count=count)
        )

    def fetch_data_parallel(self):
        try:
            client = self.get_modbus_client()
            for reg in self.parallel_registers:
                address = reg["address"]
                row_id = self.address_to_rowid_parallel[address]
                if address in self.invalid_parallel_registers:
                    self.tree_parallel.item(row_id, values=(f"0x{address:04X}", reg["description"], "Invalid (skipped)"))
                    continue
                resp = client.read_input_registers(address=address, count=reg["length"])
                if resp.isError():
                    self.invalid_parallel_registers.add(address)
                    self.tree_parallel.item(row_id, values=(f"0x{address:04X}", reg["description"], "Invalid (unreadable)"))
                    continue
                raw_list = resp.registers
                raw_str, hex_str = self.format_raw_list(raw_list)
                disp_str = self.parallel_defs.render_register(reg, raw_list)
                color_tag = self.determine_color(reg, disp_str, self.prev_numeric_values_parallel)
                self.tree_parallel.item(row_id, values=(f"0x{address:04X}", reg["description"], disp_str))
                self.set_row_bg(self.tree_parallel, row_id, color_tag)
                self.tooltip_parallel.set_row_data(row_id, raw_str, hex_str)
            client.close()
        except Exception:
            pass

    def on_connect(self):
        try:
            new_interval = int(self.interval_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Interval", "Please enter a valid integer.")
            return
        self.update_interval = new_interval

        # Initialize treeviews and dictionaries.
        self.address_to_rowid = {}
        self.tree.delete(*self.tree.get_children())
        self.tooltip.row_tooltip_data.clear()
        for reg in self.holding_registers:
            row_id = self.tree.insert("", "end", values=(f"0x{reg['address']:04X}", reg["description"], ""))
            self.address_to_rowid[reg["address"]] = row_id
            self.prev_numeric_values[reg["address"]] = None

        self.address_to_rowid_input = {}
        self.tree_input.delete(*self.tree_input.get_children())
        self.tooltip_input.row_tooltip_data.clear()
        for reg in self.input_registers:
            row_id = self.tree_input.insert("", "end", values=(f"0x{reg['address']:04X}", reg["description"], ""))
            self.address_to_rowid_input[reg["address"]] = row_id
            self.prev_numeric_values_input[reg["address"]] = None

        self.address_to_rowid_test = {}
        self.tree_test.delete(*self.tree_test.get_children())
        self.tooltip_test.row_tooltip_data.clear()
        for reg in self.selftest_registers:
            row_id = self.tree_test.insert("", "end", values=(f"0x{reg['address']:04X}", reg["description"], ""))
            self.address_to_rowid_test[reg["address"]] = row_id
            self.prev_numeric_values_test[reg["address"]] = None

        self.address_to_rowid_parallel = {}
        self.tree_parallel.delete(*self.tree_parallel.get_children())
        self.tooltip_parallel.row_tooltip_data.clear()
        for reg in self.parallel_registers:
            row_id = self.tree_parallel.insert("", "end", values=(f"0x{reg['address']:04X}", reg["description"], ""))
            self.address_to_rowid_parallel[reg["address"]] = row_id
            self.prev_numeric_values_parallel[reg["address"]] = None

        # Initial fetch of all register sets.
        self.fetch_all_data()

        if self.update_interval > 0:
            self.master.after(self.update_interval * 1000, self.periodic_fetch_all)

    def fetch_all_data(self):
        self.fetch_holding_data()
        self.fetch_data_input()
        self.fetch_data_selftest()
        self.fetch_data_parallel()

    def periodic_fetch_all(self):
        self.fetch_all_data()
        self.master.after(self.update_interval * 1000, self.periodic_fetch_all)

def parse_args():
    parser = argparse.ArgumentParser(description="Solax X1/X3 Hybrid Inverter Modbus GUI.")
    parser.add_argument("--host", default="192.168.0.100", help="Inverter IP. Optionally specify as host:port")
    parser.add_argument("--interval", type=int, default=10, help="Update interval in seconds")
    args = parser.parse_args()
    if ':' in args.host:
        host, port_str = args.host.split(':', 1)
        try:
            port = int(port_str)
        except ValueError:
            parser.error("Port must be an integer when specified in host:port format")
        args.host = host
        args.port = port
    else:
        args.port = 502
    return args

def main():
    args = parse_args()
    root = tk.Tk()
    # Pass both host and port as default values for the GUI.
    app = ModbusGUI(root, default_ip=args.host, default_port=str(args.port), update_interval=args.interval)
    root.mainloop()

if __name__ == "__main__":
    main()
