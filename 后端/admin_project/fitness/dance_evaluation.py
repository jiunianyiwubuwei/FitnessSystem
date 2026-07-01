# dance_evaluation.py
# 舞蹈评分核心算法模块
# 用于关键点提取、动态标准学习和舞蹈评分计算

import cv2
import mediapipe as mp
import numpy as np
import json
from typing import List, Tuple, Optional, Dict
from scipy.spatial.distance import cdist
from scipy.signal import find_peaks


# ============================================================================
# MediaPipe Pose 关键点索引定义
# ============================================================================
class PoseLandmark:
    """MediaPipe Pose 33个关键点索引"""
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32


# 关节角度定义：三个关键点索引
JOINT_ANGLES = {
    # 手臂角度 (肩-肘-腕)
    'left_elbow': [PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_ELBOW, PoseLandmark.LEFT_WRIST],
    'right_elbow': [PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_WRIST],
    # 肩膀角度 (肘-肩-髋)
    'left_shoulder': [PoseLandmark.LEFT_ELBOW, PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_HIP],
    'right_shoulder': [PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_HIP],
    # 髋部角度 (肩-髋-膝)
    'left_hip': [PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_HIP, PoseLandmark.LEFT_KNEE],
    'right_hip': [PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_HIP, PoseLandmark.RIGHT_KNEE],
    # 膝盖角度 (髋-膝-踝)
    'left_knee': [PoseLandmark.LEFT_HIP, PoseLandmark.LEFT_KNEE, PoseLandmark.LEFT_ANKLE],
    'right_knee': [PoseLandmark.RIGHT_HIP, PoseLandmark.RIGHT_KNEE, PoseLandmark.RIGHT_ANKLE],
    # 躯干角度 (肩-髋-垂直，用于身体前倾判断)
    'trunk': [PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_HIP, PoseLandmark.LEFT_KNEE],
}

# 踢腿角度计算（腿相对于垂直方向的角度）
KICK_ANGLES = {
    'left_leg_kick': [PoseLandmark.LEFT_HIP, PoseLandmark.LEFT_ANKLE],
    'right_leg_kick': [PoseLandmark.RIGHT_HIP, PoseLandmark.RIGHT_ANKLE],
}


# ============================================================================
# 工具函数
# ============================================================================

def compute_joint_angle(landmarks_flat: List[float], idx1: int, idx2: int, idx3: int) -> Optional[float]:
    """计算三点形成的关节角度（度数）"""
    try:
        p1 = np.array([landmarks_flat[idx1 * 4], landmarks_flat[idx1 * 4 + 1]])
        p2 = np.array([landmarks_flat[idx2 * 4], landmarks_flat[idx2 * 4 + 1]])
        p3 = np.array([landmarks_flat[idx3 * 4], landmarks_flat[idx3 * 4 + 1]])

        v1 = p1 - p2
        v2 = p3 - p2
        dot = np.dot(v1, v2)
        mag = np.linalg.norm(v1) * np.linalg.norm(v2)
        if mag < 1e-6:
            return None
        cos_angle = np.clip(dot / mag, -1.0, 1.0)
        return np.arccos(cos_angle) * 180.0 / np.pi
    except:
        return None


def compute_kick_angle(landmarks_flat: List[float], hip_idx: int, ankle_idx: int) -> Optional[float]:
    """计算腿踢出角度（相对于垂直向下方向，0°=水平踢出，90°=自然下垂）"""
    try:
        hip = np.array([landmarks_flat[hip_idx * 4], landmarks_flat[hip_idx * 4 + 1]])
        ankle = np.array([landmarks_flat[ankle_idx * 4], landmarks_flat[ankle_idx * 4 + 1]])

        # 腿向量
        dx = ankle[0] - hip[0]
        dy = ankle[1] - hip[1]
        leg_len = np.sqrt(dx * dx + dy * dy)
        if leg_len < 0.01:
            return None

        # 与垂直向下方向的夹角（MediaPipe Y轴向下，所以垂直向下是(0,1)）
        # cos(theta) = dot((0,1), (dx,dy)/len) = dy/len
        cos_angle = np.clip(dy / leg_len, -1.0, 1.0)
        angle = np.arccos(cos_angle) * 180.0 / np.pi
        return angle
    except:
        return None


def get_visibility(landmarks_flat: List[float], idx: int) -> float:
    """获取关键点可见度"""
    try:
        return landmarks_flat[idx * 4 + 3]
    except:
        return 0.0


def compute_frame_angles(landmarks_flat: List[float]) -> Dict[str, Optional[float]]:
    """计算单帧所有关节角度，返回 {关节名: 角度值} 字典"""
    angles = {}
    for joint_name, (i1, i2, i3) in JOINT_ANGLES.items():
        angles[joint_name] = compute_joint_angle(landmarks_flat, i1, i2, i3)
    for joint_name, (hip_i, ankle_i) in KICK_ANGLES.items():
        angles[joint_name] = compute_kick_angle(landmarks_flat, hip_i, ankle_i)
    return angles


