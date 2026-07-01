from django.urls import path
from health_assistant.views import consult_view

urlpatterns=[
    path('GetAdvice/', consult_view, name='r1'),  # 健康助手
]