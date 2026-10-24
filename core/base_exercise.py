from abc import ABC, abstractmethod

class BaseExercise(ABC):
    def __init__(self):
        self.reps = 0
        self.stage = None


    def calculate_angle(self, a, b, c):
        import numpy as np
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle > 180.0:
            angle = 360-angle

        return angle

    @abstractmethod
    def get_points(self, landmarks, idx):
        p = landmarks[idx] # p->points
        return (p.x, p.y)

    @abstractmethod
    def process(self, landmarks):
        pass

    @abstractmethod
    def reset(self):
        pass    