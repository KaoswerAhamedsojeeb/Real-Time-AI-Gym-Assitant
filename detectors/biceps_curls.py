from core.base_exercise import BaseExercise

class BicepsCurlsDetector(BaseExercise):  
    
    DOWN_THRESHOLD = 90
    UP_THRESHOLD = 160
    MIN_VISIBILITY = 0.7

    LEFT_SHOULDER = 11
    LEFT_ELBOW = 13
    LEFT_WRIST = 15
    LEFT_KNEE = 25
    LEFT_HIP = 23
    RIGHT_SHOULDER = 12
    RIGHT_ELBOW = 14
    RIGHT_WRIST = 16
    RIGHT_KNEE = 26 
    RIGHT_HIP = 24



    def __init__(self):
        super().__init__()
        self.stage = "down"

    def get_points(self, landmarks, idx):
        p = landmarks[idx] # p->points
        return (p.x, p.y)
    
    def process(self, landmarks):   
        left_shoulder = self.get_points(landmarks, self.LEFT_SHOULDER)
        left_elbow = self.get_points(landmarks, self.LEFT_ELBOW)
        left_wrist = self.get_points(landmarks, self.LEFT_WRIST)

        right_shoulder = self.get_points(landmarks, self.RIGHT_SHOULDER)
        right_elbow = self.get_points(landmarks, self.RIGHT_ELBOW)
        right_wrist = self.get_points(landmarks, self.RIGHT_WRIST)

        left_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)

        left_visibility = landmarks[self.LEFT_SHOULDER].visibility
        right_visibility = landmarks[self.RIGHT_SHOULDER].visibility

        if left_visibility >= right_visibility:
            elbow_angle = left_angle
            shoulder_idx, elbow_idx, wrist_idx,hip_idx, knee_idx = self.LEFT_SHOULDER, self.LEFT_ELBOW, self.LEFT_WRIST,self.LEFT_HIP, self.LEFT_KNEE
        else:
            elbow_angle = right_angle
            shoulder_idx, elbow_idx, wrist_idx,hip_idx, knee_idx = self.RIGHT_SHOULDER, self.RIGHT_ELBOW, self.RIGHT_WRIST, self.RIGHT_HIP, self.RIGHT_KNEE

        back_angle = self.calculate_angle(self.get_points(landmarks, shoulder_idx), self.get_points(landmarks, hip_idx), self.get_points(landmarks, knee_idx))


        key_landmarks_visibility = (landmarks[shoulder_idx].visibility >= self.MIN_VISIBILITY and
                                    landmarks[elbow_idx].visibility >= self.MIN_VISIBILITY and
                                    landmarks[wrist_idx].visibility >= self.MIN_VISIBILITY)

        if key_landmarks_visibility:
            if elbow_angle < self.DOWN_THRESHOLD and self.stage == "up":
                self.stage = "down"
            elif elbow_angle > self.UP_THRESHOLD and self.stage == "down":
                self.stage = "up"
                self.reps += 1
        if self.stage == "down":
            form_status = "good depth" if elbow_angle < self.DOWN_THRESHOLD else "not deep enough"  
        elif self.stage == "up":
            form_status = "good form" if elbow_angle > self.UP_THRESHOLD else "not fully extended"
        else:
            form_status = "N/A"

        return {"reps": self.reps,
                "elbow_angle": int(elbow_angle),
                "back_angle" : int(back_angle),
                "form_status": form_status
                
                }

    def reset(self):    
        self.reps = 0
        self.stage = "down"