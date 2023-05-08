from random             import randint
from simulator.process  import Process
from simulator.config   import *
from simulator.main     import DELTA, DEBUG


class Sensor (Process):

    def __init__ (self, wait, od, MIN, *args):
        super(Sensor, self).__init__(*args)
        self.value = 256
        self.od_ev = od
        self.min = MIN
        self.wait_ev = wait

    def reset (self):
        self.value = 256
        super(Sensor, self).reset()
            
            
    def run (self):
    
        if self.pc == 0:
            self.setpc(1)
            self.wait(self.wait_ev, 2)
            return
    
        elif self.pc == 1:
            self.value = randint(0,255)
            if (self.value < self.min):
                self.notify(self.od_ev, DELTA)
            self.wait(self.wait_ev, 2)
            return

        else:
            raise Exception("Wrong pc: " + self.pc + " for " + str(self))
        
