from simulator.process  import Process
from simulator.main     import DELTA, DEBUG


class TickCounter (Process):
    
    def __init__ (self, fifo, waitev, *args):
        self.fifo = fifo
        self.wait_ev = waitev
        super(TickCounter, self).__init__(*args)
        self.change_state(f"|{self.fifo.name}.buffer|", 0)

    def reset(self):
        super(TickCounter,self).reset()
        self.change_state(f"|{self.fifo.name}.buffer|", 0)

    def run (self):
        speed = 0
        
        while True:
        
            if self.pc == 0:
                self.setpc(1)
                self.wait(self.wait_ev, 1)
                return
        
            elif self.pc == 1 or self.pc == 3:
                
                if self.pc == 1:
                    self.setpc(2)
                
                    speed = 0 # ------------------------------- TODO
                    
                    self.save_state_at_pc()
                
                if (self.fifo.is_full()):
                    assert False
                    self.setpc(3)
                    self.wait(self.fifo.not_full_ev)
                    return
            
                # self.save_state('pre_tc0_fifo_write')
                self.fifo.fifo_write(speed)
                self.notify(self.fifo.not_empty_ev, DELTA)
                self.change_state(f"|{self.fifo.name}.buffer|", 1)
                # self.save_state('pos_tc0_fifo_write')
                
                self.setpc(0)
                self.save_state_at_pc()
            
            else:
                raise Exception("Wrong pc: " + self.pc + " for " + str(self))


