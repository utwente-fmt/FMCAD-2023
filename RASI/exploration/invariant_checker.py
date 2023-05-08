import copy
import re
from typing import List, Callable, Dict, Tuple

from state import State
from state_container import StateContainer


def parse(inv: str) -> Tuple[List[State], List[List[int]]]:
    def parse_from_string(name: str) -> int:
        n = name.strip()
        ns = n.split(" ")
        return int(ns[-1])  # Last one is number in array

    resulting_states: List[State] = []
    resulting_pcs: List[List[int]] = []

    # Filter out comments
    r_inv = re.sub(r"/\*(.|\n)*?\*/", "", inv)
    r_inv = re.sub(r"//.*?\n", "", r_inv)

    # Filter out other supplementary constructs
    r_inv = ' '.join(r_inv.split()).replace("(", "").replace(")", "").replace("m.", "")

    # Split into states
    states = r_inv.split("||")

    for s in states:
        processes: List[str] = []
        events: List[str] = []
        pcs: List[str] = []

        props = s.split("&&")

        for p in props:
            if "process_state" in p:
                processes.append(p)
            elif "event_state" in p:
                events.append(p)
            elif ".pc" in p:
                pcs.append(p)

        resulting_states.append(State(list(map(parse_from_string, processes)), list(map(parse_from_string, events))))
        resulting_pcs.append(list(map(parse_from_string, pcs)))

    return resulting_states, resulting_pcs


class InvariantChecker(StateContainer):

    def __init__(self, variables: Dict[str, int]):
        super().__init__()
        self.n_event = 13
        self.n_proc = 6
        self.state = None
        self.variables = variables

    def set_process_state(self, index: int, value: int) -> None:
        self.state.process_state[index] = value

    def get_process_state(self, index: int) -> int:
        return self.state.process_state[index]

    def set_event_state(self, index: int, value: int) -> None:
        self.state.event_state[index] = value

    def get_event_state(self, index: int) -> int:
        return self.state.event_state[index]

    def modify_variable(self, name: str, new_val: int) -> None:
        self.variables[name] = new_val

    def get_variable_valuation(self, name: str) -> int:
        return self.variables[name]

    def find_not_preserved(self, fun: Callable, invariant: str) -> List[State]:
        states, pcs = parse(invariant)
        res: List[State] = []

        complete_states = list(zip(states, pcs))

        print(f"The total number of states in the invariant is {len(complete_states)}")

        for state, pc in complete_states:
            self.state = copy.deepcopy(state)
            fun()
            if (self.state, pc) not in complete_states:
                print(self.state)
                res.append(copy.deepcopy(state))

        return res

    def print_all_state_pairs(self, fun: Callable, invariant: str):
        states, _ = parse(invariant)
        print(len(states))

        for state in states:
            self.state = copy.deepcopy(state)
            print()
            print(f"ensures \old({str(self.state)})")
            fun()
            print(" ==> {};".format(str(self.state)))
            print()

