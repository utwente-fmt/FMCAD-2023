from process import Process
from state_container import StateContainer


class Sensor(Process):

    def __init__(self, parent: StateContainer, pid: int, od: int):
        super().__init__(parent)
        self.pid = pid
        self.od = od
        self.atomic_steps = {
            0: [(self.step_0, 1, True, lambda v: True)],
            1: [(self.step_1, 1, True, lambda v: True),
                (self.step_0, 1, True, lambda v: True)]
        }

    def step_0(self) -> None:
        self.parent.set_process_state(self.pid, self.pid)
        self.parent.set_event_state(self.pid, 2)

    def step_1(self) -> None:
        self.parent.set_event_state(self.od, -1)
        self.step_0()
