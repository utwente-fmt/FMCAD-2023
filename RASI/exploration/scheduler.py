from typing import List, Tuple, Callable, Dict

from process import Process
from state_container import StateContainer


class Scheduler(Process):

    def __init__(self, parent: StateContainer):
        super().__init__(parent)

    def get_next_steps(self, pc: int, variables: Dict[str, int]) -> List[Tuple[Callable[[], None], int, bool]]:
        # As the scheduler can only be executed atomically, its next step is a constant
        return [(self.execute_scheduler, 0, True)]

    def execute_scheduler(self) -> None:
        """
        Executes the scheduler. The scheduler does not depend on the program and should not be changed.
        """

        # Immediate wakeup
        for i in range(self.parent.n_proc):
            if self.parent.get_process_state(i) >= 0:
                ind = self.parent.get_process_state(i)
                if self.parent.get_event_state(ind) == 0:
                    self.parent.set_process_state(i, -1)

        # Reset events
        for i in range(self.parent.n_event):
            if self.parent.get_event_state(i) == 0:
                self.parent.set_event_state(i, -2)

        if not any([self.parent.get_process_state(i) == -1 for i in range(self.parent.n_proc)]):

            # Find minimum advance
            timeouts = [self.parent.get_event_state(i)
                        for i in range(self.parent.n_event)
                        if self.parent.get_event_state(i) >= -1]
            min_advance = min(timeouts) if timeouts else 0
            if min_advance == -1:
                min_advance = 0

            # Advance time
            for i in range(self.parent.n_event):
                if self.parent.get_event_state(i) >= 0:
                    self.parent.set_event_state(i, self.parent.get_event_state(i) - min_advance)
                elif self.parent.get_event_state(i) < -1:
                    self.parent.set_event_state(i, -3)

            # Wakeup after wait
            for i in range(self.parent.n_proc):
                if self.parent.get_process_state(i) >= 0:
                    ind = self.parent.get_process_state(i)
                    if self.parent.get_event_state(ind) == 0 or self.parent.get_event_state(ind) == -1:
                        self.parent.set_process_state(i, -1)

            # Reset all triggered events
            for i in range(self.parent.n_event):
                if self.parent.get_event_state(i) == 0 or self.parent.get_event_state(i) == -1:
                    self.parent.set_event_state(i, -2)
