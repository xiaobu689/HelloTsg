import urllib
from re import split
import requests
import base64
import hashlib
import time
import hmac
import random
import urllib.parse
from common import qianwen_messages

# 配置项
uid = "467300"  # 示例用户ID
salf = "86b34a"  # 示例salf
timestamp = str(int(time.time()))


def log(message):
    print(message)


def encode(string):
    encoded_bytes = base64.b64encode(string.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8').replace('/', '_')
    return encoded_str


def genmac():
    mac = [random.randint(0x00, 0xFF) for _ in range(6)]
    return ':'.join(map(lambda x: f"{x:02X}", mac))


# 用户信息
def getInfo():
    t = timestamp
    macs = genmac()
    mac = requests.utils.quote(macs)
    s = f'brand=OPPO&client=android&deviceInfo=OPPO_PCAM00_2021040100_10&interfaceVersion=v2.8&lat=30.1&lng=114.2&mac={macs}&model=PCAM00&privacyStatus=1&region=天津市&salf={salf}&timestamp={t}&uid={uid}&userId={uid}&version=2.8.4&versionCode=154'
    s_encoded = encode(s)

    key = '1s_vsegymTasdgKxiKvRz5vDlyzmc92A_H6A8zg6I'
    signs = hmac.new(key.encode('utf-8'), s_encoded.encode('utf-8'), hashlib.sha1).hexdigest().upper()
    url = 'http://bbs.zaitianjin.net/zstj/v2.8/index.php'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'bbs.zaitianjin.net',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3'
    }
    data = f'c=User&lng=114.2&privacyStatus=1&sign={signs}&interfaceVersion=v2.8&version=2.8.4&userId={uid}&m=getInfo&mac={mac}&versionCode=154&deviceInfo=OPPO_PCAM00_2021040100_10&uid={uid}&client=android&model=PCAM00&region=%E5%A4%A9%E6%B4%A5%E5%B8%82&salf={salf}&brand=OPPO&lat=30.1&timestamp={t}'

    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    log(response_data)
    if response_data['code'] == 1:
        log(f'当前账户余额: {response_data["data"]["smallChange"]}元 累计获得奖励: {response_data["data"]["profit"]}元 账号ID: {response_data["data"]["uid"]}')
        log(response_data['data']['openid'] if response_data['data'][
            'openid'] else f'{response_data["data"]["nickname"]} 未绑定微信，无法自动提现')
        if float(response_data['data']['smallChange']) >= 10:
            withdrawal()
        else:
            log('当前账户余额不足10元，无法提现！')
    else:
        log(response_data['codemsg'])


# 文章列表
def article_list():
    t = timestamp
    macs = genmac()
    mac = requests.utils.quote(macs)
    s = f'brand=OPPO&client=android&deviceInfo=OPPO_PCAM00_2021040100_10&interfaceVersion=v2.8&lat=30.1&lng=114.2&mac={macs}&model=PCAM00&privacyStatus=1&region=天津市&salf={salf}&timestamp={t}&uid={uid}&userId={uid}&version=2.8.4&versionCode=154'
    s_encoded = encode(s)

    key = '1s_vsegymTasdgKxiKvRz5vDlyzmc92A_H6A8zg6I'
    signs = hmac.new(key.encode('utf-8'), s_encoded.encode('utf-8'), hashlib.sha1).hexdigest().upper()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'bbs.zaitianjin.net',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3'
    }
    data = f'c=Forum&lng=114.2&privacyStatus=1&sign={signs}&interfaceVersion=v2.8&version=2.8.4&userId={uid}&m=getReplyList&mac={mac}&versionCode=154&deviceInfo=OPPO_PCAM00_2021040100_10&uid={uid}&client=android&model=PCAM00&region=%E5%A4%A9%E6%B4%A5%E5%B8%82&salf={salf}&brand=OPPO&lat=30.1&timestamp={t}'
    response = requests.post('http://bbs.zaitianjin.net/zstj/v2.8/index.php', headers=headers, data=data, verify=False)
    if response and response.status_code == 200:
        response_data = response.json()
        log(f'获取文章列表成功，共{len(response_data["data"]["list"])}篇文章')
        return response_data['data']['list']
    else:
        return None


