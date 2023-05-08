from random import randint
from simulator.process import Process
from simulator.config import *


class Bad (Process):

    def __init__ (self, wait, sensor, *args):
        super(Bad, self).__init__(*args)
        self.waitev = wait
        self.s = sensor
            
    def run (self):
        
        if self.pc == 0:
            self.s.value = randint(0,255)
            self.wait(self.waitev, 1)
            return
        else:
            raise Exception("Wrong pc: " + self.pc + " for " + str(self))
        

