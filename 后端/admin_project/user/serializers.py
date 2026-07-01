# 注册专用序列化器
from rest_framework import serializers
from .models import SysUser
from django.core.validators import RegexValidator
from django.utils import timezone
import hashlib#头像生成专用

class RegisterSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True, source='confirm_password')
    phone = serializers.CharField(
        required=True,
        source='phonenumber',  # 关键映射
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message="手机号格式不正确"
            )
        ],
        error_messages={
            "blank": "手机号不能为空"
        }
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "invalid": "邮箱格式不正确",
            "blank": "邮箱不能为空"
        }
    )

    class Meta:
        model = SysUser
        fields = ['username', 'password', 'confirmPassword', 'email', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        # 密码一致性验证
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({"confirmPassword": "两次输入的密码不一致"})

        # 唯一性验证
        if SysUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "用户名已被注册"})

        if SysUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "邮箱已被注册"})

        if SysUser.objects.filter(phonenumber=attrs['phonenumber']).exists():
            raise serializers.ValidationError({"phonenumber": "手机号已被注册"})

        return attrs

#密码强度验证
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("密码至少需要8个字符")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("密码必须包含数字")
        return value

    def create(self, validated_data):
        # 提取并移除确认密码字段
        validated_data.pop('confirm_password', None)

        # 创建用户对象
        user = SysUser(**validated_data)

        # 使用 Django 的密码加密方法
        user.set_password(validated_data['password'])

        # 设置默认值
        validated_data['status'] = 0  # 账号状态正常
        validated_data['create_time'] = timezone.now()
        validated_data['update_time'] = timezone.now()

        # 自动生成头像
        email_hash = hashlib.md5(validated_data['email'].encode()).hexdigest()
        validated_data['avatar'] = f"https://gravatar.com/avatar/{email_hash}?d=identicon"

        # 创建用户并加密密码
        user = SysUser(**validated_data)
        user.set_password(validated_data['password'])  # 密码加密
        user.save()
        return user