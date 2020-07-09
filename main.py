import sys
from Emulator import Emulator

if __name__ == '__main__':
    args = sys.argv
    rom = args[1]
    emu = Emulator(rom)
    emu.run()