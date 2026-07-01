"""
URL configuration for admin_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # 导入 include 函数
from django.conf import settings
from django.conf.urls.static import static
from user.views import c_hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('fitness.urls')),
    path('menu/', include('menu.urls')),
    path('user/', include('user.urls')),
    path('role/', include('role.urls')),
    path('api2/',include('health_assistant.urls')),
    path('health/', include('healthview.urls')),
    path('c_hello', c_hello, name='c_hello'),  # 测试接口
]

# 在开发模式下提供媒体文件的服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)