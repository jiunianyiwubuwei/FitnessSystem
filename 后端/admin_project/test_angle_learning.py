"""
测试脚本：验证标准视频的角度学习效果
使用方法：python test_angle_learning.py
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_project.settings')

import django
django.setup()

from fitness.dance_evaluation import AngleStandardLearner, learn_angle_standards
from fitness.models import DanceStandard
import json


def test_standard_video():
    """测试标准视频的角度学习"""
    print("=" * 60)
    print("标准视频角度学习测试")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 方法1：直接指定视频路径
    video_path = os.path.join(base_dir, "media", "video", "dance", "standards", "小弹腿.mp4")

    if not os.path.exists(video_path):
        print(f"视频文件不存在: {video_path}")
        # 尝试其他路径
        alt_path = os.path.join(base_dir, "admin_project", "media", "video", "dance", "standards", "小弹腿.mp4")
        if os.path.exists(alt_path):
            video_path = alt_path
            print(f"使用替代路径: {video_path}")
        else:
            # 列出目录内容
            print("\n检查标准视频目录:")
            std_dir = "admin_project/media/video/dance/standards"
            if os.path.exists(std_dir):
                for f in os.listdir(std_dir):
                    print(f"  - {f}")
            else:
                print(f"目录不存在: {std_dir}")
            return

    print(f"\n处理视频: {video_path}")
    print("-" * 60)

    # 学习角度标准
    try:
        result = learn_angle_standards(video_path)

        print("\n【1. 角度统计信息】")
        print("-" * 40)
        angle_stats = result.get('angle_stats', {})
        joint_names_cn = {
            'left_elbow': '左臂(肘)', 'right_elbow': '右臂(肘)',
            'left_shoulder': '左肩', 'right_shoulder': '右肩',
            'left_hip': '左髋', 'right_hip': '右髋',
            'left_knee': '左膝', 'right_knee': '右膝',
            'left_leg_kick': '左腿踢腿', 'right_leg_kick': '右腿踢腿',
        }

        for joint, stats in angle_stats.items():
            if stats.get('valid_frames', 0) > 0:
                cn_name = joint_names_cn.get(joint, joint)
                print(f"\n  {cn_name}:")
                print(f"    角度范围: {stats['min']:.1f}° ~ {stats['max']:.1f}°")
                print(f"    均值: {stats['mean']:.1f}°")
                print(f"    标准差: {stats['std']:.1f}°")
                print(f"    可接受范围: {stats['acceptable_min']:.1f}° ~ {stats['acceptable_max']:.1f}°")
                print(f"    有效帧: {stats['valid_frames']}/{stats['total_frames']}")

        print("\n\n【2. 关键帧信息】")
        print("-" * 40)
        keyframes = result.get('keyframes', [])
        print(f"共提取 {len(keyframes)} 个关键帧")
        for kf in keyframes[:10]:  # 只显示前10个
            cn_name = joint_names_cn.get(kf['joint'], kf['joint'])
            print(f"  第{kf['frame']}帧 | {cn_name} | {kf['angle']:.1f}° | {kf['type']}")

        print("\n\n【3. 动作阶段】")
        print("-" * 40)
        phase_info = result.get('phase_info', {})
        print(f"阶段: {phase_info.get('phase_names', [])}")
        boundaries = phase_info.get('phase_boundaries', [])
        print(f"边界: {boundaries}")
        print(f"总帧数: {result.get('total_frames')}")

        print("\n\n【4. 角度变化速率】")
        print("-" * 40)
        delta_stats = result.get('delta_stats', {})
        for joint, stats in delta_stats.items():
            cn_name = joint_names_cn.get(joint, joint)
            print(f"  {cn_name}: 最大变化 {stats['max_delta']:.2f}°/帧, 平均 {stats['mean_delta']:.2f}°/帧")

        print("\n\n【5. 建议的评分标准范围】")
        print("-" * 40)
        print("基于标准视频自动学习到的角度范围：")
        for joint, stats in angle_stats.items():
            if stats.get('valid_frames', 0) > 0:
                cn_name = joint_names_cn.get(joint, joint)
                print(f"  {cn_name}: 优秀 <{stats['acceptable_max']:.0f}° | 合格 <{stats['acceptable_max'] + 20:.0f}°")

        print("\n" + "=" * 60)
        print("测试完成！")
        print("=" * 60)

        # 保存结果到文件
        output_dir = os.path.join(base_dir, "media", "video", "dance", "standards")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "小弹腿_angle_standards.json")
808        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n完整结果已保存到: {output_path}")

        return result

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_database_standard():
    """测试数据库中的标准舞蹈"""
    print("\n\n" + "=" * 60)
    print("测试数据库中的标准舞蹈")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取第一个标准舞蹈
    try:
        dance = DanceStandard.objects.first()
        if not dance:
            print("数据库中没有标准舞蹈记录")
            return

        print(f"\n舞蹈: {dance.name} ({dance.dance_type})")

        if not dance.video_path:
            print("该舞蹈没有视频路径")
            return

        video_path = os.path.join(base_dir, dance.video_path)

        if not os.path.exists(video_path):
            print(f"视频文件不存在: {video_path}")
            return

        print(f"视频路径: {video_path}")

        # 学习角度标准
        result = learn_angle_standards(video_path)

        # 保存到数据库
        dance.angle_standards = json.dumps(result)
        dance.save()

        print(f"\n角度标准已保存到数据库")
        print(f"各关节角度范围:")
        for joint, stats in result.get('angle_stats', {}).items():
            if stats.get('valid_frames', 0) > 0:
                print(f"  {joint}: {stats['min']:.1f}° ~ {stats['max']:.1f}°")

        return result

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == '__main__':
    # 测试1：直接测试视频文件
    result = test_standard_video()

    # 测试2：如果有数据库记录，也测试一下
    # test_database_standard()
