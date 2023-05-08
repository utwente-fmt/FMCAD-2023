import sys
from .state import State
from random import choice
from .process import Process

DEBUG = 0

# configurations
SIM_END = 100  # How many times you schedule without finding new states.
SIM_COUNT = 1000 # How many times you run the simulation from the start.

# constants

## event state values:
DELTA    = -1
OCCURRED = -2
IDLE     = -3

## process state values
READY    = -1

## Other
MAXDELAY = 1000000


class Main ():
    
    def __init__(self):
        self.processes = {}
        self.events = {}
        self.vars = {}  # user defined variables with their reset values
        self.state = State()


    def register_process(self, proc: Process):
        """ Register a new process, generate it's internal pid 
            and save it indexed by it's name.
        """
        if proc.name in self.processes:
            raise Exception(
                f"ERROR: A process with name {proc.name} is already registered")
        pid = len(self.processes)
        self.processes[pid] = proc
        return pid


    def register_event(self, eid: int, name: str):
        """ Register a new event generate its internal eid
            and save it indexed by it's name.
        """
        if eid in self.events:
            raise Exception(
                f"ERROR: An event with id {eid} is already registered.")
        if name in self.events.values():
            raise Exception(
                f"ERROR: An event with name {name} is already registered.")
        self.events[eid] = name


    def register_var(self, var: str, val):
        if var in self.vars:
            raise Exception(
                f"ERROR: An variable with name {var} is already registered.")
        self.vars[var] = val

    def reset_simulation(self):

        for p in self.processes.values():
            p.reset()
            
        self.state["process_state"] = [READY for _ in self.processes]
        self.state["event_state"]   = [IDLE for _ in self.events]
        self.state["pc"]            = [0 for _ in self.processes]
        for var,val in self.vars.items():
            self.state[var] = val

        self.state.save()

    
    def change_state(self, var, val, idx=-1):
        if idx != -1:
            self.state[var][idx] = val
        else:
            self.state[var] = val
            
    def check_state(self, var, idx=-2):
        return self.state[var][idx] if idx >= 0 else self.state[var]
    
    def save_state(self, tag):
        self.state.save(tag)
        
    def save_state_all(self): 
        """ FIXME make the state saving cleaner. Currently we use several
            methods to save them within different classes.
        """
        self.state.save() # save it for the scheduler
        pcs = self.state['pc']
        for i,pc in enumerate(pcs):
            self.save_state(f'{self.processes[i].name}_{pc}')
    
    def wait(self, pid, pc, eid, time=None):
    
        if time:
            self.state["process_state"][pid] = eid
            self.state["event_state"][eid] = time    
        else:
            self.state["process_state"][pid] = eid

        # self.state.save() # save state at scheduler
