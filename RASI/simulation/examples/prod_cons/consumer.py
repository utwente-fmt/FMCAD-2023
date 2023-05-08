from simulator.process import Process
from simulator.main import DELTA
import random

class Consumer(Process):
    
    def __init__(self, wait, read, write, fifo, *args):
        
        super(Consumer,self).__init__(*args)
        
        self.wait_ev = wait
        self.r_ev  = read
        self.w_ev = write
        self.fifo = fifo
        
    def reset(self):
        super(Consumer,self).reset()
        self.fifo.reset()
        
    def run(self):
        c = 0
        
        while True:
            
            if self.pc == 0 or self.pc == 1:
            
                # while self.fifo.n == 0:
                while random.choice([True, False]):
                            
                    self.setpc(1)
                    self.wait(self.w_ev)
                    return
            
                self.setpc(2)
                self.save_state_at_pc()
        
                c = self.fifo.buffer[self.fifo.r_pos];
                self.fifo.r_pos = (self.fifo.r_pos + 1) % len(self.fifo.buffer)
                self.fifo.n = self.fifo.n - 1;

                self.notify(self.r_ev, DELTA)
                self.setpc(3)
                self.save_state_at_pc()
        
                self.setpc(4)
                self.wait(self.wait_ev,200)
                return
        
            if self.pc == 4:
                self.setpc(0)
                self.save_state_at_pc()