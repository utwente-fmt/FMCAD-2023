from process import Process
from state_container import StateContainer


class Consumer(Process):

    def __init__(self, parent: StateContainer, pid: int):
        super().__init__(parent)
        self.pid = pid
        self.atomic_steps = {
            0: [(self.step_0, 1, True, lambda v: True),
                (self.null_step, 2, False, lambda v: True)],
            1: [(self.null_step, 0, False, lambda v: True)],
            2: [(self.step_1, 3, False, lambda v: True)],
            3: [(self.step_2, 4, True, lambda v: True)],
            4: [(self.null_step, 0, False, lambda v: True)]
        }

    def step_0(self) -> None:
        self.parent.set_process_state(self.pid, 1)

    def step_1(self) -> None:
        self.parent.set_event_state(0, -1)

    def step_2(self) -> None:
        self.parent.set_process_state(self.pid, 3)
        self.parent.set_event_state(3, 200)

    def null_step(self) -> None:
        pass
