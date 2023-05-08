from simulator.main import Main
from .tickcounter import TickCounter
from .abs_main import AbsMain
from .abs_read import AbsRead
from .fifo import Fifo

class AbsAsr():

    def simulate(self):

        m = Main()

        # register events
        
        MAINWAIT    = 0
        TC0WAIT     = 1
        TC1WAIT     = 2
        TC2WAIT     = 3
        TC3WAIT     = 4
        FIFO0READ   = 5
        FIFO0WRITE  = 6
        FIFO1READ   = 7
        FIFO1WRITE  = 8
        FIFO2READ   = 9
        FIFO2WRITE  = 10
        FIFO3READ   = 11
        FIFO3WRITE  = 12
        # PROP0EVENT  = 13
        
        m.register_event(MAINWAIT, "absasr_main.wait")
        m.register_event(TC0WAIT, "tickcounter_0.wait")
        m.register_event(TC1WAIT, "tickcounter_1.wait")
        m.register_event(TC2WAIT, "tickcounter_2.wait")
        m.register_event(TC3WAIT, "tickcounter_3.wait")
        m.register_event(FIFO0READ, "fifo_0.read_event")
        m.register_event(FIFO0WRITE, "fifo_0.write_event")
        m.register_event(FIFO1READ, "fifo_1.read_event")
        m.register_event(FIFO1WRITE, "fifo_1.write_event")
        m.register_event(FIFO2READ, "fifo_2.read_event")
        m.register_event(FIFO2WRITE, "fifo_2.write_event")
        m.register_event(FIFO3READ, "fifo_3.read_event")
        m.register_event(FIFO3WRITE, "fifo_3.write_event")
        # m.register_event(PROP0EVENT, "prop0_event")

        # add extra variables
        
        m.register_var("|fifo_0.buffer|", 0)
        m.register_var("|fifo_1.buffer|", 0)
        m.register_var("|fifo_2.buffer|", 0)
        m.register_var("|fifo_3.buffer|", 0)

        # build fifos

        f0 = Fifo("fifo_0", 1, FIFO0READ, FIFO0WRITE)
        f1 = Fifo("fifo_1", 1, FIFO1READ, FIFO1WRITE)
        f2 = Fifo("fifo_2", 1, FIFO2READ, FIFO2WRITE)
        f3 = Fifo("fifo_3", 1, FIFO3READ, FIFO3WRITE)

        # register processes
        
        absmain = AbsMain(f0,f1,f2,f3,-1,"absasr_main",m.wait,m.notify,m.set_pc,m.change_state,m.save_state,m.check_state)
        pid = m.register_process(absmain)
        absmain.set_pid(pid)
        
        read = AbsRead(absmain,-1,"absasr_read",m.wait,m.notify,m.set_pc,m.change_state,m.save_state)
        pid = m.register_process(read)
        read.set_pid(pid)
        
        tc0 = TickCounter(f0,TC0WAIT,-1,"tickcounter_0",m.wait,m.notify,m.set_pc,m.change_state,m.save_state)
        pid = m.register_process(tc0)
        tc0.set_pid(pid)
        
        tc1 = TickCounter(f1,TC1WAIT,-1,"tickcounter_1",m.wait,m.notify,m.set_pc,m.change_state,m.save_state)
        pid = m.register_process(tc1)
        tc1.set_pid(pid)
        
        tc2 = TickCounter(f2,TC2WAIT,-1,"tickcounter_2",m.wait,m.notify,m.set_pc,m.change_state,m.save_state)
        pid = m.register_process(tc2)
        tc2.set_pid(pid)
        
        tc3 = TickCounter(f3,TC3WAIT,-1,"tickcounter_3",m.wait,m.notify,m.set_pc,m.change_state,m.save_state)
        pid = m.register_process(tc3)
        tc3.set_pid(pid)

        # run simulation
                    
        m.simulate()


if __name__ == "__main__":
    abs = AbsAsr()
    abs.simulate()
