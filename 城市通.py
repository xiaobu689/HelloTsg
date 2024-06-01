"""
城市通

抓任意包请求头 token
变量名: CST_TOKEN

cron: 0 0 * * *
const $ = new Env("城市通");
"""
import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

from common import qianwen_messages, make_request

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class CST():
    name = "城市通"

    def __init__(self, token):
        self.token = token.split('#')[0]
        self.deptCode = token.split('#')[1]
        self.verify = False
        self.totalScore = 0
        self.headers = {
            'Host': 'tcmobileapi.17usoft.com',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'TC-MALL-PLATFORM-CODE': 'SUBWAY_MP',
            'Sec-Fetch-Site': 'cross-site',
            'TC-MALL-OS-TYPE': 'IOS',
            'TC-MALL-DEPT-CODE': self.deptCode,
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Origin': 'https://wx.17u.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003131) NetType/4G Language/zh_CN miniProgram/wx624dc2cce62f7008',
            'Referer': 'https://wx.17u.cn/',
            'TC-MALL-CLIENT': 'API_CLIENT',
            'TC-MALL-USER-TOKEN': self.token,
            'TC-MALL-PLATFORM-SUB': 'SUBWAY_MP',
            'Sec-Fetch-Dest': 'empty',
        }
        self.signHeaders = {
            'Host': 'wx.17u.cn',
            # 'Cookie': '__tctmb=217272534.1104278252383289.1717183237683.1717183237683.13; __tctma=217272534.1717182787184584.1717182787141.1717182787141.1717182787141.1; __tctmc=217272534.223058653; __tctmd=217272534.213680082; __tctmu=217272534.0.0; __tctmz=217272534.1717182787141.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); __tctrack=0; longKey=1717182787184584',
            'TC-MALL-USER-TOKEN': self.token,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003131) NetType/4G Language/zh_CN miniProgram/wx624dc2cce62f7008',
            'TC-MALL-PLATFORM-SUB': 'SUBWAY_MP',
            'Referer': 'https://wx.17u.cn/mileagemall/activity/mallVue3/home?miniAppPlat=citymp&refid=2000027364&unionId=ohmdTt1TSce70l1uL1U2DGcZmGVU&openId=o4VjT5Az0RxdUIz6-sBCjVDBpRd0&r=169&cityCode=310000',
            'TC-MALL-PLATFORM-CODE': 'SUBWAY_MP',
            'TC-MALL-DEPT-CODE': self.deptCode,
            'TC-MALL-CLIENT': 'API_CLIENT',
            'Origin': 'https://wx.17u.cn',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            'TC-MALL-OS-TYPE': 'IOS',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Sec-Fetch-Mode': 'cors',
        }

    def sign(self):
        json_data = {}
        response = requests.post('https://wx.17u.cn/wxmpsign/sign/saveSignInfo',  headers=self.signHeaders,
                                 json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'✅签到成功')
            else:
                print(f'❌签到失败， {response_json["msg"]}')
        else:
            print(f'❌签到失败')

    def coupon_list(self):
        params = {
            'zoneId': '8',
        }
        url = 'https://tcmobileapi.17usoft.com/mallgatewayapi/activityApi/superCoupon/zoneSku'
        response = requests.get(url, params=params, headers=self.headers)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                coupons = response_json['data']["skuInfos"]
                for coupon in coupons:
                    if coupon["baseInfo"]["threeLevelCategoryName"] == "公交地铁":
                        print(f'✅{coupon["baseInfo"]["skuTitle"]} | {coupon["baseInfo"]["sill"]} | {coupon["buttonInfo"]["content"]}')

# ------------------------------------------------------------------------------

    def user_mileage_info(self):
        json_data = {}
        url = 'https://tcmobileapi.17usoft.com/mallgatewayapi/userApi/mileages/remain'
        response = requests.post(url, headers=self.headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'✅当前可用里程：{response_json["data"]["remainMileageTitle"]} | 价值：{response_json["data"]["deductionPrice"]}元')

    def main(self):
        self.sign()
        self.coupon_list()
        self.user_mileage_info()


if __name__ == '__main__':
    env_name = 'CST_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"上海嘉定共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        CST(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
