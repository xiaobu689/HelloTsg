import datetime
import json
import os
import random
import re
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


# 随机一句网易云热评
def get_163music_comments():
    comments = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    }
    url = 'https://music.163.com/discover/toplist?id=3778678'  # 热歌榜的url
    response = requests.get(url, headers=headers)
    music_ids = re.findall('<a href="/song\?id=(\d+)"', response.text)
    music_id = random.choice(music_ids)
    get_url = "http://music.163.com/api/v1/resource/comments/R_SO_4_" + music_id + "?limit=0&offset=0"
    response = requests.get(get_url, headers=headers)
    json_dict = json.loads(response.content.decode("utf-8"))
    hotcomments = json_dict["hotComments"]
    for j in hotcomments:
        nickname = j["user"]["nickname"]
        content = j["content"].replace("\n", " ")
        liked = str(j["likedCount"]) + "赞"
        # print(f"{nickname} | {content} | {liked}赞")
        if len(content) >= 60:
            # 定义一个正则表达式模式，用于匹配表情符号
            emoji_pattern = re.compile(
                "["
                "\U0001F600-\U0001F64F"
                "\U0001F300-\U0001F5FF"
                "\U0001F680-\U0001F6FF"
                "\U0001F700-\U0001F77F"
                "\U0001F780-\U0001F7FF"
                "\U0001F800-\U0001F8FF"
                "\U0001F900-\U0001F9FF"
                "\U0001FA00-\U0001FA6F"
                "\U0001FA70-\U0001FAFF"
                "\U00002702-\U000027B0"
                "]+",
                flags=re.UNICODE,
            )
            # 定义一个正则表达式模式，用于匹配特殊字符
            special_char_pattern = re.compile(r'[^\w\s，。！？、‘’“”（）【】《》]+')
            hot_comment = emoji_pattern.sub(r'', content)
            # 使用正则表达式替换特殊字符为空字符串
            clean_text = special_char_pattern.sub('', hot_comment)

            comments.append(clean_text)

    return comments
