"""
This script runs when the board does a hard reset.

This lets you set certain details of the board like:
* Do we showup as USB drive
* Can we connect via serial USB?
* What name do we show up as?
"""
# pyright: reportMissingImports=false
# pylint: disable=import-error

import usb_cdc # type: ignore

usb_cdc.enable(console=True, data=True)