# ============================================================================
# 姿态关键点提取器
# ============================================================================

class PoseKeypointExtractor:
    """姿态关键点提取器"""

    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def extract_frame_keypoints(self, frame) -> Optional[List[float]]:
        """从单帧图像提取33个关键点"""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if results.pose_landmarks:
            keypoints = []
            for landmark in results.pose_landmarks.landmark:
                keypoints.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
            return keypoints
        return None

    def extract_video_keypoints(self, video_path: str) -> Tuple[List[Optional[List[float]]], float, int]:
        """从视频中提取所有帧的关键点"""
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"无法打开视频: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0

        keypoints_sequence = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            keypoints = self.extract_frame_keypoints(frame)
            keypoints_sequence.append(keypoints)

        cap.release()
        return keypoints_sequence, duration, frame_count

    def draw_pose_on_frame(self, frame, landmarks) -> np.ndarray:
        """在帧上绘制姿态骨架"""
        return self.mp_drawing.draw_landmarks(
            frame, landmarks, self.mp_pose.POSE_CONNECTIONS
        )

    def extract_angle_sequence(self, keypoints_sequence: List[Optional[List[float]]]) -> Dict[str, List[Optional[float]]]:
        """从关键点序列中提取所有关节角度序列"""
        angle_sequences = {}

        # 关节角度（三点夹角）
        for joint_name, (idx1, idx2, idx3) in JOINT_ANGLES.items():
            angle_sequences[joint_name] = []
            for kp in keypoints_sequence:
                if kp is None:
                    angle_sequences[joint_name].append(None)
                else:
                    angle = compute_joint_angle(kp, idx1, idx2, idx3)
                    angle_sequences[joint_name].append(angle)

        # 踢腿角度（腿踢出角度）
        for joint_name, (hip_idx, ankle_idx) in KICK_ANGLES.items():
            angle_sequences[joint_name] = []
            for kp in keypoints_sequence:
                if kp is None:
                    angle_sequences[joint_name].append(None)
                else:
                    angle = compute_kick_angle(kp, hip_idx, ankle_idx)
                    angle_sequences[joint_name].append(angle)

        return angle_sequences


# ============================================================================
# 动态角度标准学习器
# ============================================================================

