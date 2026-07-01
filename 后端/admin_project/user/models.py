from django.contrib.auth.hashers import make_password
from django.db import models

# 封装好的数据库类
from django.utils import timezone
from rest_framework import serializers


class SysUser(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100,unique=True,verbose_name="用户名")
    password=models.CharField(max_length=100,verbose_name="密码")
    avatar=models.CharField(max_length=255,null=True,verbose_name="用户头像")
    email=models.CharField(max_length=100,null=True,verbose_name="用户邮箱")
    phonenumber=models.CharField(max_length=11,null=True,verbose_name="手机号码")
    login_date=models.DateField(null=True,verbose_name="最后登录时间")
    status=models.IntegerField(null=False,default=1,verbose_name="账号状态（0正常 1停用）")
    create_time=models.DateField(null=True,verbose_name="创建时间")
    update_time=models.DateField(null=True,verbose_name="更新时间")
    remark=models.CharField(max_length=500,null=True,verbose_name="备注")

    @property
    def is_active(self):
        """兼容 DRF 认证：status=0 表示正常（活跃）"""
        return self.status == 0

    def save(self, *args,** kwargs):
        """自动处理密码哈希和字段默认值"""
        if not self.id:  # 新建用户时处理
            # 密码哈希处理
            if not self.password.startswith('pbkdf2_sha256'):
                self.password = make_password(self.password)
            # 设置默认状态
            if self.status is None:
                self.status = 0
            # 自动设置创建时间
            if not self.create_time:
                self.create_time = timezone.now().date()
        super().save(*args,  ** kwargs)
    class Meta:
        db_table="sys_user"


class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=SysUser
        fields='__all__'
