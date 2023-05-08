import copy
import random
from typing import List, Tuple, Callable, Dict

from process import Process
from scheduler import Scheduler
from state import State
from state_container import StateContainer

#######################################################
#             PRODUCER-CONSUMER EXAMPLE               #
#######################################################
# from producer_consumer.consumer import Consumer
# from producer_consumer.producer import Producer
#######################################################

#######################################################
#             SENSOR-CONTROLLER EXAMPLE               #
#######################################################
# from sensor_controller.sensor import Sensor
# from sensor_controller.controller import Controller
# from sensor_controller.dummy import Dummy
#######################################################

#######################################################
#          ANTI-LOCK BRAKING SYSTEM EXAMPLE           #
#######################################################
from abs_asr.absasr_main import ABSASRMain
from abs_asr.absasr_read import ABSASRRead
from abs_asr.tick_counter import TickCounter
#######################################################


class Simulator(StateContainer):
    """
    Container class for the simulation functionality. Enables the exhaustive exploration of the state space with regard
    to the scheduling variables ``wait_on``, ``ev_timeout``, ``delta_delay`` and ``occurred``.

    To adapt the class to a different model, implement subclasses of ``Process`` for all distinct processes (process
    classes) in your model and adjust the ``n_proc``, ``n_event`` and ``processes`` attributes accordingly.
    """

    def __init__(self):
        super().__init__()
        # Initialise numbers of processes and events
        self.n_proc = 6
        self.n_event = 17

        # Variables that are relevant for the execution order
        self.sys_vars = ["|fifo_0.buffer|", "|fifo_1.buffer|", "|fifo_2.buffer|", "|fifo_3.buffer|"]

        # Initialise relevant processes
        self.processes: List[Process] = [ABSASRMain(self, 0, 0),
                                         ABSASRRead(self, 1,
                                                    6, 5, 13, self.sys_vars[0],
                                                    8, 7, 14, self.sys_vars[1],
                                                    10, 9, 15, self.sys_vars[2],
                                                    12, 11, 16, self.sys_vars[3]),
                                         TickCounter(self, 2, 1, 5, 6, 13, self.sys_vars[0]),
                                         TickCounter(self, 3, 2, 7, 8, 14, self.sys_vars[1]),
                                         TickCounter(self, 4, 3, 9, 10, 15, self.sys_vars[2]),
                                         TickCounter(self, 5, 4, 11, 12, 16, self.sys_vars[3]),
                                         Scheduler(self)]

        # self.processes: List[Process] = [Producer(self, 0), Consumer(self, 1), Scheduler(self)]
        # self.processes: List[Process] = [Sensor(self, 0, 3), Controller(self, 1, 3), Dummy(self, 2), Scheduler(self)]

        # Initialise state and list of visited states
        self.state = State([-1] * self.n_proc,
                           [-3] * self.n_event)

        self.variables: Dict[str, int] = {}
        for sys_var in self.sys_vars:
            self.variables[sys_var] = 0

        # Structure of entry in explored_states: (state, [pc_0, ..., pc_n], {var_1: val, ..., var_k: val})
        self.explored_states: List[Tuple[State, List[int], Dict[str, int]]] = [(copy.deepcopy(self.state),
                                                                                [0] * (self.n_proc + 1),
                                                                                copy.deepcopy(self.variables))]

        self.explored_states_reachable_by: List[List[int]] = [[i for i in range(self.n_proc + 1)]]

        # Set up simulation branches
        # Structure of entry in active_branches: (state, [pc_0, ..., pc_n], next_process, variables)
        self.active_branches: List[Tuple[State, List[int], int, Dict[str, int]]] = [(copy.deepcopy(self.state),
                                                                                     [0] * (self.n_proc + 1),
                                                                                     i,
                                                                                     copy.deepcopy(self.variables))
                                                                                    for i in range(self.n_proc + 1)]

    def get_nr_reachable_states(self) -> int:
        return len(self.explored_states)

    def set_process_state(self, index: int, value: int):
        self.state.process_state[index] = value

    def get_process_state(self, index: int) -> int:
        return self.state.process_state[index]

    def set_event_state(self, index: int, value: int):
        self.state.event_state[index] = value

    def get_event_state(self, index: int) -> int:
        return self.state.event_state[index]

    def modify_variable(self, name: str, new_val: int) -> None:
        self.variables[name] = new_val

    def get_variable_valuation(self, name: str) -> int:
        return self.variables[name]

    def execute(self, debug: bool = False) -> None:
        """
        Executes the simulation to exhaustively find all reachable states in the given process model.
        """

        index = 0
        while self.active_branches:
            if debug:
                index += 1
                if index % 100 == 0:
                    ls = len(self.explored_states)
                    la = len(self.active_branches)
                    print(f"{index}. Found {ls} states, {la} branches left.")
            # Choose a branch to continue and remove it from the active branches
            branch = random.choice(self.active_branches)
            self.active_branches.remove(branch)
            state, pcs, i, variables = branch

            # Find all possible next execution options
            next_steps = self.processes[i].get_next_steps(pcs[i], variables)

            # Execute every possible option
            for step in next_steps:
                self.state = copy.deepcopy(state)
                self.variables = copy.deepcopy(variables)
                self.execute_step(i, step, pcs)

        if debug:
            print(f"In total, {len(self.explored_states)} states were found.")

    def execute_step(self, proc_index: int, next_step: Tuple[Callable[[], None], int, bool], pcs: List[int]) -> None:
        """
        Executes a program transition and adds the result to the active branches if it has not yet been explored.

        :param proc_index: Index of the process to be executed
        :param next_step: A tuple describing the execution of the next process step
        :param pcs: A list of program counters for all processes
        """

        # Execute step
        fun, nxt, rel = next_step
        fun()

        # Create resulting state after execution
        new_state = (copy.deepcopy(self.state),
                     [pcs[k] if k != proc_index else nxt for k in range(len(pcs))],
                     copy.deepcopy(self.variables))

        # If the state has already been seen, ignore it
        if new_state not in self.explored_states:

            # Add the new state to the explored states
            self.explored_states.append(new_state)

            # If the lock is released any process could execute next
            if rel:
                # This state is reachable by all other states
                self.explored_states_reachable_by.append([i for i in range(self.n_proc + 1)])

                # Find all possible further run configurations
                next_procs = [n for n in range(self.n_proc) if self.state.process_state[n] == -1]
                # Scheduler can always run
                next_procs.append(self.n_proc)

                # Try to append every run configuration for the new state to the active branches
                for proc in next_procs:
                    if (new_state[0], new_state[1], proc, self.variables) not in self.active_branches:
                        self.active_branches.append((copy.deepcopy(new_state[0]),
                                                     copy.deepcopy(new_state[1]),
                                                     proc,
                                                     copy.deepcopy(self.variables)))
            # If the process kept the lock, then only this process can be executed next
            else:
                # This state is reachable only by the process itself
                self.explored_states_reachable_by.append([proc_index])

                if self.state.process_state[proc_index] == -1:
                    if (new_state[0], new_state[1], proc_index, self.variables) not in self.active_branches:
                        self.active_branches.append((copy.deepcopy(new_state[0]),
                                                     copy.deepcopy(new_state[1]),
                                                     proc_index,
                                                     copy.deepcopy(self.variables)))

        # An old state might be revisited by a different process that can also use it
        else:
            ind = self.explored_states.index(new_state)
            if rel:
                self.explored_states_reachable_by[ind] = [i for i in range(self.n_proc + 1)]
            else:
                if proc_index not in self.explored_states_reachable_by[ind]:
                    self.explored_states_reachable_by[ind].append(proc_index)

    def get_full_invariant(self, proc_names: List[str], cond: Tuple[Tuple[int, int]] = ()) -> str:
        """
        Returns a string representing all possible states, including all possible process program counters in these
        states.

        :param proc_names: A list of names to give to the processes for naming the program counters
        :param cond: A tuple of tuples of the form (process, program_counter) to restrict the selection of states
        :return: An invariant listing all states, including possible program counters
        """

        # ----------------------------------------------------------------
        def to_string(s: State, pcs: List[int], var: Dict[str, int]) -> str:
            # Replace the closing bracket at the end of the state representation with a line break to append more info
            state_str = str(s).replace(")", "\n")

            # Append process counters for each process
            state_str += "    && " + ' && '.join([f"{name}.pc == {pc}" for name, pc in zip(proc_names, pcs)]) + "\n"

            # Append variable valuations for each variable
            if self.variables:
                state_str += "    && " + ' && '.join([f"{variable} == {value}" for variable, value in var.items()])\
                             + "\n"

            # Replace the last line break with a bracket again and return
            return state_str[::-1].replace("\n", ")", 1)[::-1]

        # ----------------------------------------------------------------

        return '\n|| '.join([to_string(s, pcs, var)
                             for by, (s, pcs, var) in zip(self.explored_states_reachable_by, self.explored_states)
                             if all([pcs[c[0]] == c[1] for c in cond]) and any([c[0] in by for c in cond])]).lower()

    def get_scheduler_invariant(self, proc_names: List[str]) -> str:
        """
        Returns the states that are reachable in the scheduler.

        :param proc_names: A list of names to give to the processes for naming the program counters
        :return: An invariant listing all states, including program counters, that are reachable in the scheduler
        """

        return self.get_full_invariant(proc_names, ((self.n_proc, 0),))
