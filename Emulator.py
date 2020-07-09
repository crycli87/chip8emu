import threading
import curses

class Emulator :
    def __init__(self, rom):
        self._load_rom(rom)
        self.memory = [0]
        hz = threading.Thread(target=self._pulse_60hz)
        hz.start()

    def _pulse_60hz(self):
        t = threading.Timer(1/60, self._pulse_60hz)
        t.start()

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
        None


