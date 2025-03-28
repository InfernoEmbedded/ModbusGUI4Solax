# Modbus GUI 4 Solax

## Overview
This project is a GUI application for interacting with a Solax X1/X3 Hybrid Inverter via Modbus TCP. It supports reading various registers including holding, input, self-test, and parallel registers.

## Supported Inverters
- Solax X1/X3 G3 Hybrid inverters and battery chargers

## Features
- **Tkinter GUI**: A user-friendly graphical interface built with Tkinter, featuring separate tabs for each register category.
- **Dynamic Data Fetching**: Periodically retrieves and updates data from the inverter with visual cues to indicate changes in numeric values.

## Installation
Ensure you have Python 3 installed along with the required dependencies:

- **pymodbus**
- **tkinter** (usually included with Python)

Install pymodbus using pip:

```bash
pip install pymodbus
```

## Usage
Run the GUI application from the command line:

```bash
python solax-xhybrid-gui.py --host <inverter_ip> --interval <update_interval_in_seconds>
```

Default values are IP `192.168.0.100` and an update interval of `10` seconds.

## License
This project is licensed under the GNU General Public License v3.0 (GPLv3). See the [LICENSE](gpl-3.0.txt) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.
