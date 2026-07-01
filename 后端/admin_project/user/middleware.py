from django.http import HttpResponse, JsonResponse
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings
from user.models import SysUser  # 你的用户模型


class JwtAuthenticationMiddleware:
    """
    Django 4.2+ 标准中间件写法（不使用已弃用的 MiddlewareMixin）。
    直接实现 __call__，在 process_request 阶段完成 JWT 验证。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        # 预检请求直接放行，避免 CORS 失败
        if request.method == "OPTIONS":
            return HttpResponse(status=200)

        white_list = [
            "/user/login/", "/user/register/", "/api2/GetAdvice/",
            "/health/news/", "/health/data/", "/health/checkin/",
            "/api/upload/", "/api/real_time/", "/api/calorie-record/",
            "/api/dance/standards/", "/api/dance/scores/", "/api/dance/evaluate/", "/api/dance/keypoints/",
            "/api/annotation/upload/", "/api/annotation/status/", "/api/annotation/frames/", "/api/annotation/list/",
            "/c_hello"  # 测试接口，免验证
        ]  # 免验证接口

        path = request.path
        print(f"当前请求路径: {path}")

        if not any(path.startswith(white_path) for white_path in white_list) and not path.startswith("/media"):
            print("需要进行 Token 验证")
            token = request.META.get('HTTP_AUTHORIZATION')
            print("请求头 Authorization:", token)

            if not token:
                return HttpResponse("缺少 Token，请登录！", status=401)

            try:
                # ✅ 去除 `Bearer` 前缀
                token = token.replace("Bearer ", "")
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                payload = jwt_decode_handler(token)

                print("解码后的 Token Payload:", payload)

                # 获取用户 ID**
                user_id = payload.get("user_id")
                user = SysUser.objects.filter(id=user_id).first()

                if user:
                    request.user = user  # ✅ 确保 `request.user` 是 SysUser 对象**
                else:
                    print("用户不存在")
                    request.user = payload  # 兼容 `request.user` 作为字典
                    return JsonResponse({"error": "用户不存在，请重新登录"}, status=401)

            except ExpiredSignatureError:
                return HttpResponse("Token 过期，请重新登录！", status=401)
            except (InvalidTokenError, PyJWTError):
                return HttpResponse("Token 无效！", status=401)

        else:
            print(" 该接口不需要 Token 验证")
            return None
