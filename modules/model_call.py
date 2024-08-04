# qwen_call.py
from dashscope import Generation
from .config import Config
import random
from http import HTTPStatus

from openai import OpenAI

from zhipuai import ZhipuAI

class QwenCall():
    def __init__(self):
        pass
    
    def get_response(self, prompt):
        messages = [{'role': 'system', 'content': '你是一个专业的人工智能助手'},
                    {"role": "user", "content": prompt}]

        response = Generation.call(
            model=Config.QWEN_CHAT_MODEL,
            messages=messages,
            api_key=Config.QWEN_API,
            result_format='message'
        )

        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message['content']
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            return None
        

class DeepseekCall():
    def __init__(self) -> None:
        self.client = OpenAI(api_key=Config.DEEPSEEK_API, base_url="https://api.deepseek.com")
    
    def get_response(self, prompt):
        response = self.client.chat.completions.create(
            model=Config.DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": "你是一个专业的人工智能助手"},
                {"role": "user", "content": prompt},
        ],
            max_tokens=4096,
            temperature=0.7,
            stream=False
        )

        return response.choices[0].message.content
    

class GlmCall():
    def __init__(self) -> None:
        self.client = ZhipuAI(api_key=Config.GLM_API)

    def get_response(self, prompt):
        messages=[{"role": "user", "content": prompt}],
        
        response = self.client.chat.completions.create(
                    model=Config.GLM_MODEL,  # 填写需要调用的模型名称
                    messages=messages,
                    )
        
        return response.choices[0].message.content
