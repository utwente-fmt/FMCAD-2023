from typing import Tuple

from comparator import compare
from invariant_checker import InvariantChecker
from scheduler import Scheduler
from simulator import Simulator


# Add invariant to compare it against the automatically generated invariant (ignores program counters + variables)
INVARIANT: str = """
"""


PROC_NAMES = ["absasr_main", "absasr_read", "tickcounter_0", "tickcounter_1", "tickcounter_2", "tickcounter_3"]
PROGRAM_COUNTERS = [2, 8, 4, 4, 4, 4]

# PROC_NAMES = ["prod", "cons"]
# PROGRAM_COUNTERS = [5, 5]

# PROC_NAMES = ["sensor", "controller", "dummy"]
# PROGRAM_COUNTERS = [2, 5, 1]


def test_invariant():
    s = Simulator()
    s.execute()
    s1, s2 = compare(INVARIANT, s.get_full_invariant(PROC_NAMES, ((2, 1),)))
    print(f"The following {len(s1)} states are missing in the invariant:")
    print('\n|| '.join([str(s) for s in s1]).lower().replace("&& ", "&& m.").replace("ready", "m.ready"))
    print()
    print(f"The following {len(s2)} states have not been found through state space exploration:")
    print('\n|| '.join([str(s) for s in s2]).lower())


def get_invariant_with_pc(cond: Tuple[Tuple[int, int]] = ()) -> str:
    s = Simulator()
    if cond:
        s.execute()
        inv = s.get_full_invariant(PROC_NAMES, cond)
    else:
        s.execute(True)
        inv = s.get_scheduler_invariant(PROC_NAMES)
    return inv


def main_generate_invariant():
    inv = get_invariant_with_pc(((0, 0),))
    print(inv)
    print(f"With program counter, there are {0 if not inv else len(inv.split('||'))} states.")


def main_check_invariant():
    inv_check = InvariantChecker({})
    scheduler = Scheduler(inv_check)
    not_preserved = inv_check.find_not_preserved(scheduler.execute_scheduler, INVARIANT)
    print("\n\n".join(map(lambda s: str(s), not_preserved)))
    print(f"\nThere were {len(not_preserved)} states for which the invariant is not preserved!")
    # inv_check.print_all_state_pairs(scheduler.execute_scheduler, INVARIANT)


def main_generate_all_invariants():
    """
    Generates and prints out all sub-invariants at each program counter for each process, and prints out each sub-
    invariants's length.
    """

    lengths = []
    s = Simulator()
    s.execute(True)
    for counters, (i, proc_name) in zip(PROGRAM_COUNTERS, enumerate(PROC_NAMES)):
        for c in range(counters):
            inv = s.get_full_invariant(PROC_NAMES, ((i, c),))
            inv_name = f"reachable_states_{proc_name}_{c}"
            if inv:
                print(f"inline resource {inv_name}() = true\n    ** (   {inv}\n);\n")
            else:
                print(f"inline resource {inv_name}() = false;\n")
            lengths.append(f"Length of {inv_name}: {0 if not inv else len(inv.split('||'))}")

    inv = s.get_scheduler_invariant(PROC_NAMES)
    inv_name = "reachable_abstract_states_invariant"
    print(f"inline resource {inv_name}() = true\n    ** (   {inv}\n);\n")
    lengths.append(f"Length of {inv_name}: {0 if not inv else len(inv.split('||'))}")

    print(f"Total number of states: {s.get_nr_reachable_states()}")
    for l_string in lengths:
        print(l_string)


def main():
    main_generate_all_invariants()
    

if __name__ == "__main__":
    main()
