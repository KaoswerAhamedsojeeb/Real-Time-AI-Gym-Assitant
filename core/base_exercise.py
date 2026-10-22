from abc import ABC, abstractmethod

class BaseExercise(ABC):
    def __init__(self):
        self.reps = 0
        self.stage = None

    @abstractmethod
    def get_points(self, landmarks, idx):
        p = landmarks[idx]
        return (p.x, p.y)

    @abstractmethod
    def process(self, landmarks):
        pass

    @abstractmethod
    def reset(self):
        pass    