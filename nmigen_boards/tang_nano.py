from nmigen.build import *
from nmigen.vendor.gowin_gw1n import *
from nmigen_boards.resources import *

import os
import subprocess

class TangNanoPlatform(GowinGW1NPlatform):
    default_clk = "clk24"
    device = "GW1N-1"
    package = "QN48"
    voltage = "LV"
    speed = "C6/I5"

    resources   = [
        Resource("clk24", 0, Pins("35", dir="i"),
                 Clock(24e6), Attrs(IO_TYPE="LVCMOS33")),

        RGBLEDResource(0,
            r="18", g="16", b="17", invert=True,
            attrs=Attrs(IO_TYPE="LVCMOS33")),

        # LCD connector (with pin numbers, save for later...)
        Resource("lcd", 0,
            Subsignal("r",    Pins("27 28 29 30 31", dir="o")),
            Subsignal("g",    Pins("32 33 34 38 39 40", dir="o")),
            Subsignal("b",    Pins("41 42 43 44 45", dir="o")),
            Subsignal("vs",   Pins("46", dir="o")),
            Subsignal("hs",   Pins("10", dir="o")),
            Subsignal("den",  Pins("5", dir="o")),
            Subsignal("pclk", Pins("11", dir="o")),
            Attrs(IO_TYPE="LVCMOS33"),
        ),

        *ButtonResources(pins="14 15", invert=True, attrs=Attrs(IO_TYPE="LVCMOS33")),

        # These are the dedicated UART pins, however they are dual function with
        # RECONFIG_N and DONE which make them difficult to use.
        UARTResource(0,
            rx="9", tx="8",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),

        *SPIFlashResources(0,
            cs_n="19", clk="20", copi="22", cipo="23", wp_n="21", hold_n="24",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),
    ]
    connectors = [
    ]

    def toolchain_program(self, products, name):
        openFPGALoader = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}.fs".format(name)) as (bitstream):
            print(subprocess.check_call([
                openFPGALoader, "-m", "-b", "tangnano", bitstream
            ]))

if __name__ == "__main__":
    from .test.blinky import *
    TangNanoPlatform().build(Blinky(), do_program=True)
