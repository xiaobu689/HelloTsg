import hashlib
import random

import requests
import time
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import qianwen_messages, make_request
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
timestamp = str(int(time.time() * 1000))


def generate_random_string_and_timestamp():
    T = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=8))
    d = str(int(time.time() * 1000))
    return T, d


def sha256_encrypt(data):
    hash_object = hashlib.sha256()
    hash_object.update(data.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


def get_header(url1):
    T, d = generate_random_string_and_timestamp()
    message = url1.replace("https://koplus.icoke.cn/cre-bff", "")
    encrypted_data = sha256_encrypt(message + d + "apyuc3#7%m4*")
    headers = {
        "x-sg-id": T,
        "x-sg-timestamp": d,
        "x-sg-signature": encrypted_data
    }
    headers = {
        'Host': 'koplus.icoke.cn',
        'Connection': 'keep-alive',
        'x-sg-timestamp': timestamp,
        'content-type': 'application/json',
        'Authorization': 'MP c5ce060c32d04e4cb410fb1fc9c1e3af',
        'SV': '5',
        'x-sg-signature': '5dd59fe87917ac8bf15a044f577e06292b9bf7d096fc4b553d9cd7ff0faed1d3',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003132) NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxa5811e0426a94686/388/page-frame.html',
    }
    print("headers:", headers)

    return T, d, encrypted_data


def points_list():
    url = 'https://koplus.icoke.cn/cre-bff/wechat/point'
    T, d, encrypted_data = get_header(url)
    headers = {
        'authority': 'koplus.icoke.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': 'MP b4fa2809c39c46b0b86528821c6853e4',
        'content-type': 'application/json',
        'referer': 'https://servicewechat.com/wxa5811e0426a94686/388/page-frame.html',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sv': '10',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
        'x-sg-signature': '454899d991f1b1729ff70808042b538c1b39ae3feecb9a4783d74b46b20a46a5',
        'x-sg-timestamp': '1717684599770',
        'xweb_xhr': '1',
    }

    response = requests.get(url, headers=headers)
    print("----------------我的积分points=", response.text)

def lottery():
    import requests
    headers = {
        'Host': 'koplus.icoke.cn',
        'Connection': 'keep-alive',
        'x-sg-timestamp': '1717685383834',
        'content-type': 'application/json',
        'Authorization': 'MP d9e030641ccb48afa39e3dffee515a29',
        'SV': '10',
        # 'x-sg-signature': '65b2f2ab1649d6d9949ab5dfa3af2ed1cbf59f883e13e5efe79232ea17c8157',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003133) NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxa5811e0426a94686/388/page-frame.html',
    }

    json_data = {
        'pincode': 'http://i.icoke.cn/G/4HPRSZUK708A4RZE',
        'isAuthLbs': True,
        'latitude': 31.184051649305555,
        'longitude': 121.55045464409723,
        'accuracy': 22.371676585191583,
        'altitude': 21.546748170629144,
        'speed': 0,
    }
    url = 'https://koplus.icoke.cn/cre-bff/wechat/user/lotteries/G/scan-draw'
    response = requests.post(url, headers=headers, json=json_data)
    print(response.text)

def userinfo():
    import requests
    headers = {
        'authority': 'koplus.icoke.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': 'MP d9e030641ccb48afa39e3dffee515a29',
        # 'content-type': 'application/json',
        'referer': 'https://servicewechat.com/wxa5811e0426a94686/388/page-frame.html',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sv': '10',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
        'x-sg-signature': '454899d991f1b1729ff70808042b538c1b39ae3feecb9a4783d74b46b20a46a5',
        'x-sg-timestamp': '1717684599776',
        'xweb_xhr': '1',
    }
    response = requests.get('https://koplus.icoke.cn/cre-bff/wechat/profile', headers=headers)
    print(response.text)



if __name__ == '__main__':
    lottery()
    userinfo()
