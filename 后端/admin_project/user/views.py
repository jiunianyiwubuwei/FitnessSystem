import json
import re
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.shortcuts import render
from django.utils import timezone
from  django.views import View
from django.http import  JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings

from admin_project import settings
from menu.models import SysMenu, SysMenuSerializer
from role.models import SysRole, SysUserRole
from user.models import SysUser,SysUserSerializer
# Create your views here.

class loginView(View):

    #构建菜单树
    def buildTreeMenu(self, sysMenuList):
        menu_dict = {menu.id: menu for menu in sysMenuList}
        resultMenuList = []

        for menu in sysMenuList:
            parent_id = menu.parent_id
            if parent_id == 0:
                resultMenuList.append(menu)
            else:
                parent_menu = menu_dict.get(parent_id)
                if parent_menu and not hasattr(parent_menu, 'children'):
                    parent_menu.children = []
                if parent_menu:
                    parent_menu.children.append(menu)

        return resultMenuList


    def post(self,request):
        # 获取传递过来的账户、密码：兼容 query/form/json 三种来源
        username = request.GET.get("username") or request.POST.get("username")
        password = request.GET.get("password") or request.POST.get("password")
        if not username or not password:
            try:
                body_data = json.loads(request.body.decode("utf-8")) if request.body else {}
                username = username or body_data.get("username")
                password = password or body_data.get("password")
            except Exception:
                pass
        """
        测试拿到的值
        print(password)
        print(username)
        """

        try:
            user=SysUser.objects.get(username=username)
            #暂时注释，后面需要恢复
            if user.status == 0:  # 🔥 如果用户被禁用
                return JsonResponse({"code": 403, "error": "该用户已被冻结，无法登录，请联系管理员！"}, status=403)
            if not check_password(password, user.password):
                return JsonResponse({'code': 401, 'info': '密码错误'})



            #后端返回token才能进行连接
            jwt_payload = api_settings.JWT_PAYLOAD_HANDLER
            Encondeing = api_settings.JWT_ENCODE_HANDLER
            test = jwt_payload(user)
            token = Encondeing(test)
            #数据库部分
            rolelist=SysRole.objects.raw("SELECT id,name FROM sys_role WHERE id IN (SELECT role_id FROM sys_user_role WHERE user_id="+str(user.id)+")")
            print(rolelist)
            #获取当前用户的角色
            roles=",".join([role.name for role in rolelist])
            menuSet:set(SysMenu)=set()
            for row in rolelist:
                print(row.id,row.name)
                menuList=SysMenu.objects.raw("SELECT * FROM sys_menu WHERE id IN (SELECT menu_id FROM sys_role_menu WHERE role_id=" + str(row.id) + ")")
                for row2 in menuList:
                    print(row2.id,row2.name)
                    menuSet.add(row2)
            menuList:list[SysMenu]=list(menuSet)#set转list
            sorted_menulist=sorted(menuList)#根据order_num排序
            print(sorted_menulist)
            #构建菜单树
            sysMenuList:list[SysMenu]=self.buildTreeMenu(sorted_menulist)
            print(sysMenuList)
            #序列化返回给前端
            serializerMenuList=list()
            for sysMenu in sysMenuList:
                serializerMenuList.append(SysMenuSerializer(sysMenu).data)
            #调试错误信息，保留
        except ObjectDoesNotExist:
            return JsonResponse({'code': 404, 'info': '用户不存在'})
        except Exception as e:
            print(e)
            return JsonResponse({'code':500, 'info':'账号或密码错误！'})
        except Exception as e:
            print(f"登录异常: {str(e)}")
            return JsonResponse({'code': 500, 'info': '系统错误'})
        #登录成功后，需要展示一些用户信息，返回一个序列化后的数据而不是一个user对象，所以定义了SysUerSerializer序列化方法,再转成json数据
        return JsonResponse({'code':200,'info':'登录成功！','roles':roles,'token':token, 'user':SysUserSerializer(user).data,'menulist':serializerMenuList})




class jwttest(View):
    def get(self,request):
        user=SysUser.objects.get(username='你看看',password='123456')
        jwt_payload=api_settings.JWT_PAYLOAD_HANDLER
        Encondeing=api_settings.JWT_ENCODE_HANDLER
        test=jwt_payload(user)
        token=Encondeing(test)
        return JsonResponse({'code':200,'token':token})



