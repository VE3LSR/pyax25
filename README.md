# pyax25
Python module to send AX25 UI messages over UDP

ax25 = pyax25.AX25(Source CallSign, AX25 IP Address, AX25 UDP Port, Source SSID [Default 0], Use UTC [Default False])

# Add a relay to the AX25 routing
ax25.addRelay(Relay Callsign, Relay SSID [Default 0])

# Send an APRS Bulletin
ax25.sendBulletin(message, group [Default None], line = 0):
- Group must be 5 chars, space padded 

Usefull Groups:
- LOCAL: Local news
- WXBLN: Weather Bulletin
- AMBER: Amber Alerts

# Send an APRS Message

ax25.sendMessage(message, group [Default BOM_WARN])
