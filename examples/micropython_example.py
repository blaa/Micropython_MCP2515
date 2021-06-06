import mcp2515
from machine import Pin
from machine import SPI
from mcp2515.canio import Message
from time import sleep

def conn(cs, spibus, loopback=False, silent=False):
    spi_bus = SPI(spibus)
    cs_pin = Pin(cs, Pin.OUT)
    can = mcp2515.MCP2515(spi_bus, cs_pin, loopback=loopback, silent=silent)
    return (spi_bus, can)

def test(cs, spibus):
    mb1 = [0xDE, 0xAD, 0xBE, 0xEF]
    mb2 = [0xCA, 0xFE, 0xFA, 0xDE]
    spi_bus, can = conn(cs, spibus, True, True)
    with can.listen(timeout=1.0) as listener:
        message = Message(id=0xFFAA, data=bytes(mb1 + mb2), extended=True)

        can.send(message)
        sleep(0.01)

        message_count = listener.in_waiting()
        print(message_count, "messages available")
        for _i in range(message_count):
            msg = listener.receive()
            print("Message from ", hex(msg.id))
            print("message data:", msg.data)
            message_str = "::".join(["0x{:02X}".format(i) for i in msg.data])
            print(message_str)

    return can

def stat(can):
    for _ in range(2):
        print("1 bufs", can.state, can._tx_buffers_in_use)
        print("  tx errors", can.transmit_error_count, "rx_errors", can.receive_error_count)
        sleep(1)

def tx(cs="A4", spibus=1):
    spi_bus, can = conn(cs, spibus)
    while True:
        print("Send hello FFAA")
        message = Message(id=0xFFAA, data=b"hello", extended=True)
        can.send(message)
        stat(can)

        print("Send bye FFBB")
        message = Message(id=0xFFBB, data=b"bye", extended=True)
        can.send(message)
        stat(can)

def rx(cs="A4", spibus=1):
    spi_bus, can = conn(cs, spibus)
    with can.listen(timeout=1.0) as listener:
        while True:
            message_count = listener.in_waiting()
            print(message_count, "messages available")
            for _i in range(message_count):
                msg = listener.receive()
                print("Message from ", hex(msg.id))
                print("message data:", msg.data)
                message_str = "::".join(["0x{:02X}".format(i) for i in msg.data])
                print(message_str)
            sleep(0.5)