#         self.state.save(f'{self.processes[pid].name}_{pc}') # save state at pc
        self.save_state_all()

    def set_pc(self, pid, val, save=False):
                
        self.state["pc"][pid] = val
        if save:
            self.state.save(f"{self.processes[pid].name}_{val}")
        

    def notify(self, eid, time):

        self.state['event_state'][eid] = time


    def simulate (self):

        self.reset_simulation()
        self.save_state_all()

        sim_end = 0
        sim_count = 0

        while(True):
            
            cstate = self.state.get_current_state()
            
            # Wake up processes waiting 0 time without delta delay
            self.state["process_state"] = \
                [-1 if x >= 0 and self.state["event_state"][x] == 0
                    else x for x in self.state["process_state"]]

            # Also reset any events that triggered
            self.state["event_state"] = \
                [-2 if x == 0 else x for x in self.state["event_state"]]

            assert cstate == self.state.get_current_state()
        
            # schedule processes
            while sum([x == READY for x in self.state["process_state"]]) == 0 :
                # print("Scheduling processes")
                
                if sum([x == -3 for x in self.state["event_state"]]) == len(self.state["event_state"]):
                    break
                                                
                # get minimum advance time
                delta = MAXDELAY
                for d in self.state["event_state"]:
                     delta = d if d >= -1 and d < delta else delta
                delta = 0 if delta == -1 or delta == MAXDELAY else delta

                assert delta >= 0
                                
                # advance time for events and reset occurred ones
                self.state["event_state"] = \
                    [-3 if x < -1 else x - delta for x in self.state["event_state"]]

                # wake up processes due to occurred events
                self.state["process_state"] = \
                    [-1 if x >= 0 and self.state["event_state"][x] in (0,-1) 
                        else x for x in self.state["process_state"]]
                
                # set occurred events to -2
                self.state["event_state"] = \
                    [-2 if x in (0,-1) else x for x in self.state["event_state"]]    
                        
                self.save_state_all()
                
                # FIXME exit all events idle
                
            # save the new scheduled state
            # if cstate != self.state.get_current_state():
            self.save_state_all()

            # FIXME end simulation if no process ready?

            # get processes ready to execute
            choices = [i for i in range(0,len(self.state["process_state"])) \
                if self.state["process_state"][i] == -1]

            if not choices: # deadlock?
                print("WARNING: deadlock found.",file=sys.stderr)
                print(self.state,file=sys.stderr)
                sim_end = 0
                sim_count += 1                
                self.reset_simulation()
                if sim_count >= SIM_COUNT:
                    self.end_simulation()
                    break
                continue

            
            # we schedule a random one
            i = choice(choices)
            sspace = len(self.state)

            # self.state.save(f"i_{self.state['pc'][i]}")
            # print(f"Running process {self.processes[i].name}")
            # this one may be redundant due to the save_state_all above:
            self.state.save(f'{self.processes[i].name}_{self.processes[i].pc}') 
            self.processes[i].run()

            if len(self.state) == sspace :
                sim_end += 1
                
            if sim_end >= SIM_END:
                sim_end = 0
                sim_count += 1
                self.reset_simulation()
                if sim_count >= SIM_COUNT:
                    self.end_simulation()
                    break

    def end_simulation(self):
        
        self.state.state_list = sorted(self.state.state_list)
        
        invs, allinvs = self.get_all_invariants()# (None,("prod_3",))
        
        for x in invs:
            print(x)
            
        for p in self.processes:
            print(f"// Process with pid {p} is called {self.processes[p].name}")
        mssg = f"// Found a total of {len(self.state)} states ({self.count_states_no_tag()} real states)."
        print(mssg)
        print(mssg, file=sys.stderr)
    
    def get_all_invariants(
        self, 
        filter: (str,)=None, 
        trivial_invs: (str,)=() )-> [str]:
        
        self.state.state_list = sorted(self.state.state_list)
        allstates = ""
        
        invariant = ""
        result = []
        oldtag = ""
        count = 0
        
        for x in self.state.state_list:
            
            if x[0] != oldtag: # new invariant
                # close old invariant
                if invariant:
                    invariant = invariant[:-3] + f");// invariant for {oldtag} has {count} states.\n"
                    if not filter or oldtag in filter:
                        result.append(invariant)
                # reset for next invariant
                invariant = ""
                count = 0    
                oldtag = x[0]
                # init next invariant
                invariant = "// This invariant has been generated with the simulation tool:\n"
                if oldtag == "scheduler":
                    invariant += "inline resource reachable_abstract_states_invariant() = true **\n(\n"
                else:
                    invariant += f"inline resource reachable_states_{oldtag}() = true **\n(\n"
            # add new state
            newstate = self.format_state(x) + "\n||\n"
            invariant += newstate
            allstates += newstate
            count += 1
        # to close last invariant
        invariant = invariant[:-3] + f");// invariant for {oldtag} has {count} states.\n"
        if not filter or oldtag in filter:
            result.append(invariant)
        
        invariant = ""
        for name in trivial_invs:
            invariant = "// This invariant has been generated with the simulation tool:\n"
            invariant += f"inline resource reachable_states_{name}() = false; // has 0 states.\n"
            result.append(invariant)

        return result, allstates[:-3]
    
    def get_scheduler_invariant(self) -> str:
        
        states = [x for x in self.state.state_list if x[0] == "scheduler"]
        
        invariant = "// This invariant has been generated with the simulation tool:\n"
        invariant += "inline resource reachable_abstract_states_invariant() = true **\n(\n"
        
        for x in states:
            invariant += self.format_state(x) + "\n||\n"
        
        return invariant[:-3] + f");// the scheduler invariant has {len(states)} states.\n"
        
    def get_pc_invariant(self, pid, pc) -> str:
        
        states = [x for x in self.state.state_list if x[0] == f"{pid}_{pc}"]
        
        invariant = "// This invariant has been generated with the simulation tool:\n"
        invariant += f"inline resource reachable_abstract_states_invariant_{pid}_{pc}() = true **\n(\n"
        
        if not states:
            invariant += "true\n||\n"
        
        for x in states:
            invariant += self.format_state(x) + "\n||\n"
        
        return invariant[:-3] + f");// has {len(states)} states.\n"
        
    def format_state_invariant_splitted(self, states, subst: str, pid: int) -> str:
        """
        Generates invariants for the set of states <states> where each invariant
        filters only states with the same value for <state[substr][pid]>.
        """
        
        d = dict()
        
        for s in states:
            aux = dict(s[1:])
            d.setdefault(aux[subst][pid],[]).append(s)
        
        result = []
        
        for k in d:
            proc = self.processes[pid]
            inv = f"inline resource reachable_states_splitted_{proc.name}_{subst}_{k}() = true **\n(\n"
            for v in d[k]:
                inv += self.format_state(v) + "\n||\n"
            inv = inv[:-3] + f"); // invariant for {proc.name}_{subst}_{k} has {len(d[k])} states.\n"
            result.append(inv)

        return result
        

    def format_state(self, st) :
        tag = st[0]
        st = dict(st[1:])
        
        state = "(\n"    

        for p in self.processes:
            state += f"process_state[{p}] == {st['process_state'][p]} && "  
            
        state += "\n"
        
        for e in self.events:
            state += f"event_state[{e}] == {st['event_state'][e]} && "
        
        state += "\n"

        for pid,proc in self.processes.items():
            state += f"{proc.name}.pc == {st['pc'][pid]} && "
        
        for var, val in st.items():
            if var not in ('process_state','event_state','pc'):
                state += f"{var} == {val[0]} && "
        
        state = state[:-3] + "\n)"

        return state
        
    def count_states_no_tag(self):
        notags = [x[1:] for x in self.state.state_list]
        return len(set(notags))


if __name__ == "__main__":
    m = Main()
    m.run()

