from simulator.process import Process
from simulator.config import *


class Controller (Process):

    def __init__ (self, wait, od, *args):
        super(Controller, self).__init__(*args)
        self.wait_ev = wait
        self.od_ev = od
        self.flag = False
        
    def reset(self):
        super(Controller,self).reset()

    def run (self):

        if self.pc == 0:
            self.setpc(1)
            self.wait(self.od_ev)
            return
        elif self.pc == 1:
            self.setpc(3)
            self.wait(self.wait_ev, 1)
            return
        elif self.pc == 3:
            self.setpc(1)
            self.flag = True
            self.wait(self.od_ev)
            return
        else:
            raise Exception("Wrong pc: " + self.pc + " for " + str(self))
             
