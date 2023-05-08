import copy
import re
from typing import List, Tuple

from state import State


def compare(inv1: str, inv2: str) -> Tuple[List[State], List[State]]:
    """
    Compares a string state invariant (disjunction over the state space) to a list of states and returns the difference
    both ways.

    :param inv1: A string state space encoding, attributes joined by '&&' and states joined by '||'
    :param inv2: Another invariant to compare against
    :return: A list of states missing in the invariant and a list of excess states in the invariant
    """

    inv1_states = parse(inv1)
    inv2_states = parse(inv2)

    res1: List[State] = []
    for s in inv2_states:
        if s not in inv1_states:
            res1.append(copy.deepcopy(s))

    res2: List[State] = []
    for s in inv1_states:
        if s not in inv2_states:
            res2.append(copy.deepcopy(s))

    return res1, res2


def parse(inv: str) -> List[State]:
    """
    Parses a state space encoding invariant and returns the encoded states.

    :param inv: A string state space encoding, attributes joined by '&&' and states joined by '||'
    :return: A list of all states encoded in the input
    """

    def parse_from_string(name: str) -> int:
        n = name.strip()
        ns = n.split(" ")
        return int(ns[-1])  # Last one is number in array

    res: List[State] = []

    # Filter out comments
    r_inv = re.sub(r"/\*(.|\n)*?\*/", "", inv)
    r_inv = re.sub(r"//.*?\n", "", r_inv)

    # Filter out other supplementary constructs
    r_inv = ' '.join(r_inv.split()).replace("(", "").replace(")", "").replace("m.", "")

    # Split into states
    states = r_inv.split("||")

    # For each state, reconstruct the state from the string representation
    for s in states:
        processes: List[str] = []
        events: List[str] = []

        props = s.split("&&")

        for p in props:
            if "process_state" in p:
                processes.append(p)
            elif "event_state" in p:
                events.append(p)

        res.append(State(list(map(parse_from_string, processes)), list(map(parse_from_string, events))))

    return res
