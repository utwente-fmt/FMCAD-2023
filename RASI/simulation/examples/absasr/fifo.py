from simulator.main import Main, DELTA

class Fifo ():

    def __init__(self, name, size, not_full_ev, not_empty_ev):
        self.size = size
        self.name = name
        self.fifo = []
        self.not_full_ev = not_full_ev
        self.not_empty_ev = not_empty_ev

    def fifo_write(self, elem) :

        if len(self.fifo) >= self.size:
            raise Exception("Fifo is full! Can't write.")

        self.fifo.append(elem)
        return True

    
    def fifo_read(self) :
        
        if not self.fifo:
            raise Exception("Fifo is empty! Can't read.")

        x,self.fifo = self.fifo[0],self.fifo[1:]
        return x

    def is_full(self):
        return len(self.fifo) == self.size
        
    def is_empty(self):
        return not len(self.fifo)
        
    def reset(self):
        self.fifo = []