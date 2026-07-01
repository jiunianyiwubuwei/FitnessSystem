from django.urls import path
from fitness.views import (
    upload_video, real_time_detect, calorie_record_data,
    get_dance_standards, preprocess_dance, dance_evaluate,
    get_dance_scores, get_dance_score_detail, get_dance_keypoints,
    get_task_status,
    upload_video_for_annotation, get_annotation_status, get_annotation_frames,
    list_annotations, clear_annotations,
)
from fitness.combined_views import (
    upload_video_combined,
    get_combined_task_status,
    get_combined_score_detail,
)

urlpatterns = [
    # 健身动作识别
    path('upload/', upload_video, name='upload_video'),
    path('real_time/', real_time_detect, name='upload_video'),
    path('calorie-record/', calorie_record_data, name='calorie_record'),

    # 舞蹈评分
    path('dance/standards/', get_dance_standards, name='dance_standards'),
    path('dance/preprocess/', preprocess_dance, name='dance_preprocess'),
    path('dance/evaluate/', dance_evaluate, name='dance_evaluate'),
    path('dance/scores/', get_dance_scores, name='dance_scores'),
    path('dance/score/detail/', get_dance_score_detail, name='dance_score_detail'),
    path('dance/keypoints/', get_dance_keypoints, name='dance_keypoints'),
    path('dance/task/status/', get_task_status, name='dance_task_status'),

    # 视频关键点标注（异步）
    path('annotation/upload/', upload_video_for_annotation, name='annotation_upload'),
    path('annotation/status/', get_annotation_status, name='annotation_status'),
    path('annotation/frames/', get_annotation_frames, name='annotation_frames'),
    path('annotation/list/', list_annotations, name='annotation_list'),
    path('annotation/clear/', clear_annotations, name='annotation_clear'),

    # 统一上传接口：标注 + 评分（舞蹈评分底座）
    path('combined/upload/', upload_video_combined, name='combined_upload'),
    path('combined/status/', get_combined_task_status, name='combined_status'),
    path('combined/score/detail/', get_combined_score_detail, name='combined_score_detail'),
]