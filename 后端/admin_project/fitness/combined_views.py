# GENERATED - appended to views.py
# ============ 统一上传接口：标注 + 评分（作为舞蹈评分的底座） ============

import uuid
import os
import cv2
import mediapipe as mp
import json
import threading

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from user.models import SysUser
from .models import DanceStandard, DanceScore, VideoProcessTask, AnnotatedVideo, AnnotatedFrame
from .dance_evaluation import PoseKeypointExtractor, DanceScorer, compute_frame_angles

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_video_combined(request):
    """
    统一上传接口：上传视频后自动进行关键点标注，
    标注完成后作为底座驱动舞蹈评分流程。

    流程：上传视频 → 标注线程(提取关键点) → 标注完成 → 触发评分线程

    前端轮询 status 接口，根据 progress 阶段判断：
      progress 0-85:  正在标注...
      progress 88-95:  标注完成，评分启动...
      progress 100:   评分完成，可获取结果
    """
    try:
        video_file = request.FILES.get('video_file')
        dance_id = request.POST.get('dance_id')          # 舞蹈标准ID（可选）
        user_id = request.POST.get('user_id')           # 用户ID（可选）

        if not video_file:
            return JsonResponse({'error': '缺少视频文件'}, status=400)

        # 保存视频文件
        ext = os.path.splitext(video_file.name)[1].lower() or '.mp4'
        safe_filename = f"{uuid.uuid4().hex}{ext}"
        fs = FileSystemStorage(location='media/video/combined')
        actual_filename = fs.save(safe_filename, video_file)
        video_path = os.path.join(fs.location, actual_filename)

        # 获取用户
        user = None
        if user_id:
            try:
                user = SysUser.objects.get(id=user_id)
            except SysUser.DoesNotExist:
                pass

        # 获取舞蹈标准（可选，用于评分）
        dance_standard = None
        if dance_id:
            try:
                dance_standard = DanceStandard.objects.get(id=dance_id)
            except DanceStandard.DoesNotExist:
                pass

        # 加载标准舞蹈数据
        standard_keypoints = None
        angle_standards = None
        if dance_standard:
            if dance_standard.keypoints_data:
                standard_keypoints = json.loads(dance_standard.keypoints_data)
            if dance_standard.angle_standards:
                angle_standards = json.loads(dance_standard.angle_standards)
            # 如果标准视频未预处理，先触发预处理
            if not standard_keypoints or not angle_standards:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                std_video_path = os.path.join(base_dir, dance_standard.video_path)
                if os.path.exists(std_video_path):
                    preprocess_task = VideoProcessTask.objects.create(
                        user=user,
                        task_type=VideoProcessTask.TYPE_PREPROCESS,
                        video_path=std_video_path,
                        dance_id=dance_id,
                        status=VideoProcessTask.STATUS_PENDING,
                        message='标准视频预处理中...'
                    )
                    thread = threading.Thread(target=_run_preprocess_async, args=(preprocess_task.id, dance_id))
                    thread.daemon = True
                    thread.start()

        # 创建标注记录（actual_filename 是 UUID 文件名，用于构建访问 URL）
        annotation = AnnotatedVideo.objects.create(
            user=user,
            original_filename=actual_filename,
            video_path=video_path,
            status='pending',
            progress=0,
            message='任务已创建，等待处理...'
        )

        # 创建统一任务记录（追踪整个流程）
        task = VideoProcessTask.objects.create(
            user=user,
            task_type=VideoProcessTask.TYPE_COMBINED,
            video_path=video_path,
            dance_id=dance_id if dance_id else None,
            status=VideoProcessTask.STATUS_PENDING,
            message='视频上传成功，正在处理...'
        )

        # 启动标注线程（标注完成后自动触发评分）
        thread = threading.Thread(
            target=_run_combined_async,
            args=(
                task.id,
                annotation.id,
                video_path,
                user_id,
                dance_id,
                standard_keypoints if standard_keypoints else [],
                angle_standards,
                actual_filename,
            )
        )
        thread.daemon = True
        thread.start()

        return JsonResponse({
            'code': 202,
            'message': '视频上传成功，正在后台处理标注和评分...',
            'task_id': task.id,
            'annotation_id': annotation.id,
            'has_dance_standard': dance_standard is not None,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def _run_combined_async(
    task_id, annotation_id, video_path,
    user_id, dance_id,
    standard_keypoints, angle_standards,
    original_filename
):
    """
    统一处理线程：先标注 → 标注完成后触发评分

    进度分布：
      0-5:   初始化
      5-85:  标注处理（复用 _run_annotation_async 的逻辑）
      85-88: 标注完成，准备评分
      88-95: 评分处理中
      95-100: 评分完成
    """
    try:
        task = VideoProcessTask.objects.get(id=task_id)
        annotation = AnnotatedVideo.objects.get(id=annotation_id)

        task.status = VideoProcessTask.STATUS_PROCESSING
        task.update_progress(2, '开始处理视频...')

        # ========== 阶段1：标注（0-85%） ==========
        annotation.status = 'processing'
        annotation.save()

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            annotation.fail('无法打开视频文件')
            task.fail('无法打开视频文件')
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0

        annotation.total_frames = total_frames
        annotation.fps = fps
        annotation.duration = duration
        annotation.save(update_fields=['total_frames', 'fps', 'duration', 'status'])

        task.update_progress(5, f'正在标注 {total_frames} 帧...')

        mp_pose = mp.solutions.pose
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1
        ) as pose:
            frame_index = 0
            batch_frames = []
            batch_size = 100
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

                if len(batch_frames) >= batch_size:
                    AnnotatedFrame.objects.bulk_create(batch_frames)
                    batch_frames = []
                    current_progress = int(80 * frame_index / total_frames) + 5
                    current_progress = min(85, current_progress)
                    if current_progress > last_progress_report + 3:
                        annotation.update_progress(current_progress, f'已标注 {frame_index}/{total_frames} 帧')
                        task.update_progress(current_progress, f'正在标注: {frame_index}/{total_frames} 帧')
                        last_progress_report = current_progress

            if batch_frames:
                AnnotatedFrame.objects.bulk_create(batch_frames)

        cap.release()
        annotation.frame_count = frame_index
        annotation.original_filename = original_filename  # 确保 UUID 文件名
        annotation.update_progress(85, '标注完成，准备评分...')

        # ========== 阶段2：评分（88-100%） ==========
        if dance_id and (standard_keypoints or angle_standards):
            task.update_progress(88, '标注完成，正在评分...')

            try:
                extractor = PoseKeypointExtractor()
                user_keypoints, _, _ = extractor.extract_video_keypoints(video_path)

                task.update_progress(92, '正在计算评分...')
                scorer = DanceScorer()
                result = scorer.evaluate(user_keypoints, standard_keypoints, angle_standards)

                task.update_progress(96, '正在生成报告...')
                grade, comment = scorer.get_grade(result['total_score'])

                # 保存评分记录
                try:
                    user_obj = SysUser.objects.get(id=user_id) if user_id else None
                    dance_obj = DanceStandard.objects.get(id=dance_id) if dance_id else None

                    score_record = DanceScore.objects.create(
                        user=user_obj,
                        dance_standard=dance_obj,
                        user_video_path=video_path,
                        total_score=result['total_score'],
                        accuracy_score=result['accuracy_score'],
                        rhythm_score=result['rhythm_score'],
                        fluency_score=result['fluency_score'],
                        joint_scores=json.dumps(result.get('joint_scores', {})),
                        phase_scores=json.dumps(result.get('phase_scores', {})),
                        improvement_tips=json.dumps(result.get('improvement_tips', [])),
                        dance_name=dance_obj.name if dance_obj else '标准舞'
                    )

                    joint_names_cn = {
                        'left_elbow': '左臂', 'right_elbow': '右臂',
                        'left_shoulder': '左肩', 'right_shoulder': '右肩',
                        'left_hip': '左髋', 'right_hip': '右髋',
                        'left_knee': '左膝', 'right_knee': '右膝',
                        'left_leg_kick': '左腿踢腿', 'right_leg_kick': '右腿踢腿',
                    }

                    result_cn = {
                        'annotation_id': annotation.id,
                        'video_url': f'/media/video/combined/{original_filename}',
                        'total_frames': total_frames,
                        'fps': fps,
                        'duration': duration,
                        'dance_name': dance_obj.name if dance_obj else '标准舞',
                        'grade': grade,
                        'comment': comment,
                        'total_score': result['total_score'],
                        'accuracy_score': result['accuracy_score'],
                        'rhythm_score': result['rhythm_score'],
                        'fluency_score': result['fluency_score'],
                        'joint_scores': {joint_names_cn.get(k, k): v for k, v in result.get('joint_scores', {}).items()},
                        'phase_scores': result.get('phase_scores', {}),
                        'improvement_tips': result.get('improvement_tips', []),
                        'score_id': score_record.id,
                    }
                except Exception as save_err:
                    import traceback
                    traceback.print_exc()
                    result_cn = {
                        'annotation_id': annotation.id,
                        'video_url': f'/media/video/combined/{original_filename}',
                        'total_frames': total_frames,
                        'fps': fps,
                        'duration': duration,
                        'dance_name': dance_obj.name if dance_id else '标准舞',
                        'grade': grade,
                        'comment': comment,
                        'total_score': result['total_score'],
                        'accuracy_score': result['accuracy_score'],
                        'rhythm_score': result['rhythm_score'],
                        'fluency_score': result['fluency_score'],
                    }

                task.complete(result_cn, message='标注和评分全部完成')
                annotation.complete()

            except Exception as eval_err:
                import traceback
                traceback.print_exc()
                # 标注成功，但评分失败——仍返回标注结果
                task.complete({
                    'annotation_id': annotation.id,
                    'video_url': f'/media/video/combined/{original_filename}',
                    'total_frames': total_frames,
                    'fps': fps,
                    'duration': duration,
                    'score_status': 'failed',
                    'score_error': str(eval_err),
                }, message='标注完成，评分部分失败')
                annotation.complete()
        else:
            # 没有舞蹈标准，只做标注
            annotation.complete()
            task.complete({
                'annotation_id': annotation.id,
                'video_url': f'/media/video/combined/{original_filename}',
                'total_frames': total_frames,
                'fps': fps,
                'duration': duration,
                'score_status': 'no_standard',
            }, message='标注完成（无舞蹈标准，不进行评分）')

        print(f"[统一处理完成] {original_filename}: {frame_index} 帧")

    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            task = VideoProcessTask.objects.get(id=task_id)
            task.fail(str(e))
        except:
            pass
        try:
            annotation = AnnotatedVideo.objects.get(id=annotation_id)
            annotation.fail(str(e))
        except:
            pass


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_combined_task_status(request):
    """
    查询统一任务的处理状态和结果

    返回结构：
    {
      code: 200,
      data: {
        task_id: int,
        status: 'pending'|'processing'|'completed'|'failed',
        progress: int,           # 0-100
        message: str,
        phase: 'annotation'|'scoring'|'done',
        video_url: str,          # 标注完成后可用
        annotation_id: int,       # 标注ID
        total_frames: int,
        fps: float,
        duration: float,
        // 评分完成后可用
        score: {
          score_id: int,
          dance_name: str,
          grade: str,
          comment: str,
          total_score: float,
          accuracy_score: float,
          rhythm_score: float,
          fluency_score: float,
          joint_scores: {},
          phase_scores: {},
          improvement_tips: [],
        }
      }
    }
    """
    task_id = request.GET.get('task_id')
    if not task_id:
        return JsonResponse({'error': '缺少任务ID'}, status=400)

    try:
        task = VideoProcessTask.objects.get(id=task_id)

        # 基础信息
        result = {
            'task_id': task.id,
            'status': task.status,
            'progress': task.progress,
            'message': task.message or '',
            'task_type': task.task_type,
        }

        # 处理中阶段：从 AnnotatedVideo 获取视频元数据
        if task.video_path:
            video_basename = os.path.basename(task.video_path)
            video_path_norm = task.video_path.replace('\\', '/')
            if '/combined/' in video_path_norm:
                subdir = 'combined'
            elif '/dance/' in video_path_norm:
                subdir = 'dance/user_uploads'
            else:
                subdir = 'annotated'
            result['video_url'] = f'/media/video/{subdir}/{video_basename}'
            # 从 AnnotatedVideo 获取元数据（处理中也能拿到）
            try:
                ann = AnnotatedVideo.objects.filter(video_path=task.video_path).order_by('-id').first()
                if ann:
                    result['annotation_id'] = ann.id
                    if ann.total_frames:
                        result['total_frames'] = ann.total_frames
                    if ann.fps:
                        result['fps'] = round(ann.fps, 2)
                    if ann.duration:
                        result['duration'] = round(ann.duration, 2)
            except Exception:
                pass
            result['phase'] = 'annotation_done' if task.progress >= 85 else 'annotation'
        else:
            result['phase'] = 'annotation'
            result['video_url'] = None

        # 评分阶段
        if task.progress >= 88:
            result['phase'] = 'scoring'
        if task.progress >= 95:
            result['phase'] = 'done'

        # 如果有结果数据（task 完成）
        if task.status == VideoProcessTask.STATUS_COMPLETED and task.result_data:
            try:
                result_data = json.loads(task.result_data) if isinstance(task.result_data, str) else task.result_data
                result['annotation_id'] = result_data.get('annotation_id')
                result['total_frames'] = result_data.get('total_frames')
                result['fps'] = result_data.get('fps')
                result['duration'] = result_data.get('duration')
                result['video_url'] = result_data.get('video_url')
                result['score_status'] = result_data.get('score_status', 'completed')

                # 评分结果
                if result_data.get('score_id') or result_data.get('total_score'):
                    result['score'] = {
                        'score_id': result_data.get('score_id'),
                        'dance_name': result_data.get('dance_name'),
                        'grade': result_data.get('grade'),
                        'comment': result_data.get('comment'),
                        'total_score': result_data.get('total_score'),
                        'accuracy_score': result_data.get('accuracy_score'),
                        'rhythm_score': result_data.get('rhythm_score'),
                        'fluency_score': result_data.get('fluency_score'),
                        'joint_scores': result_data.get('joint_scores', {}),
                        'phase_scores': result_data.get('phase_scores', {}),
                        'improvement_tips': result_data.get('improvement_tips', []),
                    }

                # 如果标注成功但评分失败
                if result_data.get('score_status') == 'failed':
                    result['score_error'] = result_data.get('score_error')

            except Exception:
                pass

        # 失败状态
        if task.status == VideoProcessTask.STATUS_FAILED:
            result['error'] = task.error

        return JsonResponse({'code': 200, 'data': result})

    except VideoProcessTask.DoesNotExist:
        return JsonResponse({'error': '任务不存在'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
def get_combined_score_detail(request):
    """
    获取评分详情（关节评分、阶段评分、改进建议等）
    """
    score_id = request.GET.get('score_id')
    task_id = request.GET.get('task_id')

    try:
        if score_id:
            score = DanceScore.objects.get(id=score_id)
            result = {
                'score_id': score.id,
                'dance_name': score.dance_name,
                'total_score': score.total_score,
                'accuracy_score': score.accuracy_score,
                'rhythm_score': score.rhythm_score,
                'fluency_score': score.fluency_score,
                'joint_scores': json.loads(score.joint_scores) if score.joint_scores else {},
                'phase_scores': json.loads(score.phase_scores) if score.phase_scores else {},
                'improvement_tips': json.loads(score.improvement_tips) if score.improvement_tips else [],
                'frame_similarity': json.loads(score.frame_similarity) if score.frame_similarity else [],
                'created_at': score.created_at.isoformat() if score.created_at else None,
            }
            return JsonResponse({'code': 200, 'data': result})

        elif task_id:
            task = VideoProcessTask.objects.get(id=task_id)
            if task.status != VideoProcessTask.STATUS_COMPLETED or not task.result_data:
                return JsonResponse({'error': '任务未完成或无结果'}, status=400)

            result_data = json.loads(task.result_data) if isinstance(task.result_data, str) else task.result_data
            if not result_data.get('score'):
                return JsonResponse({'error': '无评分结果'}, status=400)

            return JsonResponse({'code': 200, 'data': result_data['score']})

        else:
            return JsonResponse({'error': '缺少 score_id 或 task_id'}, status=400)

    except DanceScore.DoesNotExist:
        return JsonResponse({'error': '评分记录不存在'}, status=404)
    except VideoProcessTask.DoesNotExist:
        return JsonResponse({'error': '任务不存在'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