class AngleStandardLearner:
    """
    从标准舞蹈视频自动学习关节角度动态标准

    学习内容：
    1. 每个关节的标准角度范围（min/max/mean/std）
    2. 每帧的目标角度曲线（关键帧）
    3. 角度变化的"标准速率"（相邻帧最大变化量）
    4. 动作阶段划分（起势/发力/收势）
    5. 关键pose（角度极值点）
    """

    def __init__(self):
        self.extractor = PoseKeypointExtractor()

    def learn_from_video(self, video_path: str) -> Dict:
        """
        从标准视频学习动态角度标准

        Returns:
            包含以下内容的字典：
            - angle_sequences: 每帧各关节角度
            - angle_stats: 各关节角度统计（min/max/mean/std）
            - target_curves: 每帧目标角度（用于实时对比）
            - keyframes: 关键帧信息（极值点）
            - delta_stats: 角度变化速率统计
            - phase_info: 动作阶段信息
        """
        print(f"[AngleStandardLearner] 开始处理视频: {video_path}")

        # 1. 提取关键点序列
        keypoints_seq, duration, frame_count = self.extractor.extract_video_keypoints(video_path)
        print(f"[AngleStandardLearner] 提取到 {frame_count} 帧")

        # 2. 提取角度序列
        angle_sequences = self.extractor.extract_angle_sequence(keypoints_seq)
        print(f"[AngleStandardLearner] 提取了 {len(angle_sequences)} 个关节角度序列")

        # 3. 统计分析各关节角度
        angle_stats = self._compute_angle_statistics(angle_sequences)
        print(f"[AngleStandardLearner] 统计完成，各关节角度范围：")
        for joint, stats in angle_stats.items():
            if stats['valid_frames'] > 0:
                print(f"  {joint}: {stats['min']:.1f}° ~ {stats['max']:.1f}° (均值: {stats['mean']:.1f}°)")

        # 4. 提取关键帧（角度极值点）
        keyframes = self._extract_keyframes(angle_sequences, frame_count)
        print(f"[AngleStandardLearner] 提取了 {len(keyframes)} 个关键帧")

        # 5. 计算角度变化速率
        delta_stats = self._compute_delta_statistics(angle_sequences)
        print(f"[AngleStandardLearner] 角度变化速率分析完成")

        # 6. 动作阶段分析
        phase_info = self._analyze_phases(angle_sequences, frame_count)
        print(f"[AngleStandardLearner] 动作阶段分析完成：{phase_info['phase_names']}")

        result = {
            'angle_sequences': {k: [None if v is None else round(v, 2) for v in vals]
                               for k, vals in angle_sequences.items()},
            'angle_stats': angle_stats,
            'target_curves': self._build_target_curves(angle_sequences),
            'keyframes': keyframes,
            'delta_stats': delta_stats,
            'phase_info': phase_info,
            'total_frames': frame_count,
            'duration': round(duration, 2),
        }

        print(f"[AngleStandardLearner] 学习完成！")
        return result

    def _compute_angle_statistics(self, angle_sequences: Dict[str, List[Optional[float]]]) -> Dict:
        """计算各关节角度的统计信息"""
        stats = {}
        for joint_name, angles in angle_sequences.items():
            valid = [a for a in angles if a is not None]
            if len(valid) == 0:
                stats[joint_name] = {
                    'min': 0, 'max': 0, 'mean': 0, 'std': 0,
                    'valid_frames': 0, 'total_frames': len(angles),
                    'acceptable_min': 0, 'acceptable_max': 180,
                    'excellent_min': 0, 'excellent_max': 180,
                    'lower_quartile': 0, 'upper_quartile': 180,
                }
                continue

            valid_arr = np.array(valid)
            mean_val = float(np.mean(valid_arr))
            std_val = float(np.std(valid_arr))
            min_val = float(np.min(valid_arr))
            max_val = float(np.max(valid_arr))

            # 百分位数（更稳健的范围估计）
            p10 = float(np.percentile(valid_arr, 10))
            p25 = float(np.percentile(valid_arr, 25))
            p75 = float(np.percentile(valid_arr, 75))
            p90 = float(np.percentile(valid_arr, 90))

            # 判断关节类型，设置合理的上下限
            is_kick = 'kick' in joint_name

            if is_kick:
                # 踢腿角度：0° = 水平踢出，90° = 自然下垂
                # 合理范围 0° ~ 90°（不可能超过90°）
                min_limit, max_limit = 0, 90
                excellent_min = max(p10, 0)
                excellent_max = min(p90, 45)  # 优秀标准：踢腿不超过45°
            elif 'elbow' in joint_name or 'knee' in joint_name:
                # 关节弯曲角度：伸直=180°，完全弯曲≈30°
                min_limit, max_limit = 30, 180
                excellent_min = max(p10, 140)  # 优秀：接近伸直
                excellent_max = min(p90, 180)
            elif 'shoulder' in joint_name or 'hip' in joint_name:
                # 肩髋抬举角度：合理范围 0° ~ 180°
                min_limit, max_limit = 0, 180
                # 根据均值判断动作类型（高抬腿 vs 正常站立）
                if mean_val > 90:
                    excellent_min = max(p10, 80)
                    excellent_max = min(p90, 180)
                else:
                    excellent_min = max(p10, 0)
                    excellent_max = min(p90, 90)
            else:
                min_limit, max_limit = 0, 180
                excellent_min = max(p10, 0)
                excellent_max = min(p90, 180)

            # 可接受范围：用 IQR 扩展（更稳健）
            iqr = p75 - p25
            acceptable_min = max(p25 - 1.5 * iqr, min_limit)
            acceptable_max = min(p75 + 1.5 * iqr, max_limit)

            stats[joint_name] = {
                'min': round(min_val, 2),
                'max': round(max_val, 2),
                'mean': round(mean_val, 2),
                'std': round(std_val, 2),
                'valid_frames': len(valid),
                'total_frames': len(angles),
                'is_kick': is_kick,  # 标记是否为踢腿关节
                # 可接受范围（IQR方法，角度受限）
                'acceptable_min': round(acceptable_min, 2),
                'acceptable_max': round(acceptable_max, 2),
                # 优秀标准（基于百分位数）
                'excellent_min': round(excellent_min, 2),
                'excellent_max': round(excellent_max, 2),
                # 四分位数（供分析参考）
                'lower_quartile': round(p25, 2),
                'upper_quartile': round(p75, 2),
                'p10': round(p10, 2),
                'p90': round(p90, 2),
            }
        return stats

    def _extract_keyframes(self, angle_sequences: Dict[str, List[Optional[float]]],
                          total_frames: int) -> List[Dict]:
        """提取关键帧（角度极值点）"""
        keyframes = []

        for joint_name, angles in angle_sequences.items():
            valid = [(i, a) for i, a in enumerate(angles) if a is not None]
            if len(valid) < 5:
                continue

            values = np.array([a for _, a in valid])

            # 找极大值点（踢腿到最高）
            try:
                peaks, properties = find_peaks(values, distance=5, prominence=5)
                for peak_idx in peaks:
                    frame_idx = valid[peak_idx][0]
                    keyframes.append({
                        'joint': joint_name,
                        'frame': frame_idx,
                        'angle': round(values[peak_idx], 2),
                        'type': 'peak',
                        'position': frame_idx / total_frames  # 相对位置 0-1
                    })
            except:
                pass

            # 找极小值点（收腿）
            try:
                troughs, _ = find_peaks(-values, distance=5, prominence=5)
                for trough_idx in troughs:
                    frame_idx = valid[trough_idx][0]
                    keyframes.append({
                        'joint': joint_name,
                        'frame': frame_idx,
                        'angle': round(values[trough_idx], 2),
                        'type': 'trough',
                        'position': frame_idx / total_frames
                    })
            except:
                pass

        # 按帧排序
        keyframes.sort(key=lambda k: k['frame'])
        return keyframes

    def _compute_delta_statistics(self, angle_sequences: Dict[str, List[Optional[float]]]) -> Dict:
        """计算角度变化速率统计"""
        delta_stats = {}
        for joint_name, angles in angle_sequences.items():
            valid = [a for a in angles if a is not None]
            if len(valid) < 2:
                delta_stats[joint_name] = {'max_delta': 0, 'mean_delta': 0, 'std_delta': 0}
                continue

            # 计算相邻帧的角度变化
            deltas = []
            for i in range(1, len(valid)):
                delta = abs(valid[i] - valid[i - 1])
                deltas.append(delta)

            stats_max = round(float(np.max(deltas)), 2) if deltas else 0
            stats_mean = round(float(np.mean(deltas)), 2) if deltas else 0
            stats_std = round(float(np.std(deltas)), 2) if deltas else 0
            delta_stats[joint_name] = {
                'max_delta': stats_max,
                'mean_delta': stats_mean,
                'std_delta': stats_std,
            }
        return delta_stats

    def _analyze_phases(self, angle_sequences: Dict[str, List[Optional[float]]],
                       total_frames: int) -> Dict:
        """分析动作阶段（起势/发力/收势）"""
        # 简单分析：基于帧数均分 + 角度变化检测
        phase_boundaries = []
        phase_names = []

        # 策略1：基于帧数均分
        third = total_frames // 3
        if third > 0:
            phase_boundaries = [0, third, third * 2, total_frames]
            phase_names = ['起势', '发力', '收势']
        else:
            phase_boundaries = [0, total_frames]
            phase_names = ['整体']

        # 策略2：基于角度变化剧烈程度检测阶段切换点
        # 找角度变化最大的点作为阶段切换点
        if 'left_leg_kick' in angle_sequences:
            angles = angle_sequences['left_leg_kick']
            valid = [(i, a) for i, a in enumerate(angles) if a is not None]
            if len(valid) >= 10:
                values = np.array([a for _, a in valid])
                # 计算一阶差分
                diffs = np.abs(np.diff(values))
                # 找差分最大的点
                max_diff_idx = np.argmax(diffs)
                if max_diff_idx > 2 and max_diff_idx < len(valid) - 2:
                    switch_frame = valid[max_diff_idx][0]
                    if third > 0 and abs(switch_frame - third) > third // 2:
                        # 阶段切换点与均分点差异较大，使用检测到的切换点
                        pass  # 暂时使用均分，后续可优化

        return {
            'phase_boundaries': phase_boundaries,
            'phase_names': phase_names,
            'description': {
                '起势': '准备阶段，动作幅度较小',
                '发力': '主要动作阶段，角度变化最大',
                '收势': '恢复阶段，动作逐渐回到初始位置'
            }
        }

    def _build_target_curves(self, angle_sequences: Dict[str, List[Optional[float]]]) -> Dict[str, List[Optional[float]]]:
        """构建每帧目标角度曲线"""
        # 平滑处理后的角度序列作为目标曲线
        target_curves = {}
        for joint_name, angles in angle_sequences.items():
            valid_angles = [a for a in angles if a is not None]
            if len(valid_angles) < 3:
                target_curves[joint_name] = angles
                continue

            # 简单移动平均平滑
            smoothed = []
            window = 3
            for i in range(len(angles)):
                if angles[i] is None:
                    smoothed.append(None)
                else:
                    start = max(0, i - window // 2)
                    end = min(len(angles), i + window // 2 + 1)
                    window_vals = [angles[j] for j in range(start, end) if angles[j] is not None]
                    if window_vals:
                        smoothed.append(round(float(np.mean(window_vals)), 2))
                    else:
                        smoothed.append(None)

            target_curves[joint_name] = smoothed
        return target_curves


# ============================================================================
# 舞蹈评分器（支持动态标准）
# ============================================================================

class DanceScorer:
    """舞蹈评分器 - 支持动态标准评分"""

    def __init__(self):
        self.landmark_count = 33

    def evaluate(self, user_keypoints: List[Optional[List[float]]],
                 standard_keypoints: List[Optional[List[float]]],
                 angle_standards: Optional[Dict] = None) -> Dict:
        """
        综合评分函数

        Args:
            user_keypoints: 用户视频关键点序列
            standard_keypoints: 标准视频关键点序列
            angle_standards: 标准视频的动态角度标准（从 AngleStandardLearner 学习得到）

        Returns:
            评分结果字典
        """
        extractor = PoseKeypointExtractor()

        # 提取用户角度序列
        user_angles = extractor.extract_angle_sequence(user_keypoints)

        # 如果有动态标准，使用动态标准评分
        if angle_standards and 'angle_stats' in angle_standards:
            return self._evaluate_with_dynamic_standards(user_angles, angle_standards)

        # 否则使用传统的 DTW 方法
        return self._evaluate_with_dtw(user_keypoints, standard_keypoints)

    def _evaluate_with_dynamic_standards(self, user_angles: Dict[str, List[Optional[float]]],
                                        angle_standards: Dict) -> Dict:
        """使用动态标准评分"""
        angle_stats = angle_standards.get('angle_stats', {})
        target_curves = angle_standards.get('target_curves', {})
        phase_info = angle_standards.get('phase_info', {})

        joint_scores = {}
        all_scores = []
        phase_scores = {phase: [] for phase in phase_info.get('phase_names', ['整体'])}

        total_frames = len(next((v for v in user_angles.values() if len(v) > 0), []))

        for joint_name, user_seq in user_angles.items():
            stats = angle_stats.get(joint_name, {})
            target_curve = target_curves.get(joint_name, [])

            if not stats or stats.get('valid_frames', 0) == 0:
                continue

            joint_score_list = []

            for frame_idx, user_angle in enumerate(user_seq):
                if user_angle is None:
                    continue

                # 确定当前帧所在阶段
                phase = self._get_phase_for_frame(frame_idx, total_frames, phase_info)

                # 计算该帧得分
                score = self._score_frame_with_standards(
                    user_angle, stats, target_curve[frame_idx] if frame_idx < len(target_curve) else None
                )
                joint_score_list.append(score)
                all_scores.append(score)
                phase_scores[phase].append(score)

            if joint_score_list:
                joint_scores[joint_name] = {
                    'mean': round(float(np.mean(joint_score_list)), 2),
                    'min': round(float(np.min(joint_score_list)), 2),
                    'frames': len(joint_score_list)
                }

        # 计算各项得分
        overall_score = round(float(np.mean(all_scores)), 2) if all_scores else 0

        # 分阶段得分
        phase_result = {}
        for phase, scores in phase_scores.items():
            if scores:
                phase_result[phase] = round(float(np.mean(scores)), 2)

        # 综合评分
        accuracy_score = overall_score
        rhythm_score = self._calc_rhythm_score(user_angles, angle_standards)
        fluency_score = self._calc_fluency_score(user_angles, angle_standards)

        total_score = (
            accuracy_score * 0.45 +
            rhythm_score * 0.25 +
            fluency_score * 0.30
        )

        return {
            'total_score': round(total_score, 2),
            'accuracy_score': accuracy_score,
            'rhythm_score': rhythm_score,
            'fluency_score': fluency_score,
            'joint_scores': joint_scores,
            'phase_scores': phase_result,
            'analysis': self._generate_analysis(joint_scores, phase_result),
            'improvement_tips': self._generate_improvement_tips(joint_scores, angle_stats)
        }

    def _score_frame_with_standards(self, actual_angle: float, stats: Dict,
                                   target_angle: Optional[float]) -> float:
        """
        根据动态标准计算单帧得分

        评分策略：
        1. 优先使用目标角度曲线（偏差越小越好）
        2. 否则使用 excellent/acceptable 双层标准
        """
        is_kick = stats.get('is_kick', False)

        # 方法1：基于目标曲线评分（优先）
        if target_angle is not None:
            diff = abs(actual_angle - target_angle)
            if diff <= 5:
                return 100.0
            elif diff <= 12:
                return 95.0
            elif diff <= 22:
                return 85.0
            elif diff <= 35:
                return 72.0
            elif diff <= 50:
                return 58.0
            else:
                return max(0, 45 - (diff - 50) * 0.6)

        # 方法2：基于双层标准评分
        excellent_min = stats.get('excellent_min', 0)
        excellent_max = stats.get('excellent_max', 180)
        acceptable_min = stats.get('acceptable_min', 0)
        acceptable_max = stats.get('acceptable_max', 180)

        # 优秀层（得分 90-100）
        if excellent_min <= actual_angle <= excellent_max:
            # 越接近中心越好
            center = (stats.get('mean', 90))
            deviation = abs(actual_angle - center)
            max_dev = max(center - excellent_min, excellent_max - center, 1)
            return max(90, 100 - (deviation / max_dev) * 10)

        # 可接受层（得分 70-89）
        if acceptable_min <= actual_angle <= acceptable_max:
            dev_from_excellent = 0
            if actual_angle < excellent_min:
                dev_from_excellent = excellent_min - actual_angle
            else:
                dev_from_excellent = actual_angle - excellent_max

            return max(70, 89 - dev_from_excellent * 0.5)

        # 超出可接受范围
        if actual_angle < acceptable_min:
            dev = acceptable_min - actual_angle
        else:
            dev = actual_angle - acceptable_max

        if dev <= 10:
            return 55.0
        elif dev <= 20:
            return 42.0
        elif dev <= 35:
            return 30.0
        elif dev <= 50:
            return 18.0
        else:
            return max(0, 12 - (dev - 50) * 0.2)

    def _get_phase_for_frame(self, frame_idx: int, total_frames: int,
                            phase_info: Dict) -> str:
        """确定当前帧所属的动作阶段"""
        phase_names = phase_info.get('phase_names', ['整体'])
        if len(phase_names) == 1:
            return phase_names[0]

        phase_boundaries = phase_info.get('phase_boundaries', [])
        if not phase_boundaries:
            return '发力'  # 默认主体阶段

        for i in range(len(phase_names)):
            if i < len(phase_boundaries) - 1:
                if phase_boundaries[i] <= frame_idx < phase_boundaries[i + 1]:
                    return phase_names[i]
        return phase_names[-1] if phase_names else '整体'

    def _calc_rhythm_score(self, user_angles: Dict[str, List[Optional[float]]],
                          angle_standards: Dict) -> float:
        """计算节奏匹配度"""
        delta_stats = angle_standards.get('delta_stats', {})
        total_score = 0
        count = 0

        for joint_name, user_seq in user_angles.items():
            std_delta = delta_stats.get(joint_name, {}).get('mean_delta', 0)
            if std_delta == 0:
                continue

            # 计算用户视频的角度变化
            valid = [a for a in user_seq if a is not None]
            if len(valid) < 2:
                continue

            user_deltas = [abs(valid[i] - valid[i-1]) for i in range(1, len(valid))]
            user_mean_delta = float(np.mean(user_deltas))

            # 节奏匹配度：用户变化节奏与标准的接近程度
            ratio = user_mean_delta / std_delta if std_delta > 0 else 1.0
            if 0.7 <= ratio <= 1.3:
                score = 100.0
            elif 0.5 <= ratio <= 1.5:
                score = 85.0
            elif 0.3 <= ratio <= 2.0:
                score = 70.0
            else:
                score = max(0, 55.0 - abs(ratio - 1.0) * 20)

            total_score += score
            count += 1

        return round(total_score / count, 2) if count > 0 else 75.0

    def _calc_fluency_score(self, user_angles: Dict[str, List[Optional[float]]],
                           angle_standards: Dict) -> float:
        """计算流畅度得分"""
        total_scores = []

        for joint_name, user_seq in user_angles.items():
            valid = [a for a in user_seq if a is not None]
            if len(valid) < 3:
                continue

            # 计算相邻帧变化是否平滑（变化量是否在合理范围）
            deltas = [abs(valid[i] - valid[i-1]) for i in range(1, len(valid))]
            std_delta = angle_standards.get('delta_stats', {}).get(joint_name, {}).get('max_delta', 30)

            # 流畅帧的比例
            smooth_frames = sum(1 for d in deltas if d <= std_delta * 1.5)
            fluency = (smooth_frames / len(deltas)) * 100 if deltas else 100
            total_scores.append(fluency)

        return round(float(np.mean(total_scores)), 2) if total_scores else 75.0

    def _generate_analysis(self, joint_scores: Dict, phase_scores: Dict) -> str:
        """生成专业综合分析文字"""
        if not joint_scores:
            return "未能检测到有效动作，建议检查视频质量后重新上传。"

        # 按得分排序
        sorted_joints = sorted(joint_scores.items(), key=lambda x: x[1]['mean'])
        weakest = sorted_joints[0] if sorted_joints else (None, None)
        strongest = sorted_joints[-1] if sorted_joints else (None, None)
        avg_score = round(float(np.mean([v['mean'] for _, v in sorted_joints])), 1)

        # 计算得分分布
        excellent = [j for j, v in sorted_joints if v['mean'] >= 85]
        good = [j for j, v in sorted_joints if 70 <= v['mean'] < 85]
        medium = [j for j, v in sorted_joints if 55 <= v['mean'] < 70]
        poor = [j for j, v in sorted_joints if v['mean'] < 55]

        joint_names_cn = {
            'left_elbow': '左臂', 'right_elbow': '右臂',
            'left_shoulder': '左肩', 'right_shoulder': '右肩',
            'left_hip': '左髋', 'right_hip': '右髋',
            'left_knee': '左膝', 'right_knee': '右膝',
            'left_leg_kick': '左腿', 'right_leg_kick': '右腿',
            'trunk': '躯干'
        }

        parts = []

        # 第一段：整体水平定级
        if avg_score >= 90:
            level = "卓越"
            level_desc = "动作标准规范，与标准舞蹈高度吻合，已达到专业水准。"
        elif avg_score >= 80:
            level = "优秀"
            level_desc = "整体动作表现优秀，细节处理到位，具备较好的舞蹈基础。"
        elif avg_score >= 70:
            level = "良好"
            level_desc = "动作框架基本正确，整体协调性良好，部分细节需进一步优化。"
        elif avg_score >= 60:
            level = "一般"
            level_desc = "动作基本可辨认，但与标准存在明显差距，需要针对性强化训练。"
        elif avg_score >= 50:
            level = "较差"
            level_desc = "动作偏差较大，节奏感和姿态控制均有待提升，建议从基础动作开始练习。"
        else:
            level = "较差"
            level_desc = "当前动作与标准舞蹈差距显著，建议加强基础训练后再进行评分。"

        parts.append(f"【综合评价：{level}】（平均得分 {avg_score} 分）{level_desc}")

        # 第二段：各部位表现分析
        if excellent:
            ex_names = '、'.join(joint_names_cn.get(j, j) for j in excellent)
            parts.append(f"✓ {ex_names}等部位动作标准，表现最为突出，与标准吻合度高。")
        if good:
            gd_names = '、'.join(joint_names_cn.get(j, j) for j in good)
            parts.append(f"○ {gd_names}等部位表现良好，能够较好地完成动作要求。")
        if medium:
            md_names = '、'.join(joint_names_cn.get(j, j) for j in medium)
            parts.append(f"△ {md_names}等部位存在一定偏差，需注意调整动作幅度与姿态。")
        if poor:
            pr_names = '、'.join(joint_names_cn.get(j, j) for j in poor)
            parts.append(f"✗ {pr_names}等部位偏差明显，是影响整体评分的主要因素，需要重点训练。")

        # 第三段：最强与最弱对比
        if weakest[0] and weakest[1]:
            w_cn = joint_names_cn.get(weakest[0], weakest[0])
            w_score = weakest[1]['mean']
            parts.append(f"◆ 最薄弱环节：{w_cn}（{w_score}分），建议重点加强该部位的动作练习，可配合拉伸与力量训练提升。")

        if strongest[0] and strongest[1] and strongest[0] != weakest[0]:
            s_cn = joint_names_cn.get(strongest[0], strongest[0])
            s_score = strongest[1]['mean']
            parts.append(f"◆ 最强环节：{s_cn}（{s_score}分），继续保持并发挥该优势。")

        # 第四段：综合训练建议
        if avg_score >= 80:
            parts.append("建议：维持当前训练节奏，适当增加动作难度以进一步提升舞蹈表现力。")
        elif avg_score >= 60:
            parts.append("建议：每日坚持基本功练习，注意动作的准确性与节奏把控，逐步提升整体完成度。")
        else:
            parts.append("建议：从基础动作分解练习开始，注重单个动作的规范性，再逐步串联完整舞蹈。")

        return ' '.join(parts)

    def _generate_improvement_tips(self, joint_scores: Dict, angle_stats: Dict) -> List[Dict]:
        """生成改进建议"""
        tips = []
        joint_names_cn = {
            'left_elbow': '左臂伸直', 'right_elbow': '右臂伸直',
            'left_shoulder': '左肩抬臂', 'right_shoulder': '右肩抬臂',
            'left_hip': '左髋抬腿', 'right_hip': '右髋抬腿',
            'left_knee': '左膝弯曲', 'right_knee': '右膝弯曲',
            'left_leg_kick': '左腿踢腿高度', 'right_leg_kick': '右腿踢腿高度',
            'trunk': '躯干稳定性'
        }

        for joint_name, scores in joint_scores.items():
            if scores['mean'] < 75:
                cn_name = joint_names_cn.get(joint_name, joint_name)
                stats = angle_stats.get(joint_name, {})
                std_mean = stats.get('mean', 0)
                std_range = f"{stats.get('min', 0):.0f}°~{stats.get('max', 0):.0f}°"
                std_min = stats.get('excellent_min', std_mean)
                std_max = stats.get('excellent_max', std_mean)
                is_kick = 'kick' in joint_name

                # 计算当前得分对应的角度与标准角度的差异
                current_angle_estimate = None
                if is_kick:
                    # 踢腿：从分数反推角度 (45° 对应 85 分，90° 对应 100 分)
                    current_angle_estimate = 45 + (scores['mean'] - 85) / 15 * 45
                else:
                    # 普通关节：从分数反推角度 (140° 对应 85 分，180° 对应 100 分)
                    current_angle_estimate = 140 + (scores['mean'] - 85) / 15 * 40

                # 标准中值角度
                std_mid_angle = (std_min + std_max) / 2 if std_min < std_max else std_mean
                angle_diff = abs(current_angle_estimate - std_mid_angle) if current_angle_estimate else None

                if 'kick' in joint_name:
                    tip = f"{cn_name}不够高，建议加强腿部力量和柔韧性训练，标准动作角度范围：{std_range}"
                elif 'elbow' in joint_name or 'knee' in joint_name:
                    tip = f"{cn_name}不够充分，注意充分伸展/弯曲肢体，标准动作角度范围：{std_range}"
                elif 'shoulder' in joint_name:
                    tip = f"{cn_name}幅度不够，建议加强肩部活动范围训练，标准动作角度范围：{std_range}"
                elif 'hip' in joint_name:
                    tip = f"{cn_name}抬腿不够高，注意收紧核心发力抬腿，标准动作角度范围：{std_range}"
                else:
                    tip = f"{cn_name}动作需要改进，标准动作角度范围：{std_range}"

                tips.append({
                    'joint': joint_name,
                    'joint_cn': cn_name,
                    'current_score': scores['mean'],
                    'angle_diff': round(angle_diff, 1) if angle_diff else None,
                    'tip': tip
                })

        return tips[:5]  # 最多返回5条建议

    def _evaluate_with_dtw(self, user_keypoints: List[Optional[List[float]]],
                          standard_keypoints: List[Optional[List[float]]]) -> Dict:
        """使用传统DTW方法评分（当没有动态标准时）"""
        dtw_distance, frame_similarities = self._dynamic_time_warping(user_keypoints, standard_keypoints)

        user_len = len([k for k in user_keypoints if k is not None])
        std_len = len([k for k in standard_keypoints if k is not None])

        accuracy_score = max(0, min(100, 100 - dtw_distance * 3))
        rhythm_score = (min(user_len, std_len) / max(user_len, std_len) * 100) if std_len > 0 else 0
        fluency_score = self._calculate_fluency(user_keypoints)

        total_score = accuracy_score * 0.40 + rhythm_score * 0.20 + fluency_score * 0.40

        return {
            'total_score': round(total_score, 2),
            'accuracy_score': round(accuracy_score, 2),
            'rhythm_score': round(rhythm_score, 2),
            'fluency_score': round(fluency_score, 2),
            'analysis': '基于DTW算法的传统评分',
            'improvement_tips': []
        }

    def _dynamic_time_warping(self, seq1, seq2):
        """DTW算法"""
        seq1_filled = self._fill_missing(seq1)
        seq2_filled = self._fill_missing(seq2)

        n, m = len(seq1_filled), len(seq2_filled)
        dtw_matrix = np.full((n + 1, m + 1), np.inf)
        dtw_matrix[0, 0] = 0

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                sim = self._frame_similarity(seq1_filled[i-1], seq2_filled[j-1])
                cost = 1 - sim
                dtw_matrix[i, j] = cost + min(dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1])

        return dtw_matrix[n, m], []

    def _frame_similarity(self, landmarks1, landmarks2):
        if landmarks1 is None or landmarks2 is None:
            return 0.0
        arr1 = np.array([landmarks1[i] for i in range(len(landmarks1)) if i % 4 != 3])
        arr2 = np.array([landmarks2[i] for i in range(len(landmarks2)) if i % 4 != 3])
        if len(arr1) != len(arr2):
            return 0.0
        dist = np.linalg.norm(arr1 - arr2)
        return max(0, 1 - dist / 3.0)

    def _fill_missing(self, sequence):
        filled = []
        last_valid = None
        for kp in sequence:
            if kp is not None:
                filled.append(kp)
                last_valid = kp
            else:
                filled.append(last_valid if last_valid else [0.5] * 132)
        return filled

    def _calculate_fluency(self, keypoints_sequence):
        valid = [kp for kp in keypoints_sequence if kp is not None]
        if len(valid) < 2:
            return 100.0
        changes = [self._frame_similarity(valid[i-1], valid[i]) for i in range(1, len(valid))]
        return max(0, min(100, float(np.mean(changes)) * 100))

    def get_grade(self, score: float) -> Tuple[str, str]:
        """根据分数获取等级和评语"""
        if score >= 95:
            return 'S', '完美！堪称范本！'
        elif score >= 85:
            return 'A', '优秀！动作非常标准！'
        elif score >= 75:
            return 'B', '良好！继续加油！'
        elif score >= 65:
            return 'C', '合格！还需要多加练习'
        elif score >= 50:
            return 'D', '不合格！建议观看标准动作'
        else:
            return 'E', '差距较大，请认真练习基础动作'


# ============================================================================
# 便捷函数
# ============================================================================

def extract_keypoints_from_video(video_path: str):
    """从视频提取关键点"""
    extractor = PoseKeypointExtractor()
    return extractor.extract_video_keypoints(video_path)


def learn_angle_standards(video_path: str) -> Dict:
    """从标准视频学习动态角度标准"""
    learner = AngleStandardLearner()
    return learner.learn_from_video(video_path)


def evaluate_dance(user_video_path: str, standard_video_path: str,
                   angle_standards: Optional[Dict] = None) -> Dict:
    """评估用户舞蹈"""
    extractor = PoseKeypointExtractor()
    scorer = DanceScorer()

    user_kp, _, _ = extractor.extract_video_keypoints(user_video_path)
    std_kp, _, _ = extractor.extract_video_keypoints(standard_video_path)

    result = scorer.evaluate(user_kp, std_kp, angle_standards)
    grade, comment = scorer.get_grade(result['total_score'])
    result['grade'] = grade
    result['comment'] = comment

    return result
