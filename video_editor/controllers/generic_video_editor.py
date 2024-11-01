from abc import ABC, abstractmethod


class GenericVideoEditor(ABC):
    @abstractmethod
    def generateVideo(self, start_time, end_time, output_video_name):
        pass