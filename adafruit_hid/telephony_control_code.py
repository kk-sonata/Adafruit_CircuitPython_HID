# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.telephony_control_code.TelephonyControlCode`
========================================================

* Author(s): Dan Halbert
"""


class TelephonyControlCode:
    """USB HID Telephony Control Device constants.

    This list includes a few common telephony control codes from
    https://www.usb.org/sites/default/files/hut1_21_0.pdf#page=118.
    """

    # pylint: disable-msg=too-few-public-methods

    PHONE_MUTE = 0x2F
    """Phone Mute"""