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

from common import qianwen_messages, make_request, get_current_timestamp_milliseconds

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class CST():
    name = "城市通"

    def __init__(self, token):
        self.token = token.split('#')[0]
        self.deptCode = token.split('#')[1]
        self.verify = False
        self.totalScore = 0
        self.appId = 'wx624dc2cce62f7008'
        self.cityCode = '310000'
        self.activityCode = ''
        self.openId = 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0'
        self.unionId = 'ohmdTt1TSce70l1uL1U2DGcZmGVU'
        self.taskCode = ''
        self.recordNo = ''
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
        url = 'https://wx.17u.cn/wxmpsign/sign/saveSignInfo'
        response = requests.post(url, headers=self.signHeaders, json=json_data)
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
                        print(
                            f'✅{coupon["baseInfo"]["skuTitle"]} | {coupon["baseInfo"]["sill"]} | {coupon["buttonInfo"]["content"]}')

    def user_mileage_info(self):
        json_data = {}
        url = 'https://tcmobileapi.17usoft.com/mallgatewayapi/userApi/mileages/remain'
        response = requests.post(url, headers=self.headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            print(response_json)
            if response_json['code'] == 200:
                print(
                    f'✅当前可用里程：{response_json["data"]["remainMileageTitle"]} | 价值：{response_json["data"]["deductionPrice"]}元')

    def task_list(self):
        headers = {
            'Host': 'cvg.17usoft.com',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003132) NetType/4G Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/415/page-frame.html',
        }
        traceId = get_current_timestamp_milliseconds()
        json_data = {
            'deviceSystem': 'ios',
            'appId': self.appId,
            'cityCode': self.cityCode,
            'channelCode': 'defaultChannel',
            'traceId': traceId,
            'activityKey': 'sqzq_rw',
            'openId': self.openId,
            'unionId': self.unionId,
            'supplier': 'SH_SHS_M',
            'supplierId': self.cityCode,
            'sign': '619fdd6180f41f6bbe6087713eb7fab',
        }
        url = 'https://cvg.17usoft.com/marketingbff/saveMoneyZone/userQueryTaskList'
        response = make_request(url, json_data=json_data, method='post', headers=headers)
        if response and response["code"] == 1000:
            activityCode = response["data"]["activityCode"]
            self.activityCode = activityCode
            print(self.activityCode)
            tasks = response["data"]["detailsList"]
            for task in tasks:
                if task["mainTitle"] == "每日观看5个视频广告":
                    print(f'✅{task["mainTitle"]} | {task["subTitle"]}')
                    self.taskCode = task["taskCode"]
                    self.recordNo = task["recordNo"]
                    print(self.taskCode)
                    print(self.recordNo)

    def complete_task(self):
        headers = {
            'Host': 'cvg.17usoft.com',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003132) NetType/4G Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/415/page-frame.html',
        }

        json_data = {
            'deviceSystem': 'ios',
            'appId': self.appId,
            'cityCode': self.cityCode,
            'channelCode': 'defaultChannel',
            'traceId': 1717438571187,
            'recordNo': self.recordNo,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': self.cityCode,
            'sign': 'd949d54c44220a09edc06970f81191db',
        }
        url = 'https://cvg.17usoft.com/marketingbff/saveMoneyZone/completeTask'
        response = make_request(url, json_data=json_data, method='post', headers=headers)
        print(response)
        if response and response["code"] == 1000:
            print(f'✅任务完成')
        else:
            print(f'❌任务失败')

    def receive_rewards(self):
        headers = {
            'Host': 'cvg.17usoft.com',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003132) NetType/4G Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/415/page-frame.html',
        }
        json_data = {
            'deviceSystem': 'ios',
            'appId': self.appId,
            'cityCode': self.cityCode,
            'channelCode': 'defaultChannel',
            'traceId': 1717438573341,
            'recordNo': self.recordNo,
            'activityCode': self.activityCode,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': self.cityCode,
            'sign': '5b75aeb5b8abbd33d778da7548f9d1f5',
        }
        url = 'https://cvg.17usoft.com/marketingbff/saveMoneyZone/receiveAward'
        response = make_request(url, json_data=json_data, method='post', headers=headers)
        print(response)
        if response and response["code"] == 1000:
            print(
                f'✅领取成功 | 金币：{response["data"]["awardAmount"]} | 价值：{response["data"]["awardDeductionAmount"]}元')
        else:
            print(f'❌领取失败')

    def main(self):
        self.sign()
        self.coupon_list()
        self.user_mileage_info()
        self.task_list()
        # 看视频
        self.complete_task()
        self.receive_rewards()



if __name__ == '__main__':
    env_name = 'CST_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = 'ohmdTt1TSce70l1uL1U2DGcZmGVU#iH3PGf9ZucSMMEYi4keylA=='
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"城市通共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        CST(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
