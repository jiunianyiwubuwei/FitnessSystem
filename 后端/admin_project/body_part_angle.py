from utils import detection_body_part, calculate_angle

"""
LEFT_SHOULDER — 左肩
LEFT_ELBOW — 左肘
LEFT_WRIST — 左手腕
RIGHT_SHOULDER — 右肩
RIGHT_ELBOW — 右肘
RIGHT_WRIST — 右手腕
LEFT_HIP — 左臀部
LEFT_KNEE — 左膝盖
LEFT_ANKLE — 左踝
RIGHT_HIP — 右臀部
RIGHT_KNEE — 右膝盖
RIGHT_ANKLE — 右踝
NOSE — 鼻子
"""
class BodyPartAngle:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    # 左臂角度
    def angle_of_the_left_arm(self):
        return calculate_angle(
            detection_body_part(self.landmarks, "LEFT_SHOULDER"),
            detection_body_part(self.landmarks, "LEFT_ELBOW"),
            detection_body_part(self.landmarks, "LEFT_WRIST")
        )

    # 🎯 右臂角度
    def angle_of_the_right_arm(self):
        return calculate_angle(
            detection_body_part(self.landmarks, "RIGHT_SHOULDER"),
            detection_body_part(self.landmarks, "RIGHT_ELBOW"),
            detection_body_part(self.landmarks, "RIGHT_WRIST")
        )

    # 🎯 左腿角度
    def angle_of_the_left_leg(self):
        return calculate_angle(
            detection_body_part(self.landmarks, "LEFT_HIP"),
            detection_body_part(self.landmarks, "LEFT_KNEE"),
            detection_body_part(self.landmarks, "LEFT_ANKLE")
        )

    # 🎯 右腿角度
    def angle_of_the_right_leg(self):
        return calculate_angle(
            detection_body_part(self.landmarks, "RIGHT_HIP"),
            detection_body_part(self.landmarks, "RIGHT_KNEE"),
            detection_body_part(self.landmarks, "RIGHT_ANKLE")
        )

    # 🎯 新增：腰部角度
    def angle_of_the_waist(self):
        return calculate_angle(
            detection_body_part(self.landmarks, "LEFT_SHOULDER"),
            detection_body_part(self.landmarks, "LEFT_HIP"),
            detection_body_part(self.landmarks, "RIGHT_HIP")
        )

    # 🎯 新增：手臂抬高角度
    def angle_of_the_arm_raise(self):
        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        l_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        return calculate_angle(l_shoulder, l_elbow, [l_elbow[0], l_elbow[1] - 1])

    # 🎯 新增：头部前倾角度
    def angle_of_the_head_tilt(self):
        nose = detection_body_part(self.landmarks, "NOSE")
        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        return calculate_angle(nose, l_shoulder, [l_shoulder[0], l_shoulder[1] - 1])
