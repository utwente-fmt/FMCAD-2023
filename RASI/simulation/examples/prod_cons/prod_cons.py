from simulator.main import Main
from .producer import Producer
from .consumer import Consumer
from .fifo import Fifo

FIFOSIZE = 3

class ProdCons (Main) :

    def simulate(self):

        m = Main()
        
        # register events
        
        READEVENT   = 0
        WRITEEVENT  = 1
        PRODWAIT    = 2
        CONSWAIT    = 3

        m.register_event(READEVENT, "read_event") 
        m.register_event(WRITEEVENT, "write_event")
        m.register_event(PRODWAIT, "producer_wait")  
        m.register_event(CONSWAIT, "consumer_wait")  
        
        # add extra variables
        
        # build non processes
        
        fifo = Fifo(FIFOSIZE)        
        
        # register process
        
        producer = Producer(PRODWAIT, READEVENT, WRITEEVENT, fifo, -1, "prod",
            m.wait,m.notify,m.set_pc,m.change_state,m.save_state,m.check_state)
        pid = m.register_process(producer)
        producer.set_pid(pid)
        
        consumer = Consumer(CONSWAIT, READEVENT, WRITEEVENT, fifo, -1, "cons",
            m.wait,m.notify,m.set_pc,m.change_state,m.save_state,m.check_state)
        pid = m.register_process(consumer)
        consumer.set_pid(pid)

        m.simulate()

if __name__ == "__main__":
    pc = ProdCons()
    pc.simulate()
