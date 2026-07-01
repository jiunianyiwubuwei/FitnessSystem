from django.db import models
import json
from user.models import SysUser  # 假设你自定义了用户模型


class DanceStandard(models.Model):
    """标准舞蹈模板"""
    name = models.CharField(max_length=100, verbose_name="舞蹈名称")
    dance_type = models.CharField(max_length=50, verbose_name="舞蹈类型")
    video_path = models.CharField(max_length=255, verbose_name="标准视频路径")
    keypoints_data = models.TextField(verbose_name="关键点序列JSON", blank=True, null=True)
    # 新增：动态角度标准（从标准视频自动学习）
    angle_standards = models.TextField(verbose_name="动态角度标准JSON", blank=True, null=True,
        help_text="从标准视频自动学习的关节角度标准，包含每帧目标角度、统计范围、关键帧等")
    duration = models.FloatField(verbose_name="时长(秒)", default=0)
    difficulty = models.IntegerField(verbose_name="难度等级(1-5)", default=1)
    fps = models.FloatField(verbose_name="视频帧率", default=30)
    description = models.TextField(verbose_name="舞蹈描述", blank=True, null=True)
    thumbnail = models.CharField(max_length=255, verbose_name="封面图路径", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fitness_dance_standard'
        app_label = 'fitness'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.dance_type})"


class DanceScore(models.Model):
    """用户舞蹈评分记录"""
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE, db_column='user_id')
    dance_standard = models.ForeignKey(DanceStandard, on_delete=models.CASCADE, null=True, blank=True)
    user_video_path = models.CharField(max_length=255, verbose_name="用户视频路径", blank=True, null=True)
    total_score = models.FloatField(verbose_name="总分(0-100)", default=0)
    accuracy_score = models.FloatField(verbose_name="准确度得分", default=0)
    rhythm_score = models.FloatField(verbose_name="节奏得分", default=0)
    fluency_score = models.FloatField(verbose_name="流畅度得分", default=0)
    # 新增：详细的关节评分和阶段评分
    joint_scores = models.TextField(verbose_name="关节评分详情JSON", blank=True, null=True,
        help_text="各关节的详细评分，包含均值、最低分等")
    phase_scores = models.TextField(verbose_name="阶段评分JSON", blank=True, null=True,
        help_text="各动作阶段(起势/发力/收势)的评分")
    improvement_tips = models.TextField(verbose_name="改进建议JSON", blank=True, null=True,
        help_text="针对各关节的改进建议")
    frame_similarity = models.TextField(verbose_name="每帧相似度JSON", blank=True, null=True)
    dance_name = models.CharField(max_length=100, verbose_name="舞蹈名称", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitness_dance_score'
        app_label = 'fitness'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.dance_name} - {self.total_score}分"


class CalorieRecord(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE, db_column='user_id')  # 建议字段名为 user
    exercise_type = models.CharField(max_length=50)
    weight = models.FloatField()
    counter = models.IntegerField()
    calories = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitness_calorierecord'
        app_label = 'fitness'

    def __str__(self):
        return f"{self.user.username} - {self.exercise_type} - {self.calories} kcal"


class VideoProcessTask(models.Model):
    """视频处理任务（用于异步处理追踪）"""
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, '等待中'),
        (STATUS_PROCESSING, '处理中'),
        (STATUS_COMPLETED, '已完成'),
        (STATUS_FAILED, '失败'),
    ]

    TYPE_PREPROCESS = 'preprocess'
    TYPE_EVALUATE = 'evaluate'
    TYPE_COMBINED = 'combined'  # 统一上传：标注+评分

    user = models.ForeignKey(SysUser, on_delete=models.CASCADE, db_column='user_id', null=True, blank=True)
    task_type = models.CharField(max_length=20, choices=[
        (TYPE_PREPROCESS, '预处理'),
        (TYPE_EVALUATE, '评分'),
        (TYPE_COMBINED, '标注+评分'),
    ])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    progress = models.IntegerField(default=0, help_text="处理进度 0-100")
    message = models.CharField(max_length=200, blank=True, null=True, help_text="状态消息")
    result_data = models.TextField(blank=True, null=True, help_text="结果JSON")
    error = models.TextField(blank=True, null=True)
    video_path = models.CharField(max_length=255, blank=True, null=True)
    dance_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fitness_video_process_task'
        app_label = 'fitness'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.task_type}] {self.status} - {self.progress}%"

    def update_progress(self, progress, message=''):
        self.progress = progress
        if message:
            self.message = message
        self.save(update_fields=['progress', 'message', 'updated_at'])

    def complete(self, result_data=None, message='处理完成'):
        self.status = self.STATUS_COMPLETED
        self.progress = 100
        self.message = message
        if result_data:
            self.result_data = json.dumps(result_data) if isinstance(result_data, dict) else result_data
        self.save()

    def fail(self, error_msg):
        self.status = self.STATUS_FAILED
        self.error = error_msg
        self.save(update_fields=['status', 'error', 'updated_at'])


class AnnotatedVideo(models.Model):
    """带有关键点标注的视频（异步处理）"""
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE, db_column='user_id', null=True, blank=True)
    original_filename = models.CharField(max_length=255, verbose_name="原始文件名")
    video_path = models.CharField(max_length=255, verbose_name="视频文件路径")
    status = models.CharField(max_length=20, choices=[
        ('pending', '等待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ], default='pending')
    progress = models.IntegerField(default=0, help_text="处理进度 0-100")
    message = models.CharField(max_length=200, blank=True, null=True)
    total_frames = models.IntegerField(default=0, verbose_name="视频总帧数")
    fps = models.FloatField(default=0, verbose_name="视频帧率")
    duration = models.FloatField(default=0, verbose_name="视频时长(秒)")
    frame_count = models.IntegerField(default=0, verbose_name="已处理帧数")
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fitness_annotated_video'
        app_label = 'fitness'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.original_filename} ({self.status})"

    def update_progress(self, progress, message=''):
        self.progress = progress
        if message:
            self.message = message
        self.save(update_fields=['progress', 'message', 'updated_at'])

    def complete(self):
        self.status = 'completed'
        self.progress = 100
        self.message = '处理完成'
        self.save(update_fields=['status', 'progress', 'message', 'frame_count', 'updated_at'])

    def fail(self, error_msg):
        self.status = 'failed'
        self.error = error_msg
        self.save(update_fields=['status', 'error', 'updated_at'])


class AnnotatedFrame(models.Model):
    """单帧关键点标注数据"""
    video = models.ForeignKey(AnnotatedVideo, on_delete=models.CASCADE, related_name='frames')
    frame_index = models.IntegerField(verbose_name="帧序号(从0开始)")
    timestamp = models.FloatField(verbose_name="该帧时间戳(秒)")
    landmarks = models.TextField(verbose_name="33个关键点数据JSON [x,y,z,visibility,...]")
    is_valid = models.BooleanField(default=True, verbose_name="是否有效(检测到人体)")
    # 关节角度数据（key: 关节名, value: 角度值/None）
    angles = models.TextField(verbose_name="关节角度JSON {joint_name: angle}", blank=True, null=True,
        help_text="本帧各关节角度，包含左右肘/肩/髋/膝/踢腿等10个关节的角度值")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fitness_annotated_frame'
        app_label = 'fitness'
        ordering = ['frame_index']
        unique_together = [['video', 'frame_index']]

    def __str__(self):
        return f"{self.video.original_filename} - 帧{self.frame_index}"
