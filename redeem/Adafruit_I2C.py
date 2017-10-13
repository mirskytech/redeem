#!/usr/bin/python
# NOTE!! This code is from the Adafruit Learning System articles on the Raspberry Pi (http://learn.adafruit.com/) 
# The original version of the code can be found in the Adafruit Raspberry Pi Python Library on Github at  https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code

# ===========================================================================
# Adafruit_I2C Base Class
# ===========================================================================

import logging


class Adafruit_I2C:
    def __init__(self, address, busnum=3, debug=False):
        try:
            import smbus
            self.bus = smbus.SMBus(busnum)
        except ImportError:
            self.bus = None

        self.address = address
        self.debug = debug

    def reverseByteOrder(self, data):
        "Reverses the byte order of an int (16-bit) or long (32-bit) value"
        # Courtesy Vishal Sapre
        dstr = hex(data)[2:].replace('L', '')
        byteCount = len(dstr[::2])
        val = 0
        for i, n in enumerate(range(byteCount)):
            d = data & 0xFF
            val |= (d << (8 * (byteCount - i - 1)))
            data >>= 8
        return val

    def write8(self, reg, value):
        "Writes an 8-bit value to the specified register/address"

        if self.bus is None:
            return -1

        try:
            self.bus.write_byte_data(self.address, reg, value)
            logging.debug("I2C: Wrote 0x%02X to register 0x%02X" % (value, reg))
        except IOError as err:
            logging.error("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def writeList(self, reg, list):
        "Writes an array of bytes using I2C format"

        if self.bus is None:
            return -1

        try:
            logging.debug("I2C: Writing list to register 0x%02X:" % reg)
            logging.debug(list)
            self.bus.write_i2c_block_data(self.address, reg, list)
        except IOError as err:
            logging.error("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def readList(self, reg, length):
        "Read a list of bytes from the I2C device"

        if self.bus is None:
            return -1

        results = []
        try:
            results = self.bus.read_i2c_block_data(self.address, reg, length)
            logging.debug("I2C: Device 0x%02X returned the following from reg 0x%02X" % (self.address, reg))
            logging.debug(results)
            return results
        except IOError as err:
            logging.error("Error accessing 09x%02X: Check your I2C address" % self.address)
            return -1

    def readU8(self, reg):
        """Read an unsigned byte from the I2C device"""

        if self.bus is None:
            return -1

        try:
            result = self.bus.read_byte_data(self.address, reg)
            logging.debug("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
            return result
        except IOError as err:
            logging.error("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def readS8(self, reg):
        "Reads a signed byte from the I2C device"

        if self.bus is None:
            return -1

        try:
            result = self.bus.read_byte_data(self.address, reg)
            logging.debug("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
            if (result > 127):
                return result - 256
            else:
                return result
        except IOError as err:
            logging.error("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def readU16(self, reg):
        "Reads an unsigned 16-bit value from the I2C device"

        if self.bus is None:
            return -1

        try:
            hibyte = self.bus.read_byte_data(self.address, reg)
            result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg + 1)

            logging.debug("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
            return result
        except IOError as err:
            logging.error("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def readS16(self, reg):
        "Reads a signed 16-bit value from the I2C device"

        if self.bus is None:
            return -1

        try:
            hibyte = self.bus.read_byte_data(self.address, reg)
            if (hibyte > 127):
                hibyte -= 256
            result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg + 1)
            logging.debug("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
            return result
        except IOError as err:
            logging.error("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1
