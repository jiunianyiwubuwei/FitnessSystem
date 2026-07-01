from django.db import models
from rest_framework import serializers
from user.models import SysUser
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone


# 资讯页
class HealthNews(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.TextField()
    tag_id = models.IntegerField()
    cover = models.CharField(max_length=255)
    reader_ids = models.JSONField()  # ✅ 这里是JSON字段
    is_top = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'news'

    def __str__(self):
        # 原代码中 self.title 有误，改为 self.name
        return self.name


class HealthNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthNews
        fields = ['id', 'name', 'content', 'tag_id', 'cover', 'reader_ids', 'is_top', 'create_time']


# 评论页
class Evaluation(models.Model):
    commenter = models.ForeignKey(SysUser, on_delete=models.CASCADE)  # 评论者
    replier_id = models.IntegerField(null=True, blank=True)  # 被回复者ID（用于二级评论）
    content_type = models.CharField(max_length=50)  # 内容类型
    parent_id = models.IntegerField(null=True, blank=True)  # 父评论ID（如果是回复评论）
    content_id = models.IntegerField()  # 对应的资讯ID
    content = models.TextField()  # 评论内容
    upvote_list = models.JSONField(default=list, blank=True)  # 点赞列表
    create_time = models.DateTimeField(default=now)  # 创建时间

    class Meta:
        db_table = 'evaluations'
        ordering = ['-create_time']  # 按时间倒序排列


class EvaluationSerializer(serializers.ModelSerializer):
    commenter_name = serializers.SerializerMethodField()

    class Meta:
        model = Evaluation
        fields = [
            'id', 'commenter', 'commenter_name', 'content',
            'content_type', 'content_id', 'parent_id', 'create_time'
        ]

    def get_commenter_name(self, obj):
        """确保 `commenter` 存在时获取用户名，否则返回 '匿名用户'"""
        if obj.commenter:
            try:
                # 如果 commenter 存在，尝试获取其用户名
                return obj.commenter.username
            except SysUser.DoesNotExist:
                # 如果 commenter 对应的 SysUser 不存在，返回 '匿名用户'
                return "匿名用户"
        return "匿名用户"  # 如果 commenter 为 None，返回 '匿名用户'


# 健康数据
class HealthData(models.Model):
    id = models.AutoField(primary_key=True)  # 主键ID，自增
    user_id = models.ForeignKey(SysUser, on_delete=models.CASCADE, db_column='user_id')  # 关联用户表
    weight = models.FloatField()  # 体重
    sleep_hours = models.FloatField()  # 睡眠时长
    exercise_time = models.IntegerField()  # 运动时长
    feedback = models.CharField(max_length=200)
    exercise_type = models.CharField(max_length=100, blank=True, null=True)  # 新增运动类型字段
    create_time = models.DateTimeField(auto_now_add=True)  # 打卡时间

    class Meta:
        db_table = 'health_data'  # 数据表名
        app_label = 'healthview'

    def __str__(self):
        return f"HealthData for {self.user_id}"


class HealthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthData
        fields = '__all__'

