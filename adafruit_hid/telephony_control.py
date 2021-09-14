# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.telephony_control.TelephonyControl`
====================================================

* Author(s): Dan Halbert
"""

import sys

if sys.implementation.version[0] < 3:
    raise ImportError(
        "{0} is not supported in CircuitPython 2.x or lower".format(__name__)
    )

# pylint: disable=wrong-import-position
import struct
import time
from . import find_device

class TelephonyControl:
    """Send TelephonyControl code reports, used by headsets."""

    def __init__(self, devices):
        """Create a TelephonyControl object that will send Telephony Control Device HID reports.

        Devices can be a list of devices that includes a Telephony Control device or a CC device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._telephony_device = find_device(devices, usage_page=0x0B, usage=0x05)

        # Reuse this bytearray to send telephony reports.
        self._report = bytearray(2)

        # Do a no-op to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.send(0x0)
        except OSError:
            time.sleep(1)
            self.send(0x0)

    def send(self, telephony_code):
        """Send a report to do the specified telephony control action,
        and then stop the action (so it will not repeat).

        :param telephony_code: a 16-bit telephony control code.

        Examples::

            from adafruit_hid.telephony_control_code import TelephonyControlCode

            # Raise volume.
            telephony_control.send(TelephonyControlCode.VOLUME_INCREMENT)

            # Advance to next track (song).
            telephony_control.send(TelephonyControlCode.SCAN_NEXT_TRACK)
        """
        self.press(telephony_code)
        self.release()

    def press(self, telephony_code):
        """Send a report to indicate that the given key has been pressed.
        Only one telephony control action can be pressed at a time, so any one
        that was previously pressed will be released.

        :param telephony_code: a 16-bit telephony control code.

        Examples::

            from adafruit_hid.telephony_control_code import TelephonyControlCode

            # Raise volume for 0.5 seconds
            telephony_control.press(TelephonyControlCode.VOLUME_INCREMENT)
            time.sleep(0.5)
            telephony_control.release()
        """
        struct.pack_into("<H", self._report, 0, telephony_code)
        self._telephony_device.send_report(self._report)

    def release(self):
        """Send a report indicating that the telephony control key has been
        released. Only one telephony control key can be pressed at a time.

        Examples::

            from adafruit_hid.telephony_control_code import TelephonyControlCode

            # Raise volume for 0.5 seconds
            telephony_control.press(TelephonyControlCode.VOLUME_INCREMENT)
            time.sleep(0.5)
            telephony_control.release()
        """
        self._report[0] = self._report[1] = 0x0
        self._telephony_device.send_report(self._report)
