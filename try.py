#!/usr/bin/env python3

import pyax25

x = pyax25.AX25("ve3yca", '192.168.85.3', 10093, 4)
x.addRelay('VE3LSR')
# x.setDst("ALSRWX")

# Usefull Groups:
# LOCAL: Local news
# WXBLN: Weather Bulletin
# AMBER: Amber Alerts

x.sendBulletin("Test Bulletin")
# x.sendMessage("Test Message")
