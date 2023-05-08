from process import Process
from state_container import StateContainer


class TickCounter(Process):
    def __init__(self,
                 parent: StateContainer,
                 pid: int,
                 wait_id: int,
                 wait_event_queue: int,
                 notify_event_queue: int,
                 timing_event: int,
                 q_var: str):
        super().__init__(parent)
        self.pid = pid
        self.wait_id = wait_id
        self.wait_event_queue = wait_event_queue
        self.notify_event_queue = notify_event_queue
        self.timing_event = timing_event
        self.q_var = q_var
        self.atomic_steps = {
            0: [(self.step_0, 1, True, lambda v: True)],
            1: [(self.null_step, 2, False, lambda v: True)],
            2: [(self.step_1, 3, True, lambda v: v[self.q_var] > 0),
                (self.step_2, 0, False, lambda v: True)],
            3: [(self.step_2, 0, False, lambda v: True)]
        }

    def step_0(self) -> None:
        self.parent.set_process_state(self.pid, self.wait_id)
        self.parent.set_event_state(self.wait_id, 1)

    def step_1(self) -> None:
        self.parent.set_process_state(self.pid, self.wait_event_queue)

    def step_2(self) -> None:
        self.parent.set_event_state(self.notify_event_queue, -1)
        self.parent.modify_variable(self.q_var, self.parent.get_variable_valuation(self.q_var) + 1)

    def null_step(self) -> None:
        self.parent.set_event_state(self.timing_event, 1)
