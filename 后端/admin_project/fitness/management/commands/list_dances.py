# management/commands/list_dances.py
# 管理命令：列出所有标准舞蹈
# 用法: python manage.py list_dances

from django.core.management.base import BaseCommand
from fitness.models import DanceStandard


class Command(BaseCommand):
    help = '列出所有标准舞蹈'

    def handle(self, *args, **options):
        dances = DanceStandard.objects.all()

        if not dances:
            self.stdout.write('暂无标准舞蹈')
            return

        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('标准舞蹈列表')
        self.stdout.write('=' * 80)

        for dance in dances:
            status = '已预处理' if dance.keypoints_data else '未预处理'
            stars = '★' * dance.difficulty + '☆' * (5 - dance.difficulty)
            self.stdout.write(
                f'[{dance.id}] {dance.name}'
            )
            self.stdout.write(
                f'    类型: {dance.dance_type} | 难度: {stars} | 状态: {status}'
            )
            self.stdout.write(
                f'    时长: {dance.duration:.1f}秒 | 帧数: {int(dance.duration * dance.fps) if dance.fps else "N/A"}'
            )
            if dance.description:
                self.stdout.write(f'    描述: {dance.description}')
            self.stdout.write('-' * 80)
