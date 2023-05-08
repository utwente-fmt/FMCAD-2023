from process import Process
from state_container import StateContainer


class Dummy(Process):

    def __init__(self, parent: StateContainer, pid: int):
        super().__init__(parent)
        self.pid = pid
        self.atomic_steps = {
            0: [(self.step_0, 0, True, lambda v: True)]
        }

    def step_0(self) -> None:
        self.parent.set_process_state(self.pid, self.pid)
        self.parent.set_event_state(self.pid, 1)
