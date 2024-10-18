from abc import ABC, abstractmethod


class GenericVideoEditor(ABC):
    @abstractmethod
    def generateVideo(self):
        pass