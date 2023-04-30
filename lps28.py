# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`lps28`
================================================================================

LPS28 pressure sensor drive for CircuitPython


* Author(s): Jose D. Montoya


"""

from micropython import const
from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bits import RWBits

try:
    from busio import I2C
    from typing import Tuple
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_LPS28.git"


_REG_WHOAMI = const(0x0F)
_CTRL_REG1 = const(0x10)

# Data Rate
ONE_SHOT = const(0b0000)
RATE_1_HZ = const(0b0001)
RATE_4_HZ = const(0b0010)
RATE_10_HZ = const(0b0011)
RATE_25_HZ = const(0b0100)
RATE_50_HZ = const(0b0101)
RATE_75_HZ = const(0b0110)
RATE_100_HZ = const(0b0110)
RATE_200_HZ = const(0b1000)
data_rate_values = (
    ONE_SHOT,
    RATE_1_HZ,
    RATE_4_HZ,
    RATE_10_HZ,
    RATE_25_HZ,
    RATE_50_HZ,
    RATE_75_HZ,
    RATE_100_HZ,
    RATE_200_HZ,
)


class LPS28:
    """Driver for the LPS28 Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the LPS28 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x5D`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`LPS28` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        import board
        import lps28

    Once this is done you can define your `board.I2C` object and define your sensor object

    .. code-block:: python

        i2c = board.I2C()  # uses board.SCL and board.SDA
        lps28 = LPS28.lps28(i2c)

    Now you have access to the attributes

    .. code-block:: python

        press = lps28.pressure

    """

    _device_id = ROUnaryStruct(_REG_WHOAMI, "B")

    _data_rate = RWBits(4, _CTRL_REG1, 3)

    def __init__(self, i2c_bus: I2C, address: int = 0x5D) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != 0xB4:
            raise RuntimeError("Failed to find LPS28")

    @property
    def data_rate(self):
        """
        Sensor data_rate

        +-------------------------------+--------------------+
        | Mode                          | Value              |
        +===============================+====================+
        | :py:const:`lps28.ONE_SHOT`    | :py:const:`0b0000` |
        +-------------------------------+--------------------+
        | :py:const:`lps28.RATE_1_HZ`   | :py:const:`0b0001` |
        +-------------------------------+--------------------+
        | :py:const:`lps28.RATE_4_HZ`   | :py:const:`0b0010` |
        +-------------------------------+--------------------+
        | :py:const:`lps28.RATE_10_HZ`  | :py:const:`0b0011` |
        +-------------------------------+--------------------+
        | :py:const:`lps28.RATE_25_HZ`  | :py:const:`0b0100` |
        +-------------------------------+--------------------+
        | :py:const:`lps28.RATE_50_HZ`  | :py:const:`0b0101` |
        +-------------------------------+--------------------+
        | :py:const:`lps28.RATE_75_HZ`  | :py:const:`0b0110` |
        +-------------------------------+--------------------+
        | :py:const:`lps28.RATE_100_HZ` | :py:const:`0b0110` |
        +-------------------------------+--------------------+
        | :py:const:`lps28.RATE_200_HZ` | :py:const:`0b1000` |
        +-------------------------------+--------------------+
        """
        values = (
            "ONE_SHOT",
            "RATE_1_HZ",
            "RATE_4_HZ",
            "RATE_10_HZ",
            "RATE_25_HZ",
            "RATE_50_HZ",
            "RATE_75_HZ",
            "RATE_100_HZ",
            "RATE_200_HZ",
        )
        return values[self._data_rate]

    @data_rate.setter
    def data_rate(self, value: int):
        if value not in data_rate_values:
            raise ValueError("Value must be a valid data_rate setting")
        self._data_rate = value
