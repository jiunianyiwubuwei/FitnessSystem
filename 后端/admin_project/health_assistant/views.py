import json
from datetime import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
import requests
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
 #调用r1模型
def get_health_advice(question):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:8b",
                "prompt": f"你是一个健康顾问，请回答：{question}",
                "stream": True  # 开启流式传输
            },
            stream=True
        )

        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                full_response += chunk.get("response", "")
                # 如果需要实时推送可以在这里处理（需要WebSocket）

        return full_response

    except Exception as e:
        return f"模型调用异常：{str(e)}"


#r1模型回复问题
@csrf_exempt
def consult_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()

            if not question:
                return JsonResponse({"status": "error", "message": "问题不能为空"})

            if len(question) > 500:
                return JsonResponse({"status": "error", "message": "问题过长"})

            # 调用模型
            start_time = timezone.now()
            answer = get_health_advice(question)

            # 修正时间计算
            time_difference = timezone.now() - start_time
            process_time = round(time_difference.total_seconds(), 2)  # 关键修复点

            # 清理换行符
            answer = answer.replace("\n", "<br>").strip()

            return JsonResponse({
                "status": "success",
                "answer": answer,
                "process_time": process_time  # 现在返回的是秒数
            })

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "无效的JSON格式"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"服务器错误：{str(e)}"})
    return JsonResponse({"status": "error", "message": "仅支持POST请求"})