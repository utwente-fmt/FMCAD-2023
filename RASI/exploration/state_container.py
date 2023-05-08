from abc import ABC, abstractmethod


class StateContainer(ABC):

    def __init__(self):
        self.n_proc: int = 0
        self.n_event: int = 0

    @abstractmethod
    def set_process_state(self, index: int, value: int) -> None:
        pass

    @abstractmethod
    def get_process_state(self, index: int) -> int:
        pass

    @abstractmethod
    def set_event_state(self, index: int, value: int) -> None:
        pass

    @abstractmethod
    def get_event_state(self, index: int) -> int:
        pass

    @abstractmethod
    def modify_variable(self, name: str, new_val: int) -> None:
        pass

    @abstractmethod
    def get_variable_valuation(self, name: str) -> int:
        pass