#用户修改信息专用
class SaveView(View):
    def post(self,request):
        try:
            # 解析 JSON 数据
            data = request.GET.dict() if request.GET else json.loads(request.body.decode('utf-8'))
            print("接收到的数据：", data)

            user_id = data.get('id')

            if user_id == -1:  # 添加新用户（如果需要）
                return JsonResponse({'code': 400, 'message': '新增用户功能未实现'}, status=400)
            else:  # ✅ **修改用户信息**
                obj_sysUser = SysUser.objects.get(id=user_id)

                # 只修改前端传递的字段，保持其他字段不变
                obj_sysUser.username = data.get('username', obj_sysUser.username)
                obj_sysUser.email = data.get('email', obj_sysUser.email)
                obj_sysUser.phonenumber = data.get('phonenumber', obj_sysUser.phonenumber)
                obj_sysUser.avatar = data.get('avatar', obj_sysUser.avatar)
                obj_sysUser.status = data.get('status', obj_sysUser.status)
                obj_sysUser.remark = data.get('remark', obj_sysUser.remark)

                obj_sysUser.update_time = datetime.now()  # 更新修改时间
                obj_sysUser.save()

                return JsonResponse({'code': 200, 'message': '修改成功'})

        except SysUser.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '用户不存在'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求格式错误'}, status=400)
        except Exception as e:
            print("❌ 错误详情：", e)
            return JsonResponse({'code': 500, 'message': '服务器内部错误'}, status=500)



#修改密码专用视图
class PwdView(View):
    def post(self, request):
        try:
            # ✅ 解析 JSON 数据
            data = json.loads(request.body.decode('utf-8'))
            print("接收到的数据：", data)

            user_id = data.get('id')
            old_password = data.get('oldPassword')
            new_password = data.get('newPassword')

            # ✅ 查找用户
            obj_user = SysUser.objects.get(id=user_id)

            # ✅ 验证旧密码
            if check_password(old_password, obj_user.password):
                # ✅ 更新为新密码（加密存储）
                obj_user.password = make_password(new_password)
                obj_user.update_time = datetime.now()
                obj_user.save()

                return JsonResponse({'code': 200, 'message': '密码修改成功'})
            else:
                return JsonResponse({'code': 500, 'errorInfo': '原密码错误！'})

        except SysUser.DoesNotExist:
            return JsonResponse({'code': 404, 'errorInfo': '用户不存在！'})
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'errorInfo': '请求格式错误！'})
        except Exception as e:
            print("错误详情：", e)
            return JsonResponse({'code': 500, 'errorInfo': '服务器内部错误'})


#注册专用视图
# views.py（新增注册视图）
class RegisterView(View):
    """
    用户注册接口
    请求示例：
    POST /api/user/register/
    {
        "username": "testuser",
        "password": "test1234",
        "confirmpassword": "test1234",
        "email": "test@example.com",
        "phonenumber": "13812345678"
    }
    """
    required_fields = ['username', 'password', 'confirmPassword', 'email', 'phone']

    def validate_phone(self, phone):
        """严格的中国手机号验证"""
        pattern = r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$'
        return re.match(pattern, phone)

    def post(self, request):
        try:
            data = {
            **request.GET.dict(),
            **request.POST.dict()
            }
            # 字段存在性检查
            if any(data.get(field) in (None, '') for field in self.required_fields):
                return JsonResponse({'code': 400, 'msg': '所有带*字段必须填写'})

            # 字段别名映射
            username = data['username']
            password = data['password']
            confirm_password = data['confirmPassword']
            email = data['email']
            phone = data['phone']

            # 密码一致性验证
            if password != confirm_password:
                return JsonResponse({'code': 400, 'msg': '两次密码输入不一致'})

            # 邮箱格式验证
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'code': 400, 'msg': '邮箱格式无效'})

            # 手机号验证
            if not self.validate_phone(phone):
                return JsonResponse({'code': 400, 'msg': '手机号格式不正确'})

            # 唯一性检查
            if SysUser.objects.filter(username=username).exists():
                return JsonResponse({'code': 400, 'msg': '用户名已被占用'})
            if SysUser.objects.filter(email=email).exists():
                return JsonResponse({'code': 400, 'msg': '邮箱已被注册'})
            if SysUser.objects.filter(phonenumber=phone).exists():
                return JsonResponse({'code': 400, 'msg': '手机号已存在'})

            # 创建用户（使用模型自带的save处理密码哈希）
            user = SysUser(
                username=username,
                password=password,  # 模型save方法会自动哈希
                email=email,
                phonenumber=phone,  # 注意字段名映射
                create_time=timezone.now().date(),
                status=1  # 默认正常状态
            )
            user.save()

            return JsonResponse({
                'code': 200,
                'msg': '注册成功',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })

        except Exception as e:
            print(f"注册异常: {str(e)}")
            return JsonResponse({'code': 500, 'msg': '系统繁忙，请稍后再试'})



#头像上传专用视图
class ImageView(View):
    def post(self, request):
        file = request.FILES.get('avatar')
        print("file:", file)
        if file:
            file_name = file.name
            #截取后缀
            suffixName = file_name[file_name.rfind("."):]
            new_file_name = datetime.now().strftime('%Y%m%d%H%M%S') + suffixName
            file_path = str(settings.MEDIA_ROOT) + "\\userAvatar\\" + new_file_name
            print("file_path:", file_path)
            try:
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                return JsonResponse({'code': 200, 'title': new_file_name})
            except:
                return JsonResponse({'code': 500, 'errorInfo': '上传头像失败'})
