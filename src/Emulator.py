import threading
import curses

class Environment :
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

    def __init__(self) :
        self.memory = [0x0]*4096
        self.video_memory = [[0b0] * 64 for i in range(32)]
        self.registers = [0x0]*0xf # V1,V2 ~ V9,Va,Vb,~ Vf までの16個。原則16進数をindexとしてアクセスする
        self.pc = 0x200
        self.sp = 0x0 # スタックポインタ 8bit
        self.dt = 0x0
        self.st = 0x0
        self.i = 0x0
        self.stacks = [0x0]*16
        self.font_address = 0x0
        self._load_font(self.font_address)

    def _load_font(self, font_address):
        for i in range(len(Environment._fonts)):
            self.memory[font_address+i] = Environment._fonts[i]

class Emulator :
    def __init__(self, rom):
        self._env = Environment()
        self._load_rom(rom)
        self._instructions = self._init_instructions()
        hz = threading.Thread(target=self._pulse_60hz)
        hz.start()

    def _pulse_60hz(self):
        t = threading.Timer(1/60, self._pulse_60hz)
        t.start()
        if self._env.dt<0 : self._env.dt-=1
        if self._env.st<0 : self._env.st-=1

    def _init_instructions(self):
        def _not_implemented(): 
            raise NotImplementedError()
        instructions = [_not_implemented]*0xffff
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
        for i in range(0xff+1):
            instructions[0x5000+(i<<4)] = self._se_vx_vy
        for i in range(0xfff+1):
            instructions[0x6000+i] = self._ld_vx_byte
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
        return instructions

    def _get_nibbles(self):
        n1 = self._env.memory[self._env.pc-2]
        n2 = (n1 & 0x0f)
        n1 = (n1 & 0xf0) >> 4
        n3 = self._env.memory[self._env.pc-1]
        n4 = (n3 & 0x0f)
        n3 = (n3 & 0xf0) >> 4
        return (n1,n2,n3,n4)
        
    def _call_addr(self): # 2nnn
        raise NotImplementedError()

    def _se_vx_byte(self):  # 3xkk
        raise NotImplementedError()
    
    def _sne_vx_byte(self):  #4 xkk
        raise NotImplementedError()
    
    def _se_vx_vy(self):  # 5xy0
        raise NotImplementedError()

    def _ld_vx_byte(self): # 6xkk
        raise NotImplementedError()

    def _add_vx_byte(self): # 7xkk
        raise NotImplementedError()

    def _calc_vx_vy(self): # 8xy0
        raise NotImplementedError()

    def _sne_vx_vy(self): # 9xy0
        raise NotImplementedError()

    def _ld_i_addr(self): # Annn
        raise NotImplementedError()

    def _jp_v0_addr(self): # Bnnn
        raise NotImplementedError()

    def _rnd_vx_byte(self): # Cxkk
        raise NotImplementedError()

    def _skp_vx(self): # Ex9E
        raise NotImplementedError()

    def _sknp_vx(self): # ExA1
        raise NotImplementedError()

    def _ld_vx_dt(self): # Fx07
        raise NotImplementedError()

    def _ld_vx_k(self): # Fx0A
        raise NotImplementedError()

    def _ld_dt_vx(self): # Fx15
        raise NotImplementedError()

    def _ld_st_vx(self): # Fx18
        raise NotImplementedError()

    def _add_i_vx(self): # Fx1E
        raise NotImplementedError()

    def _ld_b_vx(self): # Fx33
        raise NotImplementedError()

    def _ld_refI_vx(self): # Fx55
        raise NotImplementedError()

    def _ld_vx_refI(self): # Fx65
        raise NotImplementedError()

    def _cls(self): #00E0
        self.env.video_memory = [[0] * 64 for i in range(32)]

    def _ret(self): #00EE
        self.env.pc = self.env.stacks[self.env.sp]
        self.env.sp -= 1
    
    def _ld_f_vx(self): #Fx29
        (_,x,_,_) = self._get_nibbles()
        self._env.i = self._env.font_address+(self._env.registers[x]*5)

    def _drw_vx_vy_nibble(self): #Dxyn
        (_,x,y,n) = self._get_nibbles()
        sprite = []
        for i in range(n):
            sprite.append(self._env.memory[self._env.i+i])
        for i in range(len(sprite)):
            byte = sprite[i]
            bitarr = Emulator._byte_to_bitarr(byte)
            sprite[i] = bitarr
        for yy in range(len(sprite)):
            for xx in range(len(sprite[yy])):
                self._env.video_memory[y+yy][x+xx] ^= sprite[yy][xx]

    def _byte_to_bitarr(byte):
        bitarr = []
        for i in reversed(range(8)):
            bitmask = 0b1<<i
            bitarr.append((byte&bitmask)>>i)
        return bitarr

    def _join_nibbles(*nibbles):
        ret = 0x0
        for i in range(len(nibbles)):
            tmp = nibbles[i] << ((len(nibbles)-i-1)*4) # 普通にi*4って書くとリトルエンディアンとして読み込んじゃう
            ret |= tmp
        return ret

    def _jp_addr(self): #1nnn
        (_,n1,n2,n3) = self._get_nibbles()
        nnn = self._join_nibbles(n1,n2,n3)
        self._env.pc = nnn

    def _load_rom(self,rom):
        f = open(rom, mode="rb").read()
        for i,byte in enumerate(f):
            self._env.memory[i+0x200] = byte

    def run(self):
        curses.wrapper(self._run)
    def _run(self, screen):
        while True: #TODO: デバッグ用に1tickずつ実行できるように
            n = self.tick()
            self._update_screen(screen)
    
    def _update_screen(self, screen):
        screen.clear()
        for y in range(len(self._env.video_memory)):
            row = ""
            for x in range(len(self._env.video_memory[y])):
                if x == 0 :
                    row += "   "
                else :
                    row += "■ "
            screen.addstr(y,0,row)
        screen.refresh()
    
    def tick(self):
        op = self._get_op()
        if op == 0:
            return -1
        self._exec(op)

    def _get_op(self):
        op = (self._env.memory[self._env.pc] << 8)
        op += self._env.memory[self._env.pc+1]
        self._env.pc += 2
        return op

    def _exec(self,op):
        self._instructions[op]()


