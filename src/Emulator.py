import threading
import curses

class Emulator :
    _fonts =    [0xF0,0x90,0x90,0x90,0xF0,
                 0x20,0x60,0x20,0x20,0x70,
                 0xF0,0x10,0xf0,0x80,0xf0,
                 0xf0,0x10,0xf0,0x10,0xf0,
                 0x90,0x90,0xf0,0xf0,0x10,
                 0xf0,0x80,0xf0,0x10,0xf0,
                 0xf0,0x80,0xf0,0x90,0xf0,
                 0xf0,0x10,0x20,0x40,0x40,
                 0xf0,0x90,0xf0,0x90,0xf0,
                 0xf0,0x90,0xf0,0x10,0xf0,
                 0xf0,0x90,0xf0,0x90,0x90,
                 0xe0,0x90,0xe0,0x90,0xe0,
                 0xf0,0x80,0x80,0x80,0xf0,
                 0xe0,0x90,0x90,0x90,0xe0,
                 0xf0,0x80,0xf0,0x80,0xf0,
                 0xf0,0x80,0xf0,0x80,0x80]

    def __init__(self, rom):
        self._load_rom(rom)
        self._memory = [0x0]*4096
        self._registers = [0x0]*0xf # V1,V2 ~ V9,Va,Vb,~ Vf までの16個。原則16進数をindexとしてアクセスする
        self._pc = 0x0
        self._sp = 0x0 # スタックポインタ 8bit
        self._dt = 0x0
        self._st = 0x0
        self._i = 0x0
        self._stacks = [0x0]*16
        self._font_address = 0x0
        self._load_font(self._font_address)
        hz = threading.Thread(target=self._pulse_60hz)
        hz.start()

    def _pulse_60hz(self):
        t = threading.Timer(1/60, self._pulse_60hz)
        t.start()
        if self._dt<0 : self._dt-=1
        if self._st<0 : self._st-=1

    def _load_font(self, font_address):
        for i in range(len(Emulator._fonts)):
            self._memory[font_address+i] = Emulator._fonts[i]

    def _load_rom(self,rom):
        None

    def run(self):
        curses.wrapper(self._run)
    def _run(self, screen):
        while True:
            self.tick()
            self._update_screen(screen)
    
    def _update_screen(self, screen):
        screen.clear()
        screen.refresh()
    
    def tick(self):
        


