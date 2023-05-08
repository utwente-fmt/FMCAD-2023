class State(dict):
    
    def __init__(self):
        super().__init__()
        self.state_space = set(())
        self.state_list = []

    def get_current_state (self):
        return self

    def __len__(self):
        return len(self.state_space)

    def save (self, tag="scheduler"):
        # copy the state into a hashable tuple
        t = (tag,)
        for x,y in self.items():
            t += ((x,self.totuple(y)),)
        # save the tupple if it does not exist
        if not t in self.state_space:
            self.state_space.add(t)
            self.state_list.append(t)
        return len(self)
        
    def totuple(self, value):
        if type(value) == list:
            return tuple(value)
        elif type(value) == int:
            return (value,)
        elif type(value) == bool:
            return (value,)
        else:
            raise Exception(f"Unsupported type {type(value)}")