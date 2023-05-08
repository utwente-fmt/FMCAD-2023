from simulator.process import Process
from simulator.main import DEBUG


class AbsMain (Process):

    def __init__ (self, bus0, bus1, bus2, bus3, *args):
        super(AbsMain, self).__init__(*args)
        
        self.bus_vr = bus0;
        self.bus_vl = bus1;
        self.bus_hr = bus2;
        self.bus_hl = bus3;

        self.s = [0,0,0,0];        
        self.v = [0,0,0,0];
        self.a = [0,0,0,0];

        self.temp_fv = 0;
        self.fv = 0;
        self.fa = 0;

        self.lamb = [0,0,0,0];

        self.p = [0,0,0,0];


    def reset (self):
        self.bus_vr.reset()
        self.bus_vl.reset()
        self.bus_hr.reset()
        self.bus_hl.reset()
        
        super(AbsMain, self).reset()

    def run (self):

        if self.pc == 0:
            
            for i in range(0,4):
                self.s[i] = 1;
                self.v[i] = 0;
                self.a[i] = 0;

        while True:

            if self.pc == 0:

                self.pc = 1
                self.setpc(1)
                self.wait(self.pid, 1)            
                return
            
            elif self.pc == 1:
                
                self.pc = 0
                self.setpc(0)
            
                i = 0;
                if (abs(self.a[1]) < abs(self.a[i])) :
                    i = 1;
                if (abs(self.a[2]) < abs(self.a[i])) :
                    i = 2;
                if (abs(self.a[3]) < abs(self.a[i])) :
                    i = 3;
            
                self.temp_fv = self.v[i]
                self.fa = self.temp_fv - self.fv
            
                # prop 0
                # assert self.check_state("event_state")[13] <= 2;
            
                if (self.fa < 0) :         
                    if (self.fa < m.MINUS_A) :
                        self.fv = self.fv + m.AREF
                    else :
                        self.fv = self.temp_fv
                    # self.state.save(f'pre_abs_abs')
                    _ABS()
                    # self.state.save(f'pos_abs_abs')
            
                elif (self.fa > 0) :        
                    self.fv = self.temp_fv
                    # self.state.save(f'pre_abs_asr')
                    _ASR()
                    # self.state.save(f'pos_abs_asr')
                    
                self.setpc(0)
                self.save_state_at_pc()
        
        else:
            raise Exception("Wrong pc: " + self.pc + " for " + str(self))