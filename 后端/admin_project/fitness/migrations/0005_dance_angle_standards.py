# Generated migration for angle_standards field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0004_dancestandard_dancescore'),
    ]

    operations = [
        # DanceStandard: 添加 angle_standards 字段
        migrations.AddField(
            model_name='dancestandard',
            name='angle_standards',
            field=models.TextField(
                blank=True,
                help_text='从标准视频自动学习的关节角度标准，包含每帧目标角度、统计范围、关键帧等',
                null=True,
                verbose_name='动态角度标准JSON'
            ),
        ),
        # DanceScore: 添加关节评分相关字段
        migrations.AddField(
            model_name='dancescore',
            name='improvement_tips',
            field=models.TextField(
                blank=True,
                help_text='针对各关节的改进建议',
                null=True,
                verbose_name='改进建议JSON'
            ),
        ),
        migrations.AddField(
            model_name='dancescore',
            name='joint_scores',
            field=models.TextField(
                blank=True,
                help_text='各关节的详细评分，包含均值、最低分等',
                null=True,
                verbose_name='关节评分详情JSON'
            ),
        ),
        migrations.AddField(
            model_name='dancescore',
            name='phase_scores',
            field=models.TextField(
                blank=True,
                help_text='各动作阶段(起势/发力/收势)的评分',
                null=True,
                verbose_name='阶段评分JSON'
            ),
        ),
    ]
