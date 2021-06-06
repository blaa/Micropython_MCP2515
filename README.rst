Introduction
============

A pure micropython library for the MCP2515 CAN bus controller - migrated from
the Adafruit CircuitPython library available here:
https://github.com/adafruit/Adafruit_CircuitPython_MCP2515

Dependencies
=============
This driver depends on:

* Micropython (SPI device and Pin), enough ROM.

Basic functionality tested on ESP32 and STM32F411CE (WeAct) on Micropython 1.15.

Usage Example
=============

.. code-block:: python3

    from machine import SPI, Pin
    import mcp2515

    spi_bus = SPI(1)
    cs_pin = Pin("A4", Pin.OUT)
    can = mcp2515.MCP2515(spi_bus, cs_pin, loopback=False, silent=False)

    message = Message(id=0xFFAA, data=b"hello", extended=True)
    can.send(message)

    print("1 bufs", can.state, can._tx_buffers_in_use)
    print("  tx errors", can.transmit_error_count, "rx_errors", can.receive_error_count)


Documentation
=============

This might not be relevant to micropython:

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
