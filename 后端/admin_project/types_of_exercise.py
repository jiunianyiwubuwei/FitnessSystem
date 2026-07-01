from utils import calculate_angle, detection_body_part


class TypeOfExercise:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    def calculate_exercise(self, exercise_type, counter, status):
        if exercise_type == "push-up":
            return self.push_up(counter, status)
        elif exercise_type == "pull-up":
            return self.pull_up(counter, status)
        elif exercise_type == "sit-up":
            return self.sit_up(counter, status)
        elif exercise_type == "squat":
            return self.squat(counter, status)
        elif exercise_type == "jumping-jack":
            return self.jumping_jack(counter, status)
        elif exercise_type == "jumping":
            return self.jumping(counter, status)
        elif exercise_type == "squat-jump":
            return self.squat_jump(counter, status)
        elif exercise_type == "jump-rope":
            return self.jump_rope(counter, status)
        elif exercise_type == "running":
            return self.running(counter, status)
        elif exercise_type == "plank":
            return self.plank(counter, status)
        elif exercise_type == "side-lunge":
            return self.side_lunge(counter, status)
        elif exercise_type == "leg-raise":
            return self.leg_raise(counter, status)
        elif exercise_type == "arm-curl":
            return self.arm_curl(counter, status)
        elif exercise_type == "shoulder-press":
            return self.shoulder_press(counter, status)
        elif exercise_type == "burpee":
            return self.burpee(counter, status)
        elif exercise_type == "high-knee":
            return self.high_knee(counter, status)
        else:
            return counter, status

    #引体向上
    def pull_up(self, counter, status):
        nose = detection_body_part(self.landmarks, "NOSE")
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        avg_shoulder_y = (left_elbow[1] + right_elbow[1]) / 2

        if status:
            if nose[1] > avg_shoulder_y:
                counter += 1
                status = False

        else:
            if nose[1] < avg_shoulder_y:
                status = True

        return [counter, status]

    # 俯卧撑
    def push_up(self, counter, status):
        elbow_angle = calculate_angle(
            detection_body_part(self.landmarks, "LEFT_SHOULDER"),
            detection_body_part(self.landmarks, "LEFT_ELBOW"),
            detection_body_part(self.landmarks, "LEFT_WRIST")
        )
        if elbow_angle < 70:
            status = False
        if elbow_angle > 160 and not status:
            counter += 1
            status = True
        return counter, status

    # ✅ 仰卧起坐
    def sit_up(self, counter, status):
        # 获取关键点
        left_hip = detection_body_part(self.landmarks, "LEFT_HIP")
        left_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        right_hip = detection_body_part(self.landmarks, "RIGHT_HIP")
        nose = detection_body_part(self.landmarks, "NOSE")

        # 计算躯干角度（左髋-左肩-右髋）
        trunk_angle = calculate_angle(left_hip, left_shoulder, right_hip)

        # 判断头部位置（y轴向下）
        nose_y = nose[1]
        shoulder_y = left_shoulder[1]

        # 状态切换逻辑
        if trunk_angle < 70 and nose_y < shoulder_y:
            status = False  # 坐起

        if trunk_angle > 160 and not status:
            counter += 1
            status = True  # 躺平

        # 调试输出
        print(f"Trunk Angle: {trunk_angle:.1f}° | Nose Y: {nose_y:.3f} | Status: {status}")
        return counter, status

    # ✅ 深蹲
    def squat(self, counter, status):
        knee_angle = calculate_angle(
            detection_body_part(self.landmarks, "LEFT_HIP"),
            detection_body_part(self.landmarks, "LEFT_KNEE"),
            detection_body_part(self.landmarks, "LEFT_ANKLE")
        )
        if knee_angle < 90:
            status = False
        if knee_angle > 160 and not status:
            counter += 1
            status = True
        return counter, status

    # ✅ 新增：开合跳
    def jumping_jack(self, counter, status):
        wrist_distance = abs(
            detection_body_part(self.landmarks, "LEFT_WRIST")[0] -
            detection_body_part(self.landmarks, "RIGHT_WRIST")[0]
        )
        if wrist_distance < 0.3:
            status = False
        if wrist_distance > 0.6 and not status:
            counter += 1
            status = True
        return counter, status

    # ✅ 新增：平板支撑
    def plank(self, counter, status):
        body_angle = calculate_angle(
            detection_body_part(self.landmarks, "LEFT_SHOULDER"),
            detection_body_part(self.landmarks, "LEFT_HIP"),
            detection_body_part(self.landmarks, "LEFT_KNEE")
        )
        if 160 <= body_angle <= 180:
            status = True
        else:
            status = False
        return counter, status

    # ✅ 新增：侧弓步
    def side_lunge(self, counter, status):
        knee_angle = calculate_angle(
            detection_body_part(self.landmarks, "LEFT_HIP"),
            detection_body_part(self.landmarks, "LEFT_KNEE"),
            detection_body_part(self.landmarks, "LEFT_ANKLE")
        )
        if knee_angle < 90:
            status = False
        if knee_angle > 160 and not status:
            counter += 1
            status = True
        return counter, status

    # ✅ 新增：抬腿
    def leg_raise(self, counter, status):
        hip_angle = calculate_angle(
            detection_body_part(self.landmarks, "LEFT_HIP"),
            detection_body_part(self.landmarks, "LEFT_KNEE"),
            detection_body_part(self.landmarks, "LEFT_ANKLE")
        )
        if hip_angle < 30:
            status = False
        if hip_angle > 70 and not status:
            counter += 1
            status = True
        return counter, status

    # ✅ 新增：哑铃弯举
    def arm_curl(self, counter, status):
        elbow_angle = calculate_angle(
            detection_body_part(self.landmarks, "LEFT_SHOULDER"),
            detection_body_part(self.landmarks, "LEFT_ELBOW"),
            detection_body_part(self.landmarks, "LEFT_WRIST")
        )
        if elbow_angle < 60:
            status = False
        if elbow_angle > 150 and not status:
            counter += 1
            status = True
        return counter, status

    # ✅ 新增：肩部推举
    def shoulder_press(self, counter, status):
        shoulder_angle = calculate_angle(
            detection_body_part(self.landmarks, "LEFT_ELBOW"),
            detection_body_part(self.landmarks, "LEFT_SHOULDER"),
            detection_body_part(self.landmarks, "LEFT_HIP")
        )
        if shoulder_angle > 160:
            status = False
        if shoulder_angle < 90 and not status:
            counter += 1
            status = True
        return counter, status

    # ✅ 新增：波比跳
    def burpee(self, counter, status):
        knee_angle = calculate_angle(
            detection_body_part(self.landmarks, "LEFT_HIP"),
            detection_body_part(self.landmarks, "LEFT_KNEE"),
            detection_body_part(self.landmarks, "LEFT_ANKLE")
        )
        if knee_angle < 60:
            status = False
        if knee_angle > 160 and not status:
            counter += 1
            status = True
        return counter, status

    # ✅ 新增：高抬腿
    def high_knee(self, counter, status):
        knee_height = detection_body_part(self.landmarks, "LEFT_KNEE")[1]
        hip_height = detection_body_part(self.landmarks, "LEFT_HIP")[1]

        if knee_height < hip_height:
            status = False
        if knee_height > hip_height and not status:
            counter += 1
            status = True
        return counter, status

        # ✅ 跳跃动作（新加）
    def jumping(self, counter, status):
        left_leg_angle = self.angle_of_the_left_leg()
        right_leg_angle = self.angle_of_the_right_leg()

        if status:
            if left_leg_angle > 160 and right_leg_angle > 160:
                counter += 1
                status = False
        else:
            if left_leg_angle < 120 and right_leg_angle < 120:
                status = True

        return [counter, status]

        # ✅ 深蹲跳

    def squat_jump(self, counter, status):
        knee_angle = calculate_angle(
            detection_body_part(self.landmarks, "LEFT_HIP"),
            detection_body_part(self.landmarks, "LEFT_KNEE"),
            detection_body_part(self.landmarks, "LEFT_ANKLE")
        )
        if knee_angle < 90:
            status = False
        if knee_angle > 160 and not status:
            counter += 1
            status = True
        return counter, status


        # ✅ 跳绳
    def jump_rope(self, counter, status):
        left_foot = detection_body_part(self.landmarks, "LEFT_ANKLE")[1]
        right_foot = detection_body_part(self.landmarks, "RIGHT_ANKLE")[1]
        if left_foot < 0.5 and right_foot < 0.5:
            status = False
        if left_foot > 0.5 and right_foot > 0.5 and not status:
            counter += 1
            status = True
        return counter, status

        # ✅ 跑步
    def running(self, counter, status):
        left_knee = detection_body_part(self.landmarks, "LEFT_KNEE")[1]
        right_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")[1]
        if left_knee < right_knee:
            status = False
        if right_knee < left_knee and not status:
            counter += 1
            status = True
        return counter, status
