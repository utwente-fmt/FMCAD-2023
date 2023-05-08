class Process :

    def __init__ (self, pid, name="", 
                    wait_callback=None, 
                    notify_callback=None, 
                    set_pc_callback=None,
                    change_state_callback=None,
                    save_state_callback=None,
                    check_state_callback=None) :

        self.pid = pid
        self.pc = 0
        self.name = name if name else str(self.pid)
        self.wait_ = wait_callback
        self.notify = notify_callback
        self.set_pc = set_pc_callback
        self.change_state = change_state_callback
        self.save_state = save_state_callback
        self.check_state = check_state_callback

    def save_state_at_pc(self):
        self.save_state(f'{self.name}_{self.pc}')

    def set_pid (self, pid: int):
        self.pid = pid

    def reset (self):
        self.pc = 0

    def setpc(self,val):
        self.pc = val
        self.set_pc(self.pid, val)

    def wait(self, ev, time=None):
        self.wait_(self.pid,self.pc,ev,time)
        