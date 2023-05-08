from abc import ABC
from typing import List, Callable, Tuple, Dict

from state_container import StateContainer


class Process(ABC):

    def __init__(self, parent: StateContainer):
        self.parent = parent
        self.atomic_steps: Dict[int, List[Tuple[Callable[[], None], int, bool, Callable[[Dict[str, int]], bool]]]] = {}

    def get_next_steps(self, pc: int, variables: Dict[str, int]) -> List[Tuple[Callable[[], None], int, bool]]:
        """
        Returns the transitions possible from a given state of execution.

        :param pc: Program counter to indicate the state of the process
        :param variables: Integer variable valuations in the current state, encoded as a dictionary with variable name
                          as the key
        :return: A list of transitions of the form (function, next_state, release), where function is the effects on the
                 state of the transition, next_state is the program counter after executing the transition and release
                 is a boolean indicating whether the process released the lock for other processes to execute
        """

        return [(f, nxt, rel) for f, nxt, rel, viable in self.atomic_steps[pc] if viable(variables)]
