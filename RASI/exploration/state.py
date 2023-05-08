from dataclasses import dataclass
from typing import List


@dataclass(eq=True)
class State:
    process_state: List[int]
    event_state: List[int]

    def __str__(self) -> str:
        return "(   " \
               + " && ".join([f"process_state[{i}] == {v}" for i, v in enumerate(self.process_state)]) \
               + "\n" \
               + "    && " \
               + " && ".join([f"event_state[{i}] == {v}" for i, v, in enumerate(self.event_state)]) \
               + ")"
