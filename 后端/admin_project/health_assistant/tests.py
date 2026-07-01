import requests
from django.test import TestCase

# Create your tests here.
# consult/views.py 中添加测试代码
from manage import main


def test_ollama():
    test_prompt = "如何预防感冒？"
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "deepseek-r1",
            "prompt": test_prompt,
            "stream": False
        }
    )
    print(response.json())

