from process import Process
from state_container import StateContainer


class ABSASRRead(Process):
    def __init__(self,
                 parent: StateContainer,
                 pid: int,
                 wait_event_queue_0: int,
                 notify_event_queue_0: int,
                 timing_event_0: int,
                 queue_0_var: str,
                 wait_event_queue_1: int,
                 notify_event_queue_1: int,
                 timing_event_1: int,
                 queue_1_var: str,
                 wait_event_queue_2: int,
                 notify_event_queue_2: int,
                 timing_event_2: int,
                 queue_2_var: str,
                 wait_event_queue_3: int,
                 notify_event_queue_3: int,
                 timing_event_3: int,
                 queue_3_var: str):
        super().__init__(parent)
        self.pid = pid
        self.wait_event_queue_0 = wait_event_queue_0
        self.notify_event_queue_0 = notify_event_queue_0
        self.timing_event_0 = timing_event_0
        self.queue_0_var = queue_0_var
        self.wait_event_queue_1 = wait_event_queue_1
        self.notify_event_queue_1 = notify_event_queue_1
        self.timing_event_1 = timing_event_1
        self.queue_1_var = queue_1_var
        self.wait_event_queue_2 = wait_event_queue_2
        self.notify_event_queue_2 = notify_event_queue_2
        self.timing_event_2 = timing_event_2
        self.queue_2_var = queue_2_var
        self.wait_event_queue_3 = wait_event_queue_3
        self.notify_event_queue_3 = notify_event_queue_3
        self.timing_event_3 = timing_event_3
        self.queue_3_var = queue_3_var
        self.atomic_steps = {
            0: [(self.step_0, 1, True, lambda v: v[self.queue_0_var] == 0),
                (self.step_1, 2, False, lambda v: v[self.queue_0_var] > 0)],
            1: [(self.step_1, 2, False, lambda v: True)],
            2: [(self.step_2, 3, True, lambda v: v[self.queue_1_var] == 0),
                (self.step_3, 4, False, lambda v: v[self.queue_1_var] > 0)],
            3: [(self.step_3, 4, False, lambda v: True)],
            4: [(self.step_4, 5, True, lambda v: v[self.queue_2_var] == 0),
                (self.step_5, 6, False, lambda v: v[self.queue_2_var] > 0)],
            5: [(self.step_5, 6, False, lambda v: True)],
            6: [(self.step_6, 7, True, lambda v: v[self.queue_3_var] == 0),
                (self.step_7, 0, False, lambda v: v[self.queue_3_var] > 0)],
            7: [(self.step_7, 0, False, lambda v: True)]
        }

    def step_0(self) -> None:
        self.parent.set_process_state(self.pid, self.wait_event_queue_0)

    def step_1(self) -> None:
        self.parent.set_event_state(self.notify_event_queue_0, -1)
        self.parent.modify_variable(self.queue_0_var, self.parent.get_variable_valuation(self.queue_0_var) - 1)
        self.parent.set_event_state(self.timing_event_0, -3)

    def step_2(self) -> None:
        self.parent.set_process_state(self.pid, self.wait_event_queue_1)

    def step_3(self) -> None:
        self.parent.set_event_state(self.notify_event_queue_1, -1)
        self.parent.modify_variable(self.queue_1_var, self.parent.get_variable_valuation(self.queue_1_var) - 1)
        self.parent.set_event_state(self.timing_event_1, -3)

    def step_4(self) -> None:
        self.parent.set_process_state(self.pid, self.wait_event_queue_2)

    def step_5(self) -> None:
        self.parent.set_event_state(self.notify_event_queue_2, -1)
        self.parent.modify_variable(self.queue_2_var, self.parent.get_variable_valuation(self.queue_2_var) - 1)
        self.parent.set_event_state(self.timing_event_2, -3)

    def step_6(self) -> None:
        self.parent.set_process_state(self.pid, self.wait_event_queue_3)

    def step_7(self) -> None:
        self.parent.set_event_state(self.notify_event_queue_3, -1)
        self.parent.modify_variable(self.queue_3_var, self.parent.get_variable_valuation(self.queue_3_var) - 1)
        self.parent.set_event_state(self.timing_event_3, -3)

    def null_step(self) -> None:
        pass
