import usb_hid

# SAMD21 usb_hid can only support one report
# while the RP2040 one can support more than one.

PROXIMITY_AXIS_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,       # USAGE_PAGE (Generic Desktop)
    0x09, 0x05,       # USAGE (Game Pad)
    0xA1, 0x01,       # COLLECTION (Application)
    0x85, 0x01,       #   REPORT_ID (1)
    0x05, 0x09,       #   USAGE_PAGE (Button)
    0x19, 0x01,       #   USAGE_MINIMUM (Button 1)
    0x29, 0x02,       #   USAGE_MAXIMUM (Button 2)
    0x15, 0x00,       #   LOGICAL_MINIMUM (0)
    0x25, 0x01,       #   LOGICAL_MAXIMUM (1)
    0x75, 0x01,       #   REPORT_SIZE (1)
    0x95, 0x02,       #   REPORT_COUNT (2)
    0x81, 0x02,       #   INPUT (Data,Var,Abs)
    0x75, 0x06,       #   REPORT_SIZE (6)
    0x95, 0x01,       #   REPORT_COUNT (1)
    0x81, 0x03,       #   INPUT (Cnst,Var,Abs)
    0x05, 0x01,       #   USAGE_PAGE (Generic Desktop)
    0x09, 0x36,       #   USAGE (Slider)
    0x15, 0x80,       #   LOGICAL_MINIMUM (-128)
    0x25, 0x7F,       #   LOGICAL_MAXIMUM (127)
    0x75, 0x08,       #   REPORT_SIZE (8)
    0x95, 0x01,       #   REPORT_COUNT (1)
    0x81, 0x02,       #   INPUT (Data,Var,Abs)
    0xC0              # END_COLLECTION
))

proximity_axis = usb_hid.Device(
    report_descriptor=PROXIMITY_AXIS_REPORT_DESCRIPTOR,
    # Must match Usage Page above!
    usage_page=0x01,           # Generic Desktop Control
    # Must match Usage above!
    usage=0x05,                # Gamepad
    # Must match Report ID above!
    report_ids=(1,),           # Descriptor uses report ID 1.
    # Must match number of bytes above!
    in_report_lengths=(2,),    # This gamepad sends 2 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable((proximity_axis,))
