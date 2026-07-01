from django.urls import path
from .views import get_health_news,get_health_data,comment_list,get_news_detail,health_checkin
urlpatterns=[
    path('news/<int:content_id>/comments/', comment_list, name='news_comments'),
    path('news/<int:pk>/', get_news_detail, name='news'),  # 详情页
    path('news/', get_health_news, name='news'),  #获取健康咨询
    path('checkin/', health_checkin, name='checkin'),  #健康打卡
    path('data/<int:user_id>/', get_health_data, name='checkin'),  #获取健康数据
    path('health/data/',get_health_data, name='data'),  #获取健康资讯



]