# 评论
def article_comment_create(article):
    comment = ''
    article_title = article['subject']
    article_content = article['message']
    article_pid = article['pid']
    username = urllib.parse.quote('骑狗跨大海')
    article_message = f"【标题】：{article_title}\n【内容】：{article_content}"
    basic_question_desc = '我需要你把自己当成一个本地人对下面的帖子发表感想，希望你的输出只有评论内容，没有别的无关紧要的词语，回复格式是：芝麻开门#你的评论， 评论语气要尽可能生活化、日常化，不要太正式的回答，如果是美食或者美景的内容，可以表达自己想吃或者风景好看的赞美等等，包括但不限于此，字数限制在20-35字之间，下面是我需要你发表评论的文章内容：'
    message = qianwen_messages(basic_question_desc, article_message)
    parts = message.split('#')
    if len(parts) > 1:
        comment = parts[1].strip()
    print(f'🐌预评论内容：【{comment}】, 你没意见我就在{random.randint(5, 10)}s后评论了哈......')
    time.sleep(random.randint(5, 10))

    encoded_comment = urllib.parse.quote(comment)

    t = timestamp
    macs = genmac()
    mac = requests.utils.quote(macs)
    s = f'brand=OPPO&client=android&deviceInfo=OPPO_PCAM00_2021040100_10&interfaceVersion=v2.8&lat=30.1&lng=114.2&mac={macs}&model=PCAM00&privacyStatus=1&region=天津市&salf={salf}&timestamp={t}&uid={uid}&userId={uid}&version=2.8.4&versionCode=154'
    s_encoded = encode(s)
    key = '1s_vsegymTasdgKxiKvRz5vDlyzmc92A_H6A8zg6I'
    signs = hmac.new(key.encode('utf-8'), s_encoded.encode('utf-8'), hashlib.sha1).hexdigest().upper()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'bbs.zaitianjin.net',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3'
    }
    data = f'c=Forum&lng=114.2&privacyStatus=1&sign={signs}&interfaceVersion=v2.8&version=2.8.4&userId={uid}&m=getInfo&mac={mac}&versionCode=154&deviceInfo=OPPO_PCAM00_2021040100_10&uid={uid}&client=android&model=PCAM00&region=%E5%A4%A9%E6%B4%A5%E5%B8%82&salf={salf}&brand=OPPO&lat=30.1&timestamp={t}&pid={article_pid}&message={encoded_comment}&userName={username}'
    url = 'http://bbs.zaitianjin.net/zstj/v2.8/index.php'
    response = requests.post(url, headers=headers, data=data)
    print(response.text)


# 提现
def withdrawal():
    t = timestamp
    macs = genmac()
    mac = requests.utils.quote(macs)
    s = f'brand=OPPO&client=android&deviceInfo=OPPO_PCAM00_2021040100_10&interfaceVersion=v2.8&lat=30.1&lng=114.2&mac={macs}&model=PCAM00&money=10&privacyStatus=1&region=天津市&salf={salf}&timestamp={t}&uid={uid}&userId={uid}&version=2.8.4&versionCode=154'
    s_encoded = encode(s)
    key = '1s_vsegymTasdgKxiKvRz5vDlyzmc92A_H6A8zg6I'
    signs = hmac.new(key.encode('utf-8'), s_encoded.encode('utf-8'), hashlib.sha1).hexdigest().upper()

    url = 'http://bbs.zaitianjin.net/zstj/v2.8/index.php'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'bbs.zaitianjin.net',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3'
    }
    data = f'c=Credit&lng=114.2&privacyStatus=1&sign={signs}&interfaceVersion=v2.8&version=2.8.4&userId={uid}&money=10&m=withdrawal&mac={mac}&versionCode=154&deviceInfo=OPPO_PCAM00_2021040100_10&uid={uid}&client=android&model=PCAM00&region=%E5%A4%A9%E6%B4%A5%E5%B8%82&salf={salf}&brand=OPPO&lat=30.1&timestamp={t}'

    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    log(response_data)
    if response_data['code'] == 1:
        log(response_data['codemsg'].replace('提现', '提现10元'))
    else:
        log(response_data['codemsg'].replace('提现', '提现10元'))


if __name__ == "__main__":
    getInfo()
    list = article_list()
    for i in range(1):
        article = random.choice(list)
        article_comment_create(article)
