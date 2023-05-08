from simulator.process import Process
from simulator.main import DEBUG, DELTA

class AbsRead (Process):


    def __init__ (self, absasr, *args):

        super(AbsRead, self).__init__(*args)
        
        self.tmp_0 = 0
        self.tmp_1 = 0
        self.tmp_2 = 0
        self.tmp_3 = 0
        
        self.bus_vr = absasr.bus_vr
        self.bus_vl = absasr.bus_vl
        self.bus_hr = absasr.bus_hr
        self.bus_hl = absasr.bus_hl
        
        self.v = absasr.v
        self.a = absasr.a
        
    def reset(self):
        
        self.tmp_0 = 0
        self.tmp_1 = 0
        self.tmp_2 = 0
        self.tmp_3 = 0
        super(AbsRead,self).reset()
                   
    def run(self) -> None:

        while True:

            if self.pc == 0 or self.pc == 1:
    
                if self.bus_vr.is_empty():
                    self.setpc(1)
                    self.wait(self.bus_vr.not_empty_ev)
                    return
                
                self.setpc(2);
            
                # self.save_state('pre_bus_vr_read')
                self.v[0] = self.bus_vr.fifo_read();                
                self.notify(self.bus_vr.not_full_ev, DELTA)
                self.change_state("|fifo_0.buffer|", 0)
                # self.save_state('pos_bus_vr_read')

                self.a[0] = self.v[0] - self.tmp_0;
                self.tmp_0 = self.v[0];

            if self.pc == 2 or self.pc == 3:

                self.save_state_at_pc()

                if self.bus_vl.is_empty():
                    assert False
                    self.setpc(3)

                    self.wait(self.bus_vl.not_empty_ev)
                    return
            
                self.setpc(4);
                # self.save_state('pre_bus_vl_read')
                self.v[1] = self.bus_vl.fifo_read();
                self.notify(self.bus_vl.not_full_ev, DELTA)
                self.change_state("|fifo_1.buffer|", 0)
                # self.save_state('pos_bus_vl_read')
                         
                self.a[1] = self.v[1] - self.tmp_1;
                self.tmp_1 = self.v[1];

            if self.pc == 4 or self.pc == 5:
            
                self.save_state_at_pc()
            
                if self.bus_hr.is_empty():
                    assert False
                    self.setpc(5)
                    self.wait(self.bus_hr.not_empty_ev)
                    return
            
                self.setpc(6);
                
                # self.save_state('pre_bus_hr_read')
                self.v[2] = self.bus_hr.fifo_read();
                self.notify(self.bus_hr.not_full_ev, DELTA)
                self.change_state("|fifo_2.buffer|", 0)
                # self.save_state('pos_bus_hr_read')

                self.a[2] = self.v[2] - self.tmp_2;
                self.tmp_2 = self.v[2];


            if self.pc == 6 or self.pc == 7:

                self.save_state_at_pc()

                if self.bus_hl.is_empty():
                    assert False
                    self.setpc(7)

                    self.wait(self.bus_hl.not_empty_ev)
                    return
            
                self.setpc(0);
                
                # self.save_state('pre_bus_hl_read')
                self.v[3] = self.bus_hl.fifo_read();
                self.notify(self.bus_hl.not_full_ev, DELTA)
                self.change_state("|fifo_3.buffer|", 0)
                # self.save_state('pos_bus_hl_read')

                self.a[3] = self.v[3] - self.tmp_3;
                self.tmp_3 = self.v[3];
            
            self.save_state_at_pc()
