# views.py
from datetime import timedelta
import uuid

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import localtime,timezone
from django.views.decorators.csrf import csrf_exempt
import cv2
import mediapipe as mp
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from types_of_exercise import TypeOfExercise
from user.models import SysUser
from utils import score_table
import os
import threading
from .models import CalorieRecord, DanceStandard, DanceScore, VideoProcessTask, AnnotatedVideo, AnnotatedFrame
from .dance_evaluation import PoseKeypointExtractor, DanceScorer, AngleStandardLearner, learn_angle_standards, compute_frame_angles
import json
from django.utils import timezone
from django.contrib.auth.models import User

# 定义每种运动的平均 MET 值
MET_VALUES = {
    "push-up": 8.0,
    "pull-up": 8.5,
    "sit-up": 3.8,
    "squat": 5.0,
    "jumping-jack": 8.0,
    "squat-jump": 10.0,
    "jump-rope": 12.0,
    "running": 11.0,
    "plank": 2.3,
    "side-lunge": 3.5,
    "arm-curl": 3.0,
    "shoulder-press": 3.5,
    "burpee": 14.0,
    "high-knee": 8.0
}

# 设定每种运动的默认频率（每分钟次数）
EXERCISE_FREQUENCIES = {
    "push-up": 15,
    "pull-up": 5,
    "sit-up": 20,
    "squat": 12,
    "jumping-jack": 30,
    "squat-jump": 10,
    "jump-rope": 120,
    "running": 1,
    "plank": 1,
    "side-lunge": 15,
    "arm-curl": 15,
    "shoulder-press": 10,
    "burpee": 8,
    "high-knee": 30
}

# ✅ 设定全局变量
is_running = False
lock = threading.Lock()  # 线程锁，防止并发问题

# 计算消耗的卡路里（单位：千卡）
def calculate_calories(weight, exercise_type, counter):
    met_value = MET_VALUES.get(exercise_type)
    frequency = EXERCISE_FREQUENCIES.get(exercise_type)
    if met_value and frequency:
        # 计算运动时间（小时）
        time_in_hours = counter / (frequency * 60)
        # 使用公式计算卡路里消耗
        calories = met_value * weight * time_in_hours
        return round(calories, 2)
    return 0

