#!/usr/bin/env python3

import struct
import crcmod
import socket
import textwrap
import datetime
from bitstring import BitArray

class AX25:
    def __init__(self, src, ip, port, src_ssid=0, use_utc=False):
        self.x25_crc_func = crcmod.predefined.mkCrcFun('x-25')
        self.src = src
        self.ip = ip
        self.port = port
        self.src_ssid = src_ssid
        self.relays = []
        self.dst = "APRS"
        self.dst_ssid = 0
        self.use_utc = use_utc
        self.maxlen = 64

    def setDst(self, dst, dst_ssid=0):
        self.dst = dst
        self.dst_ssid = dst_ssid

    def getDst(self):
        return (self.dst, self.dst_ssid)

    def addRelay(self, relay, ssid=0):
        self.relays.append([relay, ssid])

    def _encode_address(self, address, ssid=0, last=False):
        if ssid > 15:
            raise 
        result = ""
        for letter in address.ljust(6):
            result += chr(ord(letter.upper()) << 1)
        rssid = ssid << 1
        if last:
            rssid = rssid | 0b01100001
        else: 
            rssid = rssid | 0b01100000
        result += chr(rssid)
        return result.encode('Latin-1')

    def getAddress(self, address, ssid=0, last=False):
        return self._encode_address(address, ssid, last)

    def genTime(self):
        if self.use_utc:
            return datetime.datetime.now().strftime("%H%M%Sz")
        else: 
            return datetime.datetime.now().astimezone().strftime("%H%M%S%z")

    def calc_crc(self, packet):
        # Calculate the CRC
        c = self.x25_crc_func(packet)
        crc = BitArray(hex(c))
        crc.byteswap()
        return (crc).bytes

    # Relays is an array of relays
    def buildPacket(self, cf = 0x03, message = ""):
        # Start Building the packet
        relays = self.relays  # TODO: Clean this
        packet = struct.pack("<7s", self.getAddress(self.dst, self.dst_ssid))
        if len(relays) == 0:
            packet += struct.pack("<7s", self.getAddress(self.src, self.src_ssid, True))
        else:
            packet += struct.pack("<7s", self.getAddress(self.src, self.src_ssid))
            for relay in relays[:-1]:
                packet += struct.pack("<7s", self.getAddress(relay[0], relay[1]))
            packet += struct.pack("<7s", self.getAddress(relays[-1][0], relays[-1][1], True))
        packet += struct.pack("<BB{}s".format(len(message)), cf, 0xF0, bytes(message, "ASCII"))
        crc = self.calc_crc(packet)
        self.packet = packet + crc

    def getPacket(self):
        return self.packet

    def send(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(self.packet, (self.ip, self.port))

    # Line should not be used. If it is, consitter it the starting line for line wraps
    def sendBulletin(self, message, group = "     ", line = 0):
        maxlen = 64
        message = self.genTime() + " - " + message
        if len(message) < maxlen:
            message = ":BLN{}{}:{}".format(line, group.upper(), message)
            self.buildPacket(message=message)
            self.send()
        else:
            linenum = line
            for msgline in textwrap.wrap(message,maxlen):
                longmessage = ":BLN{}{}:{}".format(linenum, group.upper(), msgline)
                self.buildPacket(message=longmessage)
                self.send()
                linenum += 1

    def sendMessage(self, message, group = "BOM_WARN"):
        maxlen = 64
        if len(message) < self.maxlen:
            message = ":{:<9}:{}".format(group.upper(), message)
            self.buildPacket(message=message)
            self.send()
        else:
            for msgline in textwrap.wrap(message,self.maxlen):
                longmessage = ":{:<9}:{}".format(group.upper(), msgline)
                self.buildPacket(message=longmessage)
                self.send()
