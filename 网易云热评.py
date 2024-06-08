import random
import re
import requests
from bs4 import BeautifulSoup
import json
from csv import writer
import time


def get_hot_comments():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    }
    url = 'https://music.163.com/discover/toplist?id=3778678'  # 热歌榜的url
    response = requests.get(url, headers=headers)
    # 使用正则表达式找到所有歌曲的ID
    music_ids = re.findall('<a href="/song\?id=(\d+)"', response.text)
    # 打印歌曲ID列表
    print(music_ids)
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
        if len(content) >= 70:
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

            return clean_text


if __name__ == '__main__':
    comment = get_hot_comments()
