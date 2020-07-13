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
        self._instructions = self._init_instructions()
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

    def _init_instructions(self):
        instructions = []
        instructions[0x00E0] = self._cls
        instructions[0x00EE] = self._ret
        for i in range(0xfff+1):
            instructions[0x1000+i] = self._jp_addr
        for i in range(0xfff+1):
            instructions[0x2000+i] = self._call_addr
        for i in range(0xfff+1):
            instructions[0x3000+i] = self._se_vx_byte
        for i in range(0xfff+1):
            instructions[0x4000+i] = self._sne_vx_byte
        for i in range(0xfff+1):
            instructions[0x7000+i] = self._add_vx_byte
        for i in range(0xfff+1):
            instructions[0x8000+i] = self._calc_vx_vy
        for i in range(0xff+1):
            instructions[0x9000+(i<<4)] = self._sne_vx_vy
        for i in range(0xfff+1):
            instructions[0xa000+i] = self._ld_i_addr
        for i in range(0xfff+1):
            instructions[0xb000+i] = self._jp_v0_addr
        for i in range(0xfff+1):
            instructions[0xc000+i] = self._rnd_vx_byte
        for i in range(0xfff+1):
            instructions[0xd000+i] = self._drw_vx_vy_nibble
        for i in range(0xf+1):
            instructions[0xe09e+(i<<8)] = self._skp_vx
        for i in range(0xf+1):
            instructions[0xe0a1+(i<<8)] = self._sknp_vx
        for i in range(0xf+1):
            instructions[0xf007+(i<<8)] = self._ld_vx_dt
        for i in range(0xf+1):
            instructions[0xf00a+(i<<8)] = self._ld_vx_k
        for i in range(0xf+1):
            instructions[0xf015+(i<<8)] = self._ld_dt_vx
        for i in range(0xf+1):
            instructions[0xf018+(i<<8)] = self._ld_st_vx
        for i in range(0xf+1):
            instructions[0xf01e+(i<<8)] = self._add_i_vx
        for i in range(0xf+1):
            instructions[0xf029+(i<<8)] = self._ld_f_vx
        for i in range(0xf+1):
            instructions[0xf033+(i<<8)] = self._ld_b_vx
        for i in range(0xf+1):
            instructions[0xf055+(i<<8)] = self._ld_refI_vx
        for i in range(0xf+1):
            instructions[0xf065+(i<<8)] = self._ld_vx_refI

    def _load_rom(self,rom):
        None

    def run(self):
        curses.wrapper(self._run)
    def _run(self, screen):
        while True: #TODO: デバッグ用に1tickずつ実行できるように
            self.tick()
            self._update_screen(screen)
    
    def _update_screen(self, screen):
        screen.clear()
        screen.refresh()
    
    def tick(self):
        op = self._get_op()



