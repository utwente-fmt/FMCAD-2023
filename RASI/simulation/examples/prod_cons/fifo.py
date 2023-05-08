
class Fifo:
    
    def __init__(self, size):
        self.buffer = [0]*size
        self.r_pos = 0
        self.w_pos = 0
        self.n = 0

    def reset(self):
        self.buffer = [0]*len(self.buffer)
        self.r_pos = 0
        self.w_pos = 0
        self.n = 0