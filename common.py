import datetime
import os
import random
import time
from http import HTTPStatus
import dashscope
import requests


# 通义千问API
def qianwen_messages(basic_question, question):
    content = ''
    qw_key = os.getenv("QIANWEN_KEY")
    qw_key = 'sk-e5fbefa9dc2544d697505ed118359d73'
    if not qw_key:
        print(f'⛔️未获取到通义千问key：请检查变量 {qw_key} 是否填写')
    else:
        dashscope.api_key = qw_key
        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': basic_question + question}]
        response = dashscope.Generation.call(
            dashscope.Generation.Models.qwen_turbo,
            messages=messages,
            seed=random.randint(1, 10000),
            result_format='message',
        )
        if response.status_code == HTTPStatus.OK:
            content = response['output']['choices'][0]['message']['content']
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    return content


def make_request(url, json_data=None, method='get', headers=None):
    try:
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, verify=False)
        else:
            response = requests.post(url, headers=headers, json=json_data, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # 这里可以处理错误，例如记录日志或设置全局变量
        print(f"请求错误: {e}")
        return None


def get_current_timestamp_milliseconds():
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 将当前时间转换为时间戳（秒级）
    timestamp_seconds = int(time.mktime(current_time.timetuple()))
    # 将秒级时间戳转换为毫秒级
    timestamp_milliseconds = timestamp_seconds * 1000 + current_time.microsecond // 1000
    return timestamp_milliseconds


def daily_one_word():
    try:
        urls = [
            "https://api.xygeng.cn/openapi/one",
            "https://v1.hitokoto.cn",
        ]
        url = random.choice(urls)
        response = requests.get(url)
        if response and response.status_code == 200:
            response_json = response.json()
            if url == "https://api.xygeng.cn/openapi/one":
                return response_json['data']['content']
            elif url == "https://v1.hitokoto.cn":
                return response_json['hitokoto']
            else:
                return None
        else:
            # print(f"Error: Received status code {response.status_code}")
            return None
    except requests.RequestException as e:
        # print("Error fetching the daily one word:", e)
        return None