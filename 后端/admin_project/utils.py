import os

import mediapipe as mp
import pandas as pd
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

mp_pose = mp.solutions.pose


# ✅ 计算角度
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b  # 向量 BA
    bc = c - b  # 向量 BC
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(cosine))
    return angle


# ✅ 获取单个身体部位坐标
def detection_body_part(landmarks, body_part_name):
    landmark = landmarks[mp_pose.PoseLandmark[body_part_name].value]
    return [landmark.x, landmark.y]


# ✅ 将全部身体部位转换为DataFrame
def detection_body_parts(landmarks):
    body_parts = pd.DataFrame(columns=["body_part", "x", "y"])
    for i, lndmrk in enumerate(mp_pose.PoseLandmark):
        lndmrk = str(lndmrk).split(".")[1]
        cord = detection_body_part(landmarks, lndmrk)
        body_parts.loc[i] = lndmrk, cord[0], cord[1]
    return body_parts

#评分系统
def calculate_score(actual_angle, ideal_range):
    """
    根据用户实际角度计算评分
    :param actual_angle: 实际角度
    :param ideal_range: 标准角度范围 (min, max)
    :return: 评分（0-100），以及改进建议
    """
    min_angle, max_angle = ideal_range
    if min_angle <= actual_angle <= max_angle:
        return 100, "姿势完美，继续保持！"

    deviation = min(abs(actual_angle - min_angle), abs(actual_angle - max_angle))

    if deviation <= 10:
        return 90 - deviation, "轻微偏差，调整幅度稍微小一点 "
    elif deviation <= 20:
        return 80 - (deviation * 2), "角度有较大误差，请注意调整动作！"
    else:
        return max(50 - (deviation * 3), 0), "角度偏差过大，请重新学习标准动作！"

# 简单的卡路里计算函数，假设每个动作消耗 0.1 卡路里
def calculate_calories(counter):
    return counter * 0.1

# ✅ 实时展示计数表
def score_table(exercise, counter, status, calories):
    # 创建黑色背景
    score_table = np.zeros((250, 400, 3), dtype=np.uint8)
    # 将 NumPy 数组转换为 PIL 图像
    img_pil = Image.fromarray(score_table)
    draw = ImageDraw.Draw(img_pil)

    # 加载中文字体，若缺失则回退到系统字体/默认字体
    font = None
    font_search_paths = [
        os.path.join(os.path.dirname(__file__), "simhei.ttf"),
        "simhei.ttf",
        os.path.join("C:\\Windows\\Fonts", "simhei.ttf"),
        os.path.join("/usr/share/fonts/truetype", "simhei.ttf"),
    ]
    for path in font_search_paths:
        if path and os.path.exists(path):
            try:
                font = ImageFont.truetype(path, 20)
                break
            except (OSError, IOError):
                font = None
    if font is None:
        font = ImageFont.load_default()

    draw.text((10, 60), f"运动项目 : {exercise.replace('-', ' ')}", font=font, fill=(182, 158, 128))
    draw.text((10, 110), f"计数 : {str(counter)}", font=font, fill=(182, 158, 128))
    draw.text((10, 160), f"状态 : {str(status)}", font=font, fill=(182, 158, 128))
    draw.text((10, 210), f"消耗卡路里 : {calories:.2f}", font=font, fill=(182, 158, 128))

    # 将 PIL 图像转换回 NumPy 数组
    score_table = np.array(img_pil)

    try:
        cv2.imshow("计分表", score_table)
    except cv2.error:
        # 在无图形界面的环境中忽略展示错误
        pass