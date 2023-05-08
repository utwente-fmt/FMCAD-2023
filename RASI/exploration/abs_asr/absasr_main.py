from process import Process
from state_container import StateContainer


class ABSASRMain(Process):
    def __init__(self, parent: StateContainer, pid: int, wait_event: int):
        super().__init__(parent)
        self.pid = pid
        self.wait_event = wait_event
        self.atomic_steps = {
            0: [(self.step_0, 1, True, lambda v: True)],
            1: [(self.null_step, 0, False, lambda v: True)]
        }

    def step_0(self) -> None:
        self.parent.set_process_state(self.pid, self.wait_event)
        self.parent.set_event_state(self.wait_event, 1)

    def null_step(self) -> None:
        pass
