from datetime import timezone

from django.shortcuts import render

# Create your views here.
from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user.models import SysUser
from .models import HealthNews,Evaluation,HealthData
from .models import HealthNewsSerializer,EvaluationSerializer,HealthDataSerializer
import json

# 获取健康资讯
@api_view(['GET'])
def get_health_news(request):
    news = HealthNews.objects.all()
    serializer = HealthNewsSerializer(news, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_news_detail(request, pk):
    try:
        news = HealthNews.objects.get(id=pk)
        serializer = HealthNewsSerializer(news)
        return Response(serializer.data)
    except HealthNews.DoesNotExist:
        return Response({"error": "该健康资讯不存在"}, status=404)



# 获取和发布评论
@api_view(['GET', 'POST'])
@csrf_exempt
def comment_list(request, content_id):
    if request.method == 'GET':
        # 查询当前文章的所有评论，包括回复
        comments = Evaluation.objects.select_related('commenter').filter(content_id=content_id).order_by('create_time')

        # 构建评论树
        def build_comment_tree(parent_id=None):
            comment_data = []
            for comment in comments.filter(parent_id=parent_id):
                try:
                    # 尝试获取 commenter 的信息，避免因无效数据导致异常
                    data = EvaluationSerializer(comment).data
                    data['replies'] = build_comment_tree(parent_id=comment.id)
                    comment_data.append(data)
                except Exception as e:
                    # 记录异常信息
                    print(f"Error processing comment {comment.id}: {e}")
            return comment_data

        return Response(build_comment_tree())

    elif request.method == 'POST':
        print("接收到的请求体:", request.data)

        # 强制设置 content_id
        request.data['content_id'] = content_id

        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 返回最新的评论数据
            return Response(serializer.data, status=201)
        print(serializer.errors)  # 打印错误信息方便调试
        return Response(serializer.errors, status=400)


# 健康打卡
def generate_feedback(health_data):
    """根据健康数据生成反馈"""
    if "运动" in health_data:
        return "坚持锻炼有助于保持健康！"
    elif "睡眠不足" in health_data:
        return "建议每天保持 7-8 小时的充足睡眠。"
    return "请保持健康的生活方式！"

# 用户健康打卡接口
@api_view(['POST'])
def health_checkin(request):
    print(request.data)
    user_id = request.data.get('user_id')
    weight = float(request.data.get('weight'))  # 强制转换为 float
    sleep_hours = float(request.data.get('sleep_hours'))  # 强制转换为 float
    exercise_time = int(request.data.get('exercise_time'))  #  强制转换为 int
    exercise_type = request.data.get('exercise_type')  # 获取运动类型

    # 自动生成健康反馈
    feedback = generate_feedback(weight, sleep_hours, exercise_time)
    user = SysUser.objects.get(id=user_id)
    # 🎯 存储健康打卡数据
    HealthData.objects.create(
        user_id=user,
        weight=weight,
        sleep_hours=sleep_hours,
        exercise_time=exercise_time,
        feedback=feedback,
        exercise_type=exercise_type  # 保存运动类型
    )

    return Response({
        'message': '打卡成功 ',
        'feedback': feedback
    })


# 获取用户健康数据接口 (用于 ECharts 图表展示)
@api_view(['GET'])
def get_health_data(request, user_id):
    health_data = HealthData.objects.filter(user_id=user_id).order_by('-create_time')
    serializer = HealthDataSerializer(health_data, many=True)
    return Response(serializer.data)



# 健康反馈生成逻辑
def generate_feedback(weight, sleep_hours, exercise_time):
    if weight > 80:
        return "体重偏高，建议多运动和控制饮食 ️"
    elif sleep_hours < 6:
        return "睡眠不足，请注意调整作息 "
    elif exercise_time < 30:
        return "运动不足，建议每天坚持30分钟以上的有氧运动"
    else:
        return "身体状态良好，继续保持！"

