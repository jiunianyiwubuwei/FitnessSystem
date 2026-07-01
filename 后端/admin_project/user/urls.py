from django.urls import path
from user.views import jwttest, loginView, RegisterView, SaveView, PwdView, ImageView, AvatarView, SearchView,manage_comments,reset_password,change_user_status,delete_user,admin_status

urlpatterns=[
 path('login/',loginView.as_view(),name='login'),#登录
 path('save/',SaveView.as_view(),name='save'),#用户添加修改
 path('updateUserPwd/', PwdView.as_view(), name='updateUserPwd'),  # 用户添加修改
 path('jwt/',jwttest.as_view(),name='jwt'),#测试jwt
 path('register/',RegisterView.as_view(),name='register'),#注册
 path('uploadImage', ImageView.as_view(), name='uploadImage'),  # 头像上传
 path('updateAvatar', AvatarView.as_view(), name='updateAvatar'),  # 更新头像
 path('search/', SearchView.as_view(), name='search'),  # 用户信息查询
 path('manage_comments/', manage_comments, name='comments'),  # 用户评论管理
 path('status/<int:user_id>/<int:status>/', change_user_status, name='status'),  # 用户状态更新
 path('resetPwd/<int:user_id>/', reset_password, name='密码重置'),  # 用户密码重置
 path('delete/<int:user_id>/', delete_user, name='resetpwd'),  # 用户删除
 path('admin/status/', admin_status, name='index'),  # 管理员首页




]