import random
from simulator.process import Process
from simulator.main import DELTA

class Producer(Process):
    
    def __init__(self, wait, read, write, fifo, *args):
        
        super(Producer,self).__init__(*args)
        
        self.wait_ev = wait
        self.r_ev  = read
        self.w_ev = write
        self.fifo = fifo
        
    def reset(self):
        super(Producer,self).reset()
        self.fifo.reset()
        
    def run (self):
        c = 0
        
        if self.pc == 0:
            
            self.setpc(1)
            self.wait(self.wait_ev, 100)
            return

        if self.pc == 1:
            self.setpc(2)
            c = 7
            self.save_state_at_pc()
        
        if self.pc == 2 or self.pc == 3:

            # while self.fifo.n == len(self.fifo.buffer):
            while random.choice([True, False]):
                        
                self.setpc(3)
                self.wait(self.r_ev)
                return
        
            self.setpc(4)
            
            self.fifo.buffer[self.fifo.w_pos] = c;
            self.fifo.w_pos = (self.fifo.w_pos + 1) % len(self.fifo.buffer)
            self.fifo.n = self.fifo.n + 1;
            
            self.notify(self.w_ev, DELTA)
        
            self.setpc(0)
            self.save_state_at_pc()
            return
            
