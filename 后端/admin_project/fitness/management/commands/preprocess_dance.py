"""
Django 管理命令：预处理标准舞蹈视频，学习动态角度标准

使用方法：
python manage.py preprocess_dance <dance_id>
python manage.py preprocess_dance --all  (预处理所有舞蹈)
python manage.py preprocess_dance --test <视频路径>  (测试指定路径的视频)
"""

import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from fitness.models import DanceStandard, DanceScore
from fitness.dance_evaluation import (
    PoseKeypointExtractor, AngleStandardLearner, learn_angle_standards
)


class Command(BaseCommand):
    help = '预处理标准舞蹈视频，提取关键点和学习动态角度标准'

    def add_arguments(self, parser):
        parser.add_argument('dance_id', nargs='?', type=int, help='舞蹈ID')
        parser.add_argument('--all', action='store_true', help='预处理所有舞蹈')
        parser.add_argument('--test', type=str, help='测试指定路径的视频文件')
        parser.add_argument('--list', action='store_true', help='列出所有标准舞蹈')

    def handle(self, *args, **options):
        # 使用 Django 的 BASE_DIR
        base_dir = getattr(settings, 'BASE_DIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        # 列出所有舞蹈
        if options.get('list'):
            self.stdout.write("\n=== 所有标准舞蹈 ===")
            dances = DanceStandard.objects.filter(is_active=True)
            if not dances:
                self.stdout.write(self.style.WARNING("没有找到启用的标准舞蹈"))
                return
            for d in dances:
                status = "已学习" if d.angle_standards else ("已提取关键点" if d.keypoints_data else "未处理")
                self.stdout.write(f"  [{d.id}] {d.name} ({d.dance_type}) - {status}")
            return

        # 测试视频文件
        if options.get('test'):
            video_path = options['test']
            if not os.path.isabs(video_path):
                video_path = os.path.join(base_dir, video_path)
            self.preprocess_video(video_path, dance_name=os.path.basename(video_path))
            return

        # 预处理所有
        if options.get('all'):
            dances = DanceStandard.objects.filter(is_active=True)
            if not dances:
                raise CommandError("没有找到启用的标准舞蹈")
            self.stdout.write(f"将预处理 {dances.count()} 个标准舞蹈...\n")
            for d in dances:
                if d.video_path:
                    video_path = os.path.join(base_dir, d.video_path)
                    if os.path.exists(video_path):
                        self.stdout.write(f"\n[{d.id}] {d.name}...")
                        self.preprocess_dance(d, video_path)
                    else:
                        self.stdout.write(self.style.WARNING(f"  视频不存在: {video_path}"))
                else:
                    self.stdout.write(self.style.WARNING(f"  [{d.id}] {d.name} - 没有视频路径"))
            self.stdout.write(self.style.SUCCESS("\n全部预处理完成！"))
            return

        # 预处理单个
        dance_id = options.get('dance_id')
        if not dance_id:
            raise CommandError("请指定舞蹈ID，或使用 --all 预处理所有")

        try:
            dance = DanceStandard.objects.get(id=dance_id)
        except DanceStandard.DoesNotExist:
            raise CommandError(f"舞蹈不存在: {dance_id}")

        if not dance.video_path:
            raise CommandError(f"舞蹈没有视频路径: {dance.name}")

        video_path = os.path.join(base_dir, dance.video_path)
        if not os.path.exists(video_path):
            raise CommandError(f"视频文件不存在: {video_path}")

        self.preprocess_dance(dance, video_path)

    def preprocess_dance(self, dance, video_path):
        """预处理单个舞蹈"""
        self.stdout.write(f"  视频: {dance.video_path}")

        # 提取关键点
        self.stdout.write("  正在提取关键点...")
        extractor = PoseKeypointExtractor()
        keypoints, duration, frame_count = extractor.extract_video_keypoints(video_path)
        valid_frames = len([k for k in keypoints if k is not None])
        self.stdout.write(f"  提取完成: {frame_count} 帧, 有效帧: {valid_frames}")

        # 学习动态角度标准
        self.stdout.write("  正在学习动态角度标准...")
        angle_standards = learn_angle_standards(video_path)

        # 保存
        dance.keypoints_data = json.dumps(keypoints)
        dance.angle_standards = json.dumps(angle_standards)
        dance.duration = duration
        dance.fps = frame_count / duration if duration > 0 else 30
        dance.save()

        # 显示结果摘要
        angle_stats = angle_standards.get('angle_stats', {})
        joint_names_cn = {
            'left_elbow': '左臂', 'right_elbow': '右臂',
            'left_shoulder': '左肩', 'right_shoulder': '右肩',
            'left_hip': '左髋', 'right_hip': '右髋',
            'left_knee': '左膝', 'right_knee': '右膝',
            'left_leg_kick': '左腿踢腿', 'right_leg_kick': '右腿踢腿',
        }

        self.stdout.write(f"  关键帧: {len(angle_standards.get('keyframes', []))}")
        self.stdout.write(f"  动作阶段: {angle_standards.get('phase_info', {}).get('phase_names', [])}")
        self.stdout.write("  各关节角度范围:")
        for joint, stats in angle_stats.items():
            if stats.get('valid_frames', 0) > 0:
                cn_name = joint_names_cn.get(joint, joint)
                self.stdout.write(f"    {cn_name}: {stats['min']:.1f}° ~ {stats['max']:.1f}°")

        self.stdout.write(self.style.SUCCESS(f"  ✓ 完成"))

    def preprocess_video(self, video_path, dance_name=None):
        """预处理视频文件（不保存到数据库）"""
        if not os.path.exists(video_path):
            raise CommandError(f"视频文件不存在: {video_path}")

        name = dance_name or os.path.basename(video_path)
        self.stdout.write(f"\n=== 测试视频: {name} ===")
        self.stdout.write(f"  路径: {video_path}")

        # 学习角度标准
        self.stdout.write("  正在分析...")
        angle_standards = learn_angle_standards(video_path)

        # 显示结果
        angle_stats = angle_standards.get('angle_stats', {})
        joint_names_cn = {
            'left_elbow': '左臂', 'right_elbow': '右臂',
            'left_shoulder': '左肩', 'right_shoulder': '右肩',
            'left_hip': '左髋', 'right_hip': '右髋',
            'left_knee': '左膝', 'right_knee': '右膝',
            'left_leg_kick': '左腿踢腿', 'right_leg_kick': '右腿踢腿',
        }

        self.stdout.write(f"\n  视频时长: {angle_standards.get('duration', 0):.1f}秒")
        self.stdout.write(f"  总帧数: {angle_standards.get('total_frames', 0)}")
        self.stdout.write(f"  关键帧: {len(angle_standards.get('keyframes', []))}")
        self.stdout.write(f"  动作阶段: {angle_standards.get('phase_info', {}).get('phase_names', [])}")

        self.stdout.write(f"\n  各关节角度范围:")
        for joint, stats in angle_stats.items():
            if stats.get('valid_frames', 0) > 0:
                cn_name = joint_names_cn.get(joint, joint)
                self.stdout.write(
                    f"    {cn_name}: {stats['min']:.1f}° ~ {stats['max']:.1f}° "
                    f"(均值: {stats['mean']:.1f}°, 可接受: {stats['acceptable_min']:.1f}° ~ {stats['acceptable_max']:.1f}°)"
                )

        # 保存结果
        output_path = video_path + '.angle_standards.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(angle_standards, f, ensure_ascii=False, indent=2)
        self.stdout.write(f"\n  完整结果已保存到: {output_path}")

        self.stdout.write(self.style.SUCCESS(f"\n  ✓ 测试完成"))
