"""
富士instax玩拍由我俱乐部

抓任意包请求头 Authorization
变量名: INSTAX_TOKEN

cron: 35 7 * * *
const $ = new Env("富士instax玩拍由我俱乐部");
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class INSTAX():
    name = "富士instax玩拍由我俱乐部"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': token,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Referer': 'https://servicewechat.com/wx3cb572fbf3aa30c8/134/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }
    def user_info(self):
        response = requests.get('https://psjia.ipason.com/api/v2/member/memberinfo', headers=self.headers)
        if not response or response.status_code != 200:
            print("获取用户信息失败")
            return
        response_json = response.json()
        if response_json['status'] == 0:
            print(f'🐶账号: {response_json["data"]["member_truename"]}')

    def user_score(self):
        params = {
            'limit': '20',
            'offset': '1',
        }
        response = requests.get('https://instax.app.xcxd.net.cn/api/user/273931/credit-record', params=params,
                                headers=self.headers)
        if not response or response.status_code != 200:
            print("获取积分失败")
            return
        response_json = response.json()
        if response_json['error'] == False:
            print(f'🐶积分: {response_json["data"]["normal_credit"]}积分\n')
        else:
            print(f'❌获取积分失败：{response_json["error"]}')



        response = requests.get('https://psjia.ipason.com/api/v2.member.score_shop/home', headers=self.headers)
        if not response or response.status_code != 200:
            print("获取积分失败")
            return
        response_json = response.json()
        if response_json['status'] == 0:
            print(f'💰积分: {response_json["data"]["score_val"]}积分\n')

    def sign(self):
        json_data = {}
        response = requests.post('https://psjia.ipason.com/api/v2.member.score_shop/signSub', headers=self.headers,
                                 json=json_data)
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['status'] == 0:
            print(f'✅签到成功')
        else:
            print(f'❌签到失败：{response_json["error"]}')

    def user_draw_chance(self):
        response = requests.get('https://instax.app.xcxd.net.cn/api/user/273931/draw-activities/41/chance',
                                headers=self.headers)
        if not response or response.status_code != 200:
            print("获取抽奖次数异常：", response.text)
            return
        response_json = response.json()
        if response_json['error'] == False:
            print(f'抽奖次数: {response_json["data"]}')
            return response_json['data']
        else:
            return 0

    def user_draw_score(self):
        json_data = {}
        response = requests.post('https://instax.app.xcxd.net.cn/api/user/273931/draw-activities/41/draw', headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            print("抽奖异常：", response.text)
            return
        response_json = response.json()
        print(response_json)
        if response_json['error'] == 'false':
            print(f'✅抽奖成功 | 获得: {response_json["data"]["record"]["desc"]}')
        else:
            print(f'❌抽奖失败：{response_json["error"]}')

    def main(self):
        # self.user_info()
        self.user_score()
        # self.sign()
        # time.sleep(random.randint(15, 20))
        count = self.user_draw_chance()
        if count == 0:
            print("你没有抽奖次数啦！")
            return
        for i in range(count):
            time.sleep(random.randint(15, 20))
            self.user_draw_score()



if __name__ == '__main__':
    env_name = 'INSTAX_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = 'Bearer ba1e26de2f7638ea712807caf68b62ceba0df60fe49daa1df4c80e63254f7927'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"富士instax玩拍由我俱乐部共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        INSTAX(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