# ✅ 视频 & 摄像头处理函数
def process_video(source, exercise_type, weight, is_camera=False):
    cap = cv2.VideoCapture(source)  # 加载视频文件 or 摄像头流
    if not cap.isOpened():
        return {"error": "无法打开视频源，请检查摄像头或视频文件路径"}

    cap.set(3, 640)  # 设置宽度
    cap.set(4, 360)  # 设置高度

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    counter = 0  # 动作计数
    status = True  # 动作状态

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # ✅ 处理帧
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                counter, status = TypeOfExercise(landmarks).calculate_exercise(exercise_type, counter, status)
                # ✅ 绘制骨骼点
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # 计算消耗的卡路里
            calories = calculate_calories(weight, exercise_type, counter)

            # ✅ 实时展示计数和卡路里
            score_table(exercise_type, counter, status, calories)

            # ✅ 实时展示画面
            try:
                cv2.imshow("Real-time Pose Detection", frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            except cv2.error:
                # 在无图形界面的环境中忽略展示错误
                pass

    cap.release()
    cv2.destroyAllWindows()
    return counter

# ✅ 视频上传识别接口
@csrf_exempt
@api_view(['POST'])
def upload_video(request):
    if request.method == 'POST':
        if 'video_file' not in request.FILES:
            return JsonResponse({'error': '缺少视频文件'}, status=400)

        video_file = request.FILES.get('video_file')
        exercise_type = request.POST.get('exercise_type')
        weight = float(request.POST.get('weight'))
        user_id = request.POST.get('user_id')  # 获取用户 ID
        print('Received user_id:', user_id)
        print("video_file:", video_file)
        print("exercise_type:", exercise_type)
        print("FILES:", request.FILES)
        print("POST:", request.POST)
        # 此处可以加入保存逻辑或其他处理
        print(f"接收到视频: {video_file.name}, 类型: {exercise_type}, 体重: {weight}, 用户: {user_id}")

        try:
            user = SysUser.objects.get(id=user_id)
            print("[INFO] 找到用户:", user.username)
        except SysUser.DoesNotExist:
            print("[WARN] 用户不存在:", user_id)
            return JsonResponse({'error': '用户不存在'}, status=400)
        try:
            user_id = int(user_id)  # 将 user_id 转换为整数类型
            print('Converted user_id:', user_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid user_id parameter'}, status=400)


        # 🎯 确保 `exercise_type` 不能为空
        if not exercise_type:
            return JsonResponse({'error': '缺少运动类型参数'}, status=400)

        # 🎯 确保 `user_id` 不能为空
        if not user_id:
            return JsonResponse({'error': '缺少用户 ID 参数'}, status=400)




        # 🎯 存储视频文件
        fs = FileSystemStorage(location='media/video/in/test')
        filename = fs.save(video_file.name, video_file)
        video_path = os.path.join(fs.location, filename)

        # 🎯 处理视频
        result = process_video(video_path, exercise_type, weight)
        if isinstance(result, dict) and "error" in result:
            return JsonResponse({'error': result["error"]}, status=500)

        # 计算消耗的卡路里
        calories = calculate_calories(weight, exercise_type, result)



        # 保存卡路里记录到数据库，关联用户信息
        CalorieRecord.objects.create(
            user=user,
            exercise_type=exercise_type,
            weight=weight,
            counter=result,
            calories=calories,
            created_at=timezone.now()
        )

        return JsonResponse({'message': '视频处理完成', 'counter': result, 'calories': calories})

    return JsonResponse({'error': '无效请求'}, status=400)

# ✅ 摄像头实时识别接口
@csrf_exempt
def real_time_detect(request):
    global is_running

    if request.method == 'POST':
        exercise_type = request.POST.get('exercise_type')
        action = request.POST.get('action')  # 获取 action 参数
        weight = float(request.POST.get('weight', 0))
        user_id = request.POST.get('user_id')  # 获取用户 ID

        if action == "stop":
            with lock:
                is_running = False  # 停止检测
            return JsonResponse({'message': '摄像头检测已停止'})

        # 🎯 确保 `exercise_type` 不能为空
        if not exercise_type:
            return JsonResponse({'error': '缺少运动类型参数'}, status=400)

        # 🎯 确保 `user_id` 不能为空
        if not user_id:
            return JsonResponse({'error': '缺少用户 ID 参数'}, status=400)

        try:
            user = SysUser.objects.get(id=user_id)  # 获取用户对象
        except SysUser.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=400)

        result = process_video(0, exercise_type, weight, is_camera=True)
        if isinstance(result, dict) and "error" in result:
            return JsonResponse({'error': result["error"]}, status=500)

        # 计算消耗的卡路里
        calories = calculate_calories(weight, exercise_type, result)

        # 保存卡路里记录到数据库，关联用户信息
        CalorieRecord.objects.create(
            user=user,
            exercise_type=exercise_type,
            weight=weight,
            counter=result,
            calories=calories,
             created_at = timezone.now()
        )

        return JsonResponse({'message': '摄像头实时检测已开启', 'counter': result, 'calories': calories})

    return JsonResponse({'error': '无效请求'}, status=400)

def calorie_record_data(request):
    user_id = request.GET.get('user_id')
    try:
        user_id = int(user_id)  # 将 user_id 转换为整数类型
    except ValueError:
        return JsonResponse({'error': 'Invalid user_id parameter'}, status=400)
    if user_id is None:
        return JsonResponse({'error': 'Missing user_id parameter'}, status=400)
    try:
        # 获取当前月份的第一天和最后一天
        now = timezone.localtime(timezone.now())
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = (now.replace(day=28) + timezone.timedelta(days=4)).replace(day=1, hour=23, minute=59, second=59, microsecond=999999)

        # 查询本月的卡路里记录
        records = CalorieRecord.objects.filter(user_id=user_id, created_at__range=[start_of_month, end_of_month])
        monthly_data = {}
        for record in records:
            date = localtime(record.created_at).strftime('%Y-%m-%d')
            if date not in monthly_data:
                monthly_data[date] = 0
            monthly_data[date] += record.calories

        return JsonResponse(monthly_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============ 舞蹈评分相关接口 ============

from rest_framework.permissions import AllowAny

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_dance_standards(request):
    """获取所有标准舞蹈列表（无需认证）"""
    try:
        dances = DanceStandard.objects.filter(is_active=True).values(
            'id', 'name', 'dance_type', 'difficulty', 'duration',
            'description', 'thumbnail', 'video_path', 'created_at'
        )

        dance_list = []
        for dance in dances:
            dance_dict = dict(dance)
            dance_dict['created_at'] = dance_dict['created_at'].strftime('%Y-%m-%d %H:%M:%S') if dance_dict.get('created_at') else ''
            dance_list.append(dance_dict)

        return JsonResponse({
            'code': 200,
            'message': '获取成功',
            'data': dance_list
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['POST'])
def preprocess_dance(request):
    """预处理标准舞蹈视频（异步，后台处理避免卡住）"""
    try:
        dance_id = request.POST.get('dance_id')

        if not dance_id:
            return JsonResponse({'error': '缺少舞蹈ID'}, status=400)

        dance = DanceStandard.objects.get(id=dance_id)

        if not dance.video_path:
            return JsonResponse({'error': '舞蹈视频路径不存在'}, status=400)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_path = os.path.join(base_dir, dance.video_path)

        if not os.path.exists(video_path):
            return JsonResponse({'error': f'视频文件不存在: {video_path}'}, status=400)

        # 如果已经有预处理数据，直接返回
        if dance.keypoints_data and dance.angle_standards:
            return JsonResponse({
                'code': 200,
                'message': '该舞蹈已预处理完成，无需重复处理',
                'already_done': True,
            })

        # 创建异步任务
        task = VideoProcessTask.objects.create(
            task_type=VideoProcessTask.TYPE_PREPROCESS,
            video_path=video_path,
            dance_id=dance_id,
            status=VideoProcessTask.STATUS_PENDING,
            message='任务已创建，等待处理...'
        )

        # 启动后台线程处理
        thread = threading.Thread(target=_run_preprocess_async, args=(task.id, dance_id))
        thread.daemon = True
        thread.start()

        return JsonResponse({
            'code': 202,
            'message': '预处理任务已启动，请通过task_id轮询结果',
            'task_id': task.id,
        })
    except DanceStandard.DoesNotExist:
        return JsonResponse({'error': '舞蹈不存在'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
def get_task_status(request):
    """查询视频处理任务状态（用于轮询）"""
    task_id = request.GET.get('task_id')
    if not task_id:
        return JsonResponse({'error': '缺少任务ID'}, status=400)
    try:
        task = VideoProcessTask.objects.get(id=task_id)
        result = {
            'task_id': task.id,
            'status': task.status,
            'progress': task.progress,
            'message': task.message or '',
        }
        if task.status == task.STATUS_COMPLETED and task.result_data:
            result['data'] = json.loads(task.result_data)
        elif task.status == task.STATUS_FAILED:
            result['error'] = task.error
        return JsonResponse({'code': 200, 'data': result})
    except VideoProcessTask.DoesNotExist:
        return JsonResponse({'error': '任务不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ===== 异步处理任务函数 =====

def _run_preprocess_async(task_id, dance_id):
    """后台预处理舞蹈视频"""
    try:
        task = VideoProcessTask.objects.get(id=task_id)
        task.update_progress(5, '正在提取关键点...')
        dance = DanceStandard.objects.get(id=dance_id)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_path = os.path.join(base_dir, dance.video_path)

        extractor = PoseKeypointExtractor()
        task.update_progress(30, '正在处理视频关键点...')
        keypoints, duration, frame_count = extractor.extract_video_keypoints(video_path)
        task.update_progress(60, '正在学习角度标准...')

        angle_standards = learn_angle_standards(video_path)
        task.update_progress(80, '正在保存数据...')

        dance.keypoints_data = json.dumps(keypoints)
        dance.angle_standards = json.dumps(angle_standards)
        dance.duration = duration
        dance.fps = frame_count / duration if duration > 0 else 30
        dance.save()

        angle_stats = angle_standards.get('angle_stats', {})
        stats_summary = {}
        joint_names_cn = {
            'left_elbow': '左臂', 'right_elbow': '右臂',
            'left_shoulder': '左肩', 'right_shoulder': '右肩',
            'left_hip': '左髋', 'right_hip': '右髋',
            'left_knee': '左膝', 'right_knee': '右膝',
            'left_leg_kick': '左腿踢腿', 'right_leg_kick': '右腿踢腿',
        }
        for joint, stats in angle_stats.items():
            if stats.get('valid_frames', 0) > 0:
                cn_name = joint_names_cn.get(joint, joint)
                stats_summary[cn_name] = {
                    '范围': f"{stats['min']:.1f}° ~ {stats['max']:.1f}°",
                    '均值': f"{stats['mean']:.1f}°",
                }

        task.complete({
            'frame_count': frame_count,
            'duration': round(duration, 2),
            'valid_frames': len([k for k in keypoints if k is not None]),
            'angle_stats_summary': stats_summary,
        }, message='预处理完成')
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            task = VideoProcessTask.objects.get(id=task_id)
            task.fail(str(e))
        except:
            pass


def _run_evaluate_async(task_id, user_video_path, standard_keypoints, angle_standards, dance_id, user_id):
    """后台评分舞蹈视频"""
    try:
        from .models import DanceStandard
        task = VideoProcessTask.objects.get(id=task_id)
        task.update_progress(10, '正在提取用户视频关键点...')

        extractor = PoseKeypointExtractor()
        user_keypoints, _, _ = extractor.extract_video_keypoints(user_video_path)
        task.update_progress(50, '正在计算评分...')

        scorer = DanceScorer()
        result = scorer.evaluate(user_keypoints, standard_keypoints, angle_standards)
        task.update_progress(80, '正在生成报告...')

        grade, comment = scorer.get_grade(result['total_score'])

        try:
            user_obj = SysUser.objects.get(id=user_id)
            dance_obj = DanceStandard.objects.get(id=dance_id)
        except:
            task.fail('用户或舞蹈不存在')
            return

        # 保存评分记录
        DanceScore.objects.create(
            user=user_obj,
            dance_standard=dance_obj,
            user_video_path=user_video_path,
            total_score=result['total_score'],
            accuracy_score=result['accuracy_score'],
            rhythm_score=result['rhythm_score'],
            fluency_score=result['fluency_score'],
            joint_scores=json.dumps(result.get('joint_scores', {})),
            phase_scores=json.dumps(result.get('phase_scores', {})),
            improvement_tips=json.dumps(result.get('improvement_tips', [])),
            dance_name=dance_obj.name
        )

        joint_names_cn = {
            'left_elbow': '左臂', 'right_elbow': '右臂',
            'left_shoulder': '左肩', 'right_shoulder': '右肩',
            'left_hip': '左髋', 'right_hip': '右髋',
            'left_knee': '左膝', 'right_knee': '右膝',
            'left_leg_kick': '左腿踢腿', 'right_leg_kick': '右腿踢腿',
        }
        result_cn = {
            'dance_name': dance_obj.name,
            'grade': grade,
            'comment': comment,
            'total_score': result['total_score'],
            'accuracy_score': result['accuracy_score'],
            'rhythm_score': result['rhythm_score'],
            'fluency_score': result['fluency_score'],
            'joint_scores': {joint_names_cn.get(k, k): v for k, v in result.get('joint_scores', {}).items()},
        }

        task.complete(result_cn, message='评分完成')
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            task = VideoProcessTask.objects.get(id=task_id)
            task.fail(str(e))
        except:
            pass


@csrf_exempt
@api_view(['POST'])
def dance_evaluate(request):
    """舞蹈评分接口 - 支持异步处理，长视频不再卡住"""
    if request.method != 'POST':
        return JsonResponse({'error': '仅支持POST请求'}, status=405)

    try:
        video_file = request.FILES.get('video_file')
        dance_id = request.POST.get('dance_id')
        user_id = request.POST.get('user_id')

        if not video_file:
            return JsonResponse({'error': '缺少视频文件'}, status=400)
        if not user_id:
            return JsonResponse({'error': '缺少用户ID'}, status=400)
        if not dance_id:
            return JsonResponse({'error': '缺少舞蹈ID'}, status=400)

        try:
            user = SysUser.objects.get(id=user_id)
        except SysUser.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=400)

        dance_standard = DanceStandard.objects.get(id=dance_id)

        # 加载标准舞蹈数据
        standard_keypoints = None
        angle_standards = None

        if dance_standard.keypoints_data:
            standard_keypoints = json.loads(dance_standard.keypoints_data)
        if dance_standard.angle_standards:
            angle_standards = json.loads(dance_standard.angle_standards)

        # 如果标准视频没有预处理，先触发预处理任务（后台异步执行）
        needs_preprocess = not standard_keypoints or not angle_standards
        if needs_preprocess:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            video_path = os.path.join(base_dir, dance_standard.video_path)
            if os.path.exists(video_path):
                preprocess_task = VideoProcessTask.objects.create(
                    task_type=VideoProcessTask.TYPE_PREPROCESS,
                    video_path=video_path,
                    dance_id=dance_id,
                    status=VideoProcessTask.STATUS_PENDING,
                    message='标准视频预处理中...'
                )
                thread = threading.Thread(target=_run_preprocess_async, args=(preprocess_task.id, dance_id))
                thread.daemon = True
                thread.start()

        # 保存用户视频
        fs = FileSystemStorage(location='media/video/dance/user_uploads')
        filename = fs.save(video_file.name, video_file)
        user_video_path = os.path.join(fs.location, filename)

        # 创建异步评分任务
        task = VideoProcessTask.objects.create(
            user=user,
            task_type=VideoProcessTask.TYPE_EVALUATE,
            video_path=user_video_path,
            dance_id=dance_id,
            status=VideoProcessTask.STATUS_PENDING,
            message='评分任务已创建...'
        )

        std_kp = standard_keypoints if standard_keypoints else []
        ang_std = angle_standards if angle_standards else None

        thread = threading.Thread(
            target=_run_evaluate_async,
            args=(task.id, user_video_path, std_kp, ang_std, dance_id, user_id)
        )
        thread.daemon = True
        thread.start()

        return JsonResponse({
            'code': 202,
            'message': '评分任务已启动，请通过task_id轮询结果',
            'task_id': task.id,
        })

    except DanceStandard.DoesNotExist:
        return JsonResponse({'error': '舞蹈不存在'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
def get_dance_scores(request):
    """获取用户的舞蹈评分历史"""
    user_id = request.GET.get('user_id')

    if not user_id:
        return JsonResponse({'error': '缺少用户ID'}, status=400)

    try:
        user_id = int(user_id)
    except ValueError:
        return JsonResponse({'error': '无效的用户ID'}, status=400)

    try:
        scores = DanceScore.objects.filter(user_id=user_id).order_by('-created_at')[:20].values(
            'id', 'dance_name', 'total_score', 'accuracy_score',
            'rhythm_score', 'fluency_score', 'joint_scores', 'created_at'
        )

        score_list = []
        for score in scores:
            score_dict = dict(score)
            score_dict['created_at'] = score_dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')

            # 解析关节评分
            if score_dict.get('joint_scores'):
                try:
                    joint_scores = json.loads(score_dict['joint_scores'])
                    joint_names_cn = {
                        'left_elbow': '左臂', 'right_elbow': '右臂',
                        'left_shoulder': '左肩', 'right_shoulder': '右肩',
                        'left_hip': '左髋', 'right_hip': '右髋',
                        'left_knee': '左膝', 'right_knee': '右膝',
                        'left_leg_kick': '左腿踢腿', 'right_leg_kick': '右腿踢腿',
                    }
                    score_dict['joint_scores_cn'] = {
                        joint_names_cn.get(k, k): v for k, v in joint_scores.items()
                    }
                except:
                    pass

            score_list.append(score_dict)

        return JsonResponse({
            'code': 200,
            'message': '获取成功',
            'data': score_list
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
def get_dance_score_detail(request):
    """获取单条评分详情"""
    score_id = request.GET.get('score_id')

    if not score_id:
        return JsonResponse({'error': '缺少评分ID'}, status=400)

    try:
        score = DanceScore.objects.get(id=score_id)

        result = {
            'id': score.id,
            'dance_name': score.dance_name,
            'total_score': score.total_score,
            'accuracy_score': score.accuracy_score,
            'rhythm_score': score.rhythm_score,
            'fluency_score': score.fluency_score,
            'user_video_path': score.user_video_path,
            'created_at': score.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        # 添加等级
        scorer = DanceScorer()
        grade, comment = scorer.get_grade(score.total_score)
        result['grade'] = grade
        result['comment'] = comment

        return JsonResponse({
            'code': 200,
            'message': '获取成功',
            'data': result
        })
    except DanceScore.DoesNotExist:
        return JsonResponse({'error': '评分记录不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_dance_keypoints(request):
    """
    获取标准舞蹈的关键点序列（用于前端流畅叠加骨架）

    返回格式针对"视频流畅播放 + 骨架精准描绘"优化：
    - 所有帧关键点（不采样），格式紧凑
    - 包含 fps，供前端按时间同步帧索引
    - 无需前端运行任何推理
    """
    dance_id = request.GET.get('dance_id')

    if not dance_id:
        return JsonResponse({'error': '缺少舞蹈ID'}, status=400)

    try:
        dance = DanceStandard.objects.get(id=dance_id)

        # 如果没有预处理过，先预处理（一次性）
        if not dance.keypoints_data or not dance.angle_standards:
            if dance.video_path:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                video_path = os.path.join(base_dir, dance.video_path)

                if os.path.exists(video_path):
                    print(f"[get_dance_keypoints] 正在预处理标准视频: {dance.name}")
                    extractor = PoseKeypointExtractor()
                    keypoints, duration, frame_count = extractor.extract_video_keypoints(video_path)

                    # 学习动态角度标准
                    angle_standards = learn_angle_standards(video_path)

                    dance.keypoints_data = json.dumps(keypoints)
                    dance.angle_standards = json.dumps(angle_standards)
                    dance.duration = duration
                    dance.fps = frame_count / duration if duration > 0 else 30
                    dance.save()
                    print(f"[get_dance_keypoints] 预处理完成: {frame_count}帧, {dance.fps:.1f}fps")
                else:
                    return JsonResponse({'error': '视频文件不存在'}, status=400)
            else:
                return JsonResponse({'error': '舞蹈视频路径不存在'}, status=400)

        # 加载所有帧的关键点（不采样）
        all_keypoints = json.loads(dance.keypoints_data)

        # 加载角度标准
        angle_standards = json.loads(dance.angle_standards)
        angle_stats = angle_standards.get('angle_stats', {})

        # 转换为紧凑格式：[[x,y,z,visibility], ...] 每帧一个数组
        compact_keypoints = []
        for frame_kp in all_keypoints:
            if frame_kp is None:
                compact_keypoints.append(None)
            else:
                # 每4个值一组: x, y, z, visibility -> 转为列表便于JSON
                compact = []
                for i in range(0, len(frame_kp), 4):
                    compact.append([frame_kp[i], frame_kp[i+1], frame_kp[i+2], frame_kp[i+3]])
                compact_keypoints.append(compact)

        # 中文关节角度统计
        joint_names_cn = {
            'left_elbow': '左臂', 'right_elbow': '右臂',
            'left_shoulder': '左肩', 'right_shoulder': '右肩',
            'left_hip': '左髋', 'right_hip': '右髋',
            'left_knee': '左膝', 'right_knee': '右膝',
            'left_leg_kick': '左腿踢腿', 'right_leg_kick': '右腿踢腿',
        }

        stats_cn = {}
        for joint, stats in angle_stats.items():
            if stats.get('valid_frames', 0) > 0:
                stats_cn[joint_names_cn.get(joint, joint)] = {
                    '范围': f"{stats['min']:.1f}° ~ {stats['max']:.1f}°",
                    '均值': f"{stats['mean']:.1f}°",
                    '可接受范围': f"{stats['acceptable_min']:.1f}° ~ {stats['acceptable_max']:.1f}°",
                    '标准差': f"{stats['std']:.1f}°"
                }

        return JsonResponse({
            'code': 200,
            'message': '获取成功',
            # 全部帧关键点（紧凑格式），前端用 currentTime * fps 取帧
            'keyframes': compact_keypoints,
            'total_frames': len(compact_keypoints),
            'fps': dance.fps,
            'duration': dance.duration,
            # 角度标准（供评分参考）
            'angle_stats': stats_cn,
            'phases': angle_standards.get('phase_info', {}).get('phase_names', []),
        })
    except DanceStandard.DoesNotExist:
        return JsonResponse({'error': '舞蹈不存在'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


# ============ 视频关键点标注接口（异步处理） ============

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_video_for_annotation(request):
    """
    上传视频进行关键点标注（完全异步，不卡前端）
    流程：上传视频 → 后台线程逐帧提取关键点 → 前端轮询查看进度/结果
    """
    try:
        video_file = request.FILES.get('video_file')
        if not video_file:
            return JsonResponse({'error': '缺少视频文件'}, status=400)

        # 保存视频（使用 UUID 文件名，避免中文编码问题）
        ext = os.path.splitext(video_file.name)[1].lower() or '.mp4'
        safe_filename = f"{uuid.uuid4().hex}{ext}"
        fs = FileSystemStorage(location='media/video/annotated')
        actual_filename = fs.save(safe_filename, video_file)
        video_path = os.path.join(fs.location, actual_filename)

        # 获取用户ID（可选）
        user_id = request.POST.get('user_id')
        user = None
        if user_id:
            try:
                user = SysUser.objects.get(id=user_id)
            except SysUser.DoesNotExist:
                pass

        # 创建标注记录（actual_filename 是实际保存的文件名，用于构建访问 URL）
        annotation = AnnotatedVideo.objects.create(
            user=user,
            original_filename=actual_filename,
            video_path=video_path,
            status='pending',
            progress=0,
            message='任务已创建，等待处理...'
        )

        # 启动后台线程处理
        thread = threading.Thread(
            target=_run_annotation_async,
            args=(annotation.id,)
        )
        thread.daemon = True
        thread.start()

        return JsonResponse({
            'code': 202,
            'message': '视频上传成功，正在后台处理...',
            'annotation_id': annotation.id,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def _run_annotation_async(annotation_id):
    """后台逐帧提取关键点（每处理完一批帧就刷新进度）"""
    try:
        annotation = AnnotatedVideo.objects.get(id=annotation_id)
        annotation.status = 'processing'
        annotation.save()

        video_path = annotation.video_path
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            annotation.fail('无法打开视频文件')
            return

        # 获取视频基本信息
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0

        annotation.total_frames = total_frames
        annotation.fps = fps
        annotation.duration = duration
        annotation.save(update_fields=['total_frames', 'fps', 'duration', 'status'])

        annotation.update_progress(5, f'正在处理 {total_frames} 帧...')

        # 使用 MediaPipe 提取关键点
        mp_pose = mp.solutions.pose
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1
        ) as pose:
            frame_index = 0
            batch_frames = []  # 批量存储帧对象
            batch_size = 100  # 每处理100帧写入一次数据库
            last_progress_report = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(rgb)
                timestamp = frame_index / fps if fps > 0 else 0

                if results.pose_landmarks:
                    landmarks = []
                    for lm in results.pose_landmarks.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])
                    # 计算本帧各关节角度
                    frame_angles = compute_frame_angles(landmarks)
                    batch_frames.append(AnnotatedFrame(
                        video=annotation,
                        frame_index=frame_index,
                        timestamp=timestamp,
                        landmarks=json.dumps(landmarks),
                        angles=json.dumps(frame_angles),
                        is_valid=True
                    ))
                else:
                    batch_frames.append(AnnotatedFrame(
                        video=annotation,
                        frame_index=frame_index,
                        timestamp=timestamp,
                        landmarks=json.dumps([0.0] * 132),
                        angles=json.dumps({}),
                        is_valid=False
                    ))

                frame_index += 1

                # 每 batch_size 帧写入一次数据库，并更新进度
                if len(batch_frames) >= batch_size:
                    AnnotatedFrame.objects.bulk_create(batch_frames)
                    batch_frames = []
                    # 进度: 5(初始化) -> 85(处理帧), 最后15%给完成阶段
                    current_progress = int(80 * frame_index / total_frames) + 5
                    current_progress = min(85, current_progress)
                    if current_progress > last_progress_report + 5:
                        annotation.update_progress(current_progress, f'已处理 {frame_index}/{total_frames} 帧')
                        last_progress_report = current_progress

            # 处理剩余帧
            if batch_frames:
                AnnotatedFrame.objects.bulk_create(batch_frames)

        cap.release()

        annotation.frame_count = frame_index
        annotation.update_progress(95, '正在保存数据...')
        annotation.complete()
        print(f"[标注完成] {annotation.original_filename}: {frame_index} 帧")

    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            annotation = AnnotatedVideo.objects.get(id=annotation_id)
            annotation.fail(str(e))
        except:
            pass


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_annotation_status(request):
    """查询视频标注进度（前端轮询接口）"""
    annotation_id = request.GET.get('annotation_id')
    if not annotation_id:
        return JsonResponse({'error': '缺少标注ID'}, status=400)

    try:
        annotation = AnnotatedVideo.objects.get(id=annotation_id)
        # 根据 video_path 实际位置决定 media 子路径
        if annotation.video_path:
            video_basename = os.path.basename(annotation.video_path)
            video_path_norm = annotation.video_path.replace('\\', '/')
            if '/combined/' in video_path_norm:
                subdir = 'combined'
            elif '/dance/' in video_path_norm:
                subdir = 'dance/user_uploads'
            else:
                subdir = 'annotated'
            video_url = f'/media/video/{subdir}/{video_basename}'
        else:
            video_url = ''
        result = {
            'annotation_id': annotation.id,
            'status': annotation.status,
            'progress': annotation.progress,
            'message': annotation.message or '',
            'total_frames': annotation.total_frames,
            'frame_count': annotation.frame_count,
            'fps': annotation.fps,
            'duration': annotation.duration,
            'video_url': video_url,
            'original_filename': annotation.original_filename,
        }
        if annotation.status == 'failed':
            result['error'] = annotation.error
        return JsonResponse({'code': 200, 'data': result})
    except AnnotatedVideo.DoesNotExist:
        return JsonResponse({'error': '标注记录不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_annotation_frames(request):
    """
    获取标注帧数据（支持分页，按帧序号范围获取）
    前端用 video.currentTime * fps 取帧索引，再通过此接口批量拉取关键点
    """
    annotation_id = request.GET.get('annotation_id')
    start_frame = request.GET.get('start_frame', 0)
    end_frame = request.GET.get('end_frame')

    if not annotation_id:
        return JsonResponse({'error': '缺少标注ID'}, status=400)

    try:
        annotation = AnnotatedVideo.objects.get(id=annotation_id)

        if annotation.status != 'completed':
            return JsonResponse({
                'error': f'视频尚未处理完成，当前状态: {annotation.status}',
                'progress': annotation.progress
            }, status=400)

        queryset = AnnotatedFrame.objects.filter(
            video=annotation
        ).order_by('frame_index')

        start_frame = int(start_frame)
        end_frame_int = int(end_frame) if end_frame else None
        queryset = queryset.filter(frame_index__gte=start_frame)
        if end_frame_int is not None:
            queryset = queryset.filter(frame_index__lte=end_frame_int)

        frames = []
        for f in queryset:
            angles_data = json.loads(f.angles) if f.angles else {}
            frames.append({
                'frame_index': f.frame_index,
                'timestamp': f.timestamp,
                'landmarks': json.loads(f.landmarks),
                'is_valid': f.is_valid,
                'angles': angles_data,
            })

        return JsonResponse({
            'code': 200,
            'data': {
                'annotation_id': annotation.id,
                'total_frames': annotation.total_frames,
                'fps': annotation.fps,
                'duration': annotation.duration,
                'frames': frames,
            }
        })

    except AnnotatedVideo.DoesNotExist:
        return JsonResponse({'error': '标注记录不存在'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def list_annotations(request):
    """
    获取已完成的标注视频列表（支持分页）
    """
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    user_id = request.GET.get('user_id')

    queryset = AnnotatedVideo.objects.filter(status='completed').order_by('-created_at')

    if user_id:
        queryset = queryset.filter(user_id=user_id)

    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    items = queryset[start:end]

    records = []
    for ann in items:
        # 统计有效帧数
        from django.db.models import Count, Q
        frame_stats = AnnotatedFrame.objects.filter(video=ann).aggregate(
            total=Count('id'),
            valid=Count('id', filter=Q(is_valid=True))
        )
        import os
        # 优先用 video_path 的实际文件名（UUID），避免 original_filename 记录了原始文件名导致 404
        video_basename = os.path.basename(ann.video_path) if ann.video_path else ann.original_filename
        # 根据文件位置决定 media 子路径（统一用正斜杠比较，避免 Windows 反斜杠问题）
        video_path_norm = ann.video_path.replace('\\', '/') if ann.video_path else ''
        subdir = 'annotated'
        if '/combined/' in video_path_norm:
            subdir = 'combined'
        elif '/dance/' in video_path_norm:
            subdir = 'dance/user_uploads'
        records.append({
            'id': ann.id,
            'original_filename': ann.original_filename,
            'video_url': f'/media/video/{subdir}/{video_basename}',
            'video_path_exists': os.path.exists(ann.video_path) if ann.video_path else False,
            'status': ann.status,
            'total_frames': ann.total_frames,
            'fps': ann.fps,
            'duration': ann.duration,
            'valid_frame_count': frame_stats['valid'] or 0,
            'total_frame_count': frame_stats['total'] or 0,
            'created_at': ann.created_at.isoformat() if ann.created_at else None,
        })

    return JsonResponse({
        'code': 200,
        'data': {
            'total': total,
            'page': page,
            'page_size': page_size,
            'items': records,
        }
    })


@csrf_exempt
@api_view(['POST'])
def clear_annotations(request):
    """
    清空所有标注历史记录（连带删除帧数据和视频文件）
    """
    user_id = request.POST.get('user_id')
    try:
        queryset = AnnotatedVideo.objects.all()
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        deleted_count = queryset.count()

        # 删除关联的帧数据
        AnnotatedFrame.objects.filter(video__in=list(queryset)).delete()

        # 删除视频文件
        import os
        for ann in queryset:
            if ann.video_path and os.path.exists(ann.video_path):
                try:
                    os.remove(ann.video_path)
                except Exception:
                    pass

        # 删除标注记录
        queryset.delete()

        return JsonResponse({
            'code': 200,
            'message': f'已清空 {deleted_count} 条标注记录',
            'data': {'deleted_count': deleted_count},
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


# ============ 统一上传接口：标注 + 评分（作为舞蹈评分的底座） ============
# 已移至 combined_views.py 模块，通过 urls.py 导入