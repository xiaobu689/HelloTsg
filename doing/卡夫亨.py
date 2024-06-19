"""
杰士邦

抓任意包请求头 Access-Token
变量名: JSB_TOKEN

cron: 35 6 * * *
const $ = new Env("杰士邦");
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class JSB():
    name = "杰士邦"

    def __init__(self, token):
        self.token = token
        self.sharecodes = []
        self.headers = {
            'Host': 'kraftheinzcrm-uat.kraftheinz.net.cn',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'token': self.token,
            'Origin': 'https://fscrm.kraftheinz.net.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003135) NetType/WIFI Language/zh_CN',
            'Referer': 'https://fscrm.kraftheinz.net.cn/',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Dest': 'empty',
        }
    def user_info(self):
        url = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/getUserInfo'
        response = requests.get(url, headers=self.headers)
        if not response or response.status_code != 200:
            print("获取用户信息失败")
            return
        response_json = response.json()
        if response_json['error_code'] == 0:
            nickname = response_json["data"]["nickname"]
            score = response_json['data']['memberInfo']['score']
            phone = response_json['data']['memberInfo']['phone']
            print(f'🐶{nickname} | 🐱{phone} | 💰{score}积分')
    def sign(self):
        response = requests.post('https://fscrm.kraftheinz.net.cn/crm/public/index.php/api/v1/dailySign', headers=self.headers)
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['error_code'] == 0:
            print(f'✅签到成功')
        else:
            print(f'❌签到失败：{response_json["msg"]}')

    def share_cookbook_task(self):
        data = {
            'page': '1',
            'pagesize': '10',
        }
        url = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/getCookbookIndex'
        response = requests.post(url, headers=self.headers, data=data)
        if not response or response.status_code != 200:
            print("获取分享cookBook失败")
            return
        response_json = response.json()
        if response_json['error_code'] == 0:
            books = response_json["data"]["chineseCookbook"]["data"]
            ramdom_book_id = random.choice(books)['id']
            print(f'随机获取cookBook：{ramdom_book_id}')
            self.share(ramdom_book_id)

    def share(self, cookbook_id):
        data = {
            'cookbook_id': cookbook_id,
        }
        url = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/createCookbookCode'
        response = requests.post(url, headers=self.headers, data=data)
        if not response or response.status_code != 200:
            print("获取分享cookBook失败")
            return
        response_json = response.json()
        print(response_json)
        if response_json["error_code"] == 0:
            code_url = response_json['data']['code_url'].replace("https://kraftheinzcrm-uat.kraftheinz.net.cn/?", "")
            print(f"获取分享文章链接成功: {code_url}")
            self.sharecodes.append(code_url)

    def help(self, tokens):
        print("----------------tokens=", tokens)
        try:
            if len(tokens) == 1:
                print("账号不足2个,自己不能给自己助力")
                return
            for i in range(len(tokens)):
                print("--------22222i=", i)
                print("---------33333=", self.sharecodes[(i + 1) % len(self.sharecodes)])

                print("------------------222222=", self.sharecodes[(i + 1) % len(tokens)])
                url = {
                    'url': 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/recordScoreShare',
                    'headers': {
                        'Host': 'kraftheinzcrm-uat.kraftheinz.net.cn',
                        'token': tokens[i]
                    },
                    'body': self.sharecodes[(i + 1) % len(tokens)]
                }
                print("--------111111111url=", url)
                response = requests.post(url['url'], headers=url['headers'], data=url['body'])
                print("------------222222222222response=", response.text)
                result = response.json()
                if response and response.status_code == 200 and result.get('error_code') == 0:
                    if i + 1 == len(tokens):
                        print(f"账号最后一位助力首账号成功: {result['msg']}")
                    else:
                        print(f"账号 {i + 2} 被助力成功: {result['msg']}")
                else:
                    print("内部互助失败")
                time.sleep(1)
        except Exception as e:
            print(f"Exception in recordshare function: {str(e)}")

    def main(self):
        self.user_info()
        self.sign()
        # self.share_cookbook_task()



if __name__ == '__main__':
    env_name = 'JSB_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = '67b35f0dcd6db28a784f231d3ca03dea&c83c2a8116eb6e9ce60f3bd43b44467a'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"杰士邦共获取到{len(tokens)}个账号")

    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        jsb = JSB(token)
        jsb.main()
        print("\n随机等待30-60s进行下一个账号")
        # time.sleep(random.randint(30, 60))
        print("----------------------------------")
        if i == len(tokens):
            jsb.help(tokens)
