from core.base_exercise import BaseExercise

class LungesDetector(BaseExercise):
    DOWN_THRESHOLD = 100
    UP_THRESHOLD = 160
    MIN_VISIVILITY = 0.7

    LEFT_HIP = 23
    LEFT_KNEE = 25
    LEFT_ANKLE = 27
    RIGHT_HIP = 24
    RIGHT_KNEE = 26 
    RIGHT_ANKLE = 28
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12

    def __init__(self):
        super().__init__()
        self.stage = "up"

    def get_points(self, landmarks, idx):
        p = landmarks[idx] # p->points
        return (p.x, p.y)

    def process(self, landmarks):   
        left_hip = self.get_points(landmarks, self.LEFT_HIP)
        left_knee = self.get_points(landmarks, self.LEFT_KNEE)
        left_ankle = self.get_points(landmarks, self.LEFT_ANKLE)
    
        right_hip = self.get_points(landmarks, self.RIGHT_HIP)
        right_knee = self.get_points(landmarks, self.RIGHT_KNEE)
        right_ankle = self.get_points(landmarks, self.RIGHT_ANKLE)
    
        left_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
    
        left_visibility = landmarks[self.LEFT_HIP].visibility
        right_visibility = landmarks[self.RIGHT_HIP].visibility
    
        if left_visibility >= right_visibility:
            knee_angle = left_angle
            hip_idx, knee_idx, ankle_idx, shoulder_idx = self.LEFT_HIP, self.LEFT_KNEE, self.LEFT_ANKLE, self.LEFT_SHOULDER
            
        else:
            knee_angle = right_angle
            hip_idx, knee_idx, ankle_idx, shoulder_idx = self.RIGHT_HIP, self.RIGHT_KNEE, self.RIGHT_ANKLE, self.RIGHT_SHOULDER
    