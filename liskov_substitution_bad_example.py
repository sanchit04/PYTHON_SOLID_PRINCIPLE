from abc import ABC,abstractmethod

class Bird(ABC):

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def fly_with_wings(self):
        pass

    @abstractmethod
    def build_nest(self):
        pass

class Ostrich(Bird):
    pass