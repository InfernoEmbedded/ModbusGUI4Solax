# register_utils.py

def registers_to_ascii(raw_list):
    """Convert a list of 16-bit registers to an ASCII string."""
    return "".join(chr((val >> 8) & 0xFF) + chr(val & 0xFF) for val in raw_list).strip()

def convert_raw_to_float(raw_val, scale, signed):
    """Apply sign conversion and scaling to a 16-bit register value."""
    if signed and (raw_val & 0x8000):
        raw_val -= 0x10000
    return raw_val * scale

def format_display_str(value, scale, unit):
    """Format the numeric value with appropriate precision and optional unit."""
    if scale == 1.0:
        val_str = f"{int(value)}"
    elif abs(scale - 0.1) < 1e-9:
        val_str = f"{value:.1f}"
    elif abs(scale - 0.01) < 1e-9:
        val_str = f"{value:.2f}"
    else:
        val_str = f"{value:.3f}"
    return f"{val_str} {unit}" if unit else val_str

class RegisterDefinitionsBase:
    """
    Base class to provide common register rendering logic.
    The render_register method handles:
      - Multi-register values (as ASCII)
      - Single registers (scaled, signed, and formatted)
    """
    def render_register(self, reg, raw_list):
        if reg["length"] > 2:
            return registers_to_ascii(raw_list)
        raw_val = raw_list[0]
        scale = reg.get("scale", 1.0)
        unit = reg.get("unit", "")
        signed = reg.get("signed", False)
        value = convert_raw_to_float(raw_val, scale, signed)
        return format_display_str(value, scale, unit)
