from simulator.process import Process
from simulator.config import *


class Dummy (Process):

    def __init__ (self, wait, *args):
        super(Dummy, self).__init__(*args)
        self.waitev = wait
            
    def reset(self):
        super(Dummy,self).reset()
        
    def run (self):
        
        if self.pc == 0:
            self.wait(self.waitev, 1)
            return
        else:
            raise Exception("Wrong pc: " + self.pc + " for " + str(self))
        

