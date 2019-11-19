# File: packet.py

"""
This module defines Python structures for the UDP and TCP packets.
"""

def checksum16(data):
    total = 0
    for i in range(0, len(data), 2):
        halfWord = data[i] << 8 | data[i+1]
        total += int(halfWord)
        while total > 2**16:
            total = (total % 65536) + 1
    return total

class UDPPacket:
    """
    This class defines a UDP packet.  Clients refer directly to the
    fields in the structure, which are any of the following:
        src       The source port
        dst       The destination port
        length    The length of the entire segment in bytes
        checksum  The bitwise complement of the 16-bit checksum
        data      The Python bytes object representing the data
    """

# Constants

    UDP_HEADER_LENGTH = 8

# Constructor

    def __init__(self, src=0, dst=0, checksum=0, data=bytes()):
        """
        Creates a UDPPacket from the specified attributes, which are
        typically supplied using keyword parameters.  The data attached
        to the UDP packet can be specified either as a string or a bytes
        object; string data is encoded into bytes using UTF-8 encoding.
        """
        self.src = src
        self.dst = dst
        self.checksum = checksum
        if isinstance(data, str):
            self.data = data.encode("UTF-8")
        else:
            self.data = data
        self.length = UDPPacket.UDP_HEADER_LENGTH + len(data)

# Methods

    def __str__(self):
        """Converts a UDP packet to its string representation."""
        args = ""
        if self.src != 0:
            args += "src=" + str(self.src)
        if self.dst != 0:
            if len(args) > 0: args += ", "
            args += "dst=" + str(self.dst)
        if self.checksum != 0:
            if len(args) > 0: args += ", "
            args += "checksum=0x" + hex(self.checksum)[2:].upper()
        if self.data != None and len(self.data) != 0:
            if len(args) > 0: args += ", "
            args += "data=\"" + self.data.decode("UTF-8") + "\""
        return "UDPPacket(" + args + ")"

    def toBytes(self):
        """Converts a UDPPacket into a Python bytes object."""
        array = bytearray()
        appendHalfWord(array, self.src)
        appendHalfWord(array, self.dst)
        appendHalfWord(array, self.length)
        appendHalfWord(array, self.checksum)
        array.extend(self.data)
        return bytes(array)

class TCPPacket:
    """
    This class defines a TCP packet.  Clients refer directly to the
    fields in the structure, which are any of the following:
        src       The source port
        dst       The destination port
        seq       The sequence number (the first byte index in this packet)
        ack       The acknowledgment number (the next byte index expected)
        hlen      The header length in 32-bit words
        URG       True if this packet contains urgent data
        ACK       True if this packet contains a valid acknowledgment
        PSH       True if the data should be pushed to the application
        RST       True if the receiver should reset the connection
        SYN       True if this packet requests a new connection
        FIN       True if this packet requests closing the connection
        window    The size of the receive window
        checksum  The bitwise complement of the 16-bit checksum
        urgent    The urgent-data field
        options   The bytes object representing the options
        data      The bytes object representing the packet contents
    """

# Constants

    TCP_HEADER_WORDS = 5

# Constructor

    def __init__(self, src=0, dst=0, seq=0, ack=0, URG=False, ACK=False,
                 PSH=False, RST=False, SYN=False, FIN=False, window=0,
                 checksum=0, urgent=0, options=bytes(), data=bytes()):
        """
        Creates a TCPPacket from the specified attributes, which are
        typically supplied using keyword parameters.  The data attached
        to the TCP packet can be specified either as a string or a bytes
        object; string data is encoded into bytes using UTF-8 encoding.
        """
        self.src = src
        self.dst = dst
        self.seq = seq
        self.ack = ack
        self.URG = bool(URG)
        self.ACK = bool(ACK)
        self.PSH = bool(PSH)
        self.RST = bool(RST)
        self.SYN = bool(SYN)
        self.FIN = bool(FIN)
        self.window = window
        self.checksum = checksum
        self.urgent = urgent
        self.options = options
        self.hlen = TCPPacket.TCP_HEADER_WORDS + (len(options) + 3) // 4
        if isinstance(data, str):
            self.data = data.encode("UTF-8")
        else:
            self.data = data

# Methods

    def __str__(self):
        """Converts a TCP packet to its string representation."""
        flags = ""
        if self.URG:
            flags += "URG"
        if self.ACK:
            if len(flags) > 0: flags += "+"
            flags += "ACK"
        if self.PSH:
            if len(flags) > 0: flags += "+"
            flags += "PSH"
        if self.RST:
            if len(flags) > 0: flags += "+"
            flags += "RST"
        if self.SYN:
            if len(flags) > 0: flags += "+"
            flags += "SYN"
        if self.FIN:
            if len(flags) > 0: flags += "+"
            flags += "FIN"
        args = ""
        if self.src != 0:
            args += "src=" + str(self.src)
        if self.dst != 0:
            if len(args) > 0: args += ", "
            args += "dst=" + str(self.dst)
        if self.seq != 0:
            if len(args) > 0: args += ", "
            args += "seq=" + str(self.seq)
        if self.ack != 0:
            if len(args) > 0: args += ", "
            args += "ack=" + str(self.ack)
        if self.hlen != TCPPacket.TCP_HEADER_WORDS:
            if len(args) > 0: args += ", "
            args += "hlen=" + str(self.hlen)
        if flags != "":
            if len(args) > 0: args += ", "
            args += "flags=" + flags            
        if self.window != 0:
            if len(args) > 0: args += ", "
            args += "window=" + str(self.window)
        if self.checksum != 0:
            if len(args) > 0: args += ", "
            args += "checksum=0x" + hex(self.checksum)[2:].upper()
        if self.urgent != 0:
            if len(args) > 0: args += ", "
            args += "urgent=" + str(self.urgent)
        if len(self.options) != 0:
            if len(args) > 0: args += ", "
            args += "options=" + str(self.options)
        if self.data != None and len(self.data) != 0:
            if len(args) > 0: args += ", "
            args += "data=\"" + self.data.decode("UTF-8") + "\""
        return "TCPPacket(" + args + ")"

    def toBytes(self):
        """Converts a TCPPacket into a Python bytes object."""
        array = bytearray()
        appendHalfWord(array, self.src)
        appendHalfWord(array, self.dst)
        appendWord(array, self.seq)
        appendWord(array, self.ack)
        hw = self.hlen << 12
        if self.URG: hw |= 0x20
        if self.ACK: hw |= 0x10
        if self.PSH: hw |= 0x08
        if self.RST: hw |= 0x04
        if self.SYN: hw |= 0x02
        if self.FIN: hw |= 0x01
        appendHalfWord(array, hw)
        appendHalfWord(array, self.window)
        appendHalfWord(array, self.checksum)
        appendHalfWord(array, self.urgent)
        array.extend(self.options)
        if len(self.options) % 4 != 0:
            array.extend(bytearray(4 - len(self.options) % 4))
        array.extend(self.data)
        return bytes(array)

# Functions used in both packet types

def appendByte(array, b):
    """Appends the single byte b to array."""
    array.append(b & 0xFF)

def appendHalfWord(array, hw):
    """Appends the 16-bit halfword hw to array."""
    appendByte(array, hw >> 8)
    appendByte(array, hw)

def appendWord(array, w):
    """Appends the 32-bit word w to array."""
    appendByte(array, w >> 24)
    appendByte(array, w >> 16)
    appendByte(array, w >> 8)
    appendByte(array, w)