#头像更换更新
class AvatarView(View):
    def post(self, request):
        #转字典
        data=request.GET.dict()
        id = data['id']
        avatar = data['avatar']
        obj_user = SysUser.objects.get(id=id)
        obj_user.avatar = avatar
        obj_user.save()
        return JsonResponse({'code': 200})


#用户信息查询专用
class SearchView(View):
    def post(self, request):
        data=request.GET.dict()
        pageNum = data['pageNum']  # 当前页
        pageSize = data['pageSize']  # 每页大小
        query=data['query']#模糊查询参数
        print(pageNum, pageSize)
        userListPage = Paginator(SysUser.objects.filter(username__contains=query), pageSize).page(pageNum)
        print(userListPage)
        obj_users = userListPage.object_list.values()  # 转成字典
        users = list(obj_users)  # 把外层的容器转为List
        total = SysUser.objects.filter(username__contains=query).count()
        return JsonResponse({'code': 200, 'userList': users, 'total': total})

#修改用户状态（启用或者禁用）
def change_user_status(request, user_id, status):
    try:
        user = SysUser.objects.get(id=user_id)
        user.status = status
        user.save()
        return JsonResponse({"code": 200, "message": "状态更新成功"})
    except SysUser.DoesNotExist:
        return JsonResponse({"code": 404, "error": "用户不存在"})


#重置密码
def reset_password(request, user_id):
    try:
        user = SysUser.objects.get(id=user_id)
        user.password = make_password("123456")  # 默认重置密码
        user.save()
        return JsonResponse({"code": 200, "message": "密码已重置为 123456"})
    except SysUser.DoesNotExist:
        return JsonResponse({"code": 404, "error": "用户不存在"})


#删除用户
def delete_user(request, user_id):
    """删除用户"""
    if request.method == "POST":
        user = get_object_or_404(SysUser, id=user_id)

        # 先删除 `SysUserRole` 关联的角色信息
        SysUserRole.objects.filter(user=user).delete()

        # 再删除 `SysUser`
        user.delete()
        return JsonResponse({"code": 200, "message": "用户删除成功"})

    return JsonResponse({"code": 400, "error": "无效请求"}, status=400)


#编辑用户信息
def edit_user(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = SysUser.objects.get(id=user_id)

            user.username = data.get("username", user.username)
            user.email = data.get("email", user.email)
            user.phonenumber = data.get("phonenumber", user.phonenumber)
            user.avatar = data.get("avatar", user.avatar)
            user.remark = data.get("remark", user.remark)
            user.update_time = datetime.now()

            user.save()
            return JsonResponse({"code": 200, "message": "用户信息更新成功"})
        except SysUser.DoesNotExist:
            return JsonResponse({"code": 404, "error": "用户不存在"})


#


#用户评论管理界面
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from healthview.models import Evaluation, HealthNews  # 确保导入你的评论表模型
import json


@csrf_exempt
def manage_comments(request):
    if request.method == 'GET':  # 获取所有评论
        comments = Evaluation.objects.select_related("commenter").all()  # 预加载 `commenter` 数据
        comments_list = [
            {
                "id": comment.id,
                "commenter_id": comment.commenter.id if comment.commenter else None,
                "commenter_name": comment.commenter.username if comment.commenter else "匿名用户",
                "content": comment.content,
                "content_type": comment.content_type,
                "content_id": comment.content_id,
                "parent_id": comment.parent_id,
                "create_time": comment.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for comment in comments
        ]
        return JsonResponse({'code': 200, 'comments': comments_list})

    elif request.method == 'DELETE':  # 删除评论
        try:
            data = json.loads(request.body)
            comment_id = data.get('id')
            comment = get_object_or_404(Evaluation, id=comment_id)
            comment.delete()
            return JsonResponse({'code': 200, 'message': '评论删除成功'})
        except Exception as e:
            return JsonResponse({'code': 500, 'error': str(e)})

#管理员首页结构
def admin_status(request):
    """ 获取管理员首页数据 """
    # **返回用户数据**
    stats = {
        "users": SysUser.objects.count(),
        "newUsers": SysUser.objects.filter(create_time__gte="2025-03-01").count(),
        "articles": HealthNews.objects.count(),  # 这里可以换成动态数据
        "comments": Evaluation.objects.count(),
    }
    return JsonResponse(stats)

#测试接口
def c_hello(request):
    """测试接口，返回简单响应"""
    asker = request.GET.get('asker', 'unknown')
    return JsonResponse({
        'code': 200,
        'message': f'Hello, {asker}!',
        'path': request.path
    })