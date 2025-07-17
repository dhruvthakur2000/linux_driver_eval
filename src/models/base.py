from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def generate_code(self,prompt:str)->str:
        pass