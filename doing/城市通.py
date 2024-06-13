"""
城市通

抓任意包请求头 token
变量名: CST_TOKEN

cron: 45 6 * * *
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
        self.coinTaskCode = ''
        self.coinRecordNo = ''
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
            tasks = response["data"]["detailsList"]
            for task in tasks:
                if task["mainTitle"] == "每日观看5个视频广告":
                    print(f'✅{task["mainTitle"]} | {task["subTitle"]}')
                    self.taskCode = task["taskCode"]
                    if task["recordNo"] != "":
                        self.recordNo = task["recordNo"]

    def receive_task(self):
        import requests
        headers = {
            'Host': 'cvg.17usoft.com',
            'Connection': 'keep-alive',
            'Content-Length': '375',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003133) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/416/page-frame.html',
        }

        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'share_rf_cxxc_240524',
            'traceId': 1718207195210,
            'activityCode': 'ACT_6645F6UF80A21F1BD0',
            'taskCode': self.taskCode,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': '02b4bc7c82826a2e88403a363ca92345',
        }

        response = requests.post('https://cvg.17usoft.com/marketingbff/saveMoneyZone/receiveTask', headers=headers,
                                 json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 1000:
                self.recordNo = response_json['data']['recordNo']
                print(f'✅任务领取成功 | ✅任务ID{self.recordNo}')

    def complete_task(self):
        import requests
        headers = {
            'Host': 'cvg.17usoft.com',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',  # 定值
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003133) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/416/page-frame.html',
        }
        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'share_rf_cxxc_240524',
            'traceId': 1718207232790,
            'recordNo': self.recordNo,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': 'd7071de3ec0c8cf506b217191d6b6b74',
        }

        response = requests.post('https://cvg.17usoft.com/marketingbff/saveMoneyZone/completeTask', headers=headers,
                                 json=json_data)
        print(response.text)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json and response_json["code"] == 1000:
                print(f'✅视频观看完成')
            else:
                print(f'❌视频观看失败')

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
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'defaultChannel',
            'traceId': 1717438573341,
            'recordNo': self.recordNo,
            'activityCode': 'ACT_6645F6UF80A21F1BD0',
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
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

    def coin_task(self):
        import requests
        headers = {
            'Host': 'cvg.17usoft.com',
            'Connection': 'keep-alive',
            # 'Content-Length': '259',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003133) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/416/page-frame.html',
        }

        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'sqzq',
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': '12d1fab944be9b6543366820de5ab3a9',
        }
        response = requests.post('https://cvg.17usoft.com/cst/activity/center/activity/taskFlow', headers=headers,
                                 json=json_data)
        print(response.text)
        # 检查是否有响应
        if not response or response.status_code != 200:
            print("response err")
            return

        response_json = response.json()
        if response_json and response_json["code"] == 1000:
            tasks = response_json["result"]["taskList"]
            for task in tasks:
                taskCode = task["taskCode"]
                if task["taskName"] == "CST会员看视频任务":
                    for i in range(10):
                        print(f'✅开始第{i + 1}个视频任务......')
                        coinRecordNo = self.coin_task_complate(taskCode)
                        time.sleep(random.randint(30, 40))
                        self.coin_task_receive(taskCode, coinRecordNo)
                        time.sleep(random.randint(15, 20))
                elif task["taskName"] == "CST会员公交订单任务":
                    print("✅开始公交订单任务......")
                    coinRecordNo = self.coin_task_complate(taskCode)
                    time.sleep(random.randint(30, 40))
                    self.coin_task_receive(taskCode, coinRecordNo)
                    time.sleep(random.randint(30, 40))

                elif task["taskName"] == "CST会员抽奖任务":
                    print("✅开始抽奖任务......")
                    # 金币抽奖
                    response_json = self.lucky_draw()
                    time.sleep(random.randint(30, 40))
                    self.lucky_draw_receive(response_json)
                    time.sleep(random.randint(30, 40))
                    # 领取任务完成奖励
                    coinRecordNo = self.coin_task_complate(taskCode)
                    time.sleep(random.randint(30, 40))
                    self.coin_task_receive(taskCode, coinRecordNo)
                    time.sleep(random.randint(30, 40))

                elif task["taskName"] == "CST会员酒店浏览任务":
                    print("✅开始浏览任务......")
                    coinRecordNo = self.coin_task_complate(taskCode)
                    time.sleep(random.randint(30, 40))
                    self.coin_task_receive(taskCode, coinRecordNo)
                    time.sleep(random.randint(30, 40))

        else:
            return

    def coin_task_complate(self, taskCode):
        import requests
        headers = {
            'Host': 'cvg.17usoft.com',
            'Connection': 'keep-alive',
            # 'Content-Length': '295',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003133) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/416/page-frame.html',
        }
        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'sqzq',
            'taskCode': taskCode,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': 'f0026697d9f03b6075496aacb4728011',
        }
        response = requests.post(
            'https://cvg.17usoft.com/cst/activity/center/activity/dailyTaskRecAndFinish',
            headers=headers,
            json=json_data,
        )
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json and response_json["code"] == 1000:
                recordNo = response_json["result"]["recordNo"]
                return recordNo
            else:
                return None
        else:
            return None

    def coin_task_receive(self, coinTaskCode, coinRecordNo):
        import requests
        headers = {
            'Host': 'cvg.17usoft.com',
            'Connection': 'keep-alive',
            # 'Content-Length': '329',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003133) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/416/page-frame.html',
        }

        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'sqzq',
            'taskCode': coinTaskCode,
            'recordNo': coinRecordNo,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': '005ea39bf4dc469ce95a38b4fc2e4744',
        }

        response = requests.post(
            'https://cvg.17usoft.com/cst/activity/center/activity/dailyTaskSendCoin',
            headers=headers,
            json=json_data,
        )
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json and response_json["code"] == 1000:
                print(f'✅{response_json["result"]["recordNo"]} | 任务完成 | 奖励领取完成')

    # 抽奖
    def lucky_draw(self):
        import requests
        headers = {
            'Host': 'wxxcx.17u.cn',
            'Connection': 'keep-alive',
            # 'Content-Length': '277',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003133) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/416/page-frame.html',
        }

        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': '',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'goldenCoinFlag': True,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': 'bd7c3ba1e242cdc99d2955915f9b6b8f',
        }

        response = requests.post('https://wxxcx.17u.cn/subwayapi/welfare/luckyDraw', headers=headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json and response_json["code"] == 1000 and "orderNo" in response_json["result"]:
                print(f'金币抽奖获得{response_json["result"]["prize"]["name"]}')
                return response_json
            else:
                return None
        else:
            return None

    def lucky_draw_receive(self, response_json):
        import requests

        headers = {
            'Host': 'wxxcx.17u.cn',
            'Connection': 'keep-alive',
            # 'Content-Length': '325',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003133) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx624dc2cce62f7008/416/page-frame.html',
        }

        if response_json is None:
            return

        id = response_json["result"]["prize"]["id"]
        type = response_json["result"]["prize"]["type"]
        awardCount = response_json["result"]["prize"]["awardCount"]
        orderNo = response_json["result"]["orderNo"]

        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'sqzq',
            'orderNo': orderNo,
            'id': id,
            'type': type,
            'awardCount': awardCount,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': 'c29f653391e413d914f3d2bebc642aea',
        }

        response = requests.post('https://wxxcx.17u.cn/subwayapi/welfare/receive', headers=headers, json=json_data)

        if response and response.status_code == 200:
            response_json = response.json()
            if response_json and response_json["code"] == 1000:
                print(f'金币抽奖奖励领取成功')

    def main(self):
        self.coupon_list()
        self.user_mileage_info()
        self.task_list()

        # 签到
        self.sign()
        time.sleep(random.randint(30, 40))

        # 领积分任务、看视频
        self.receive_task()
        for i in range(5):
            self.complete_task()
            time.sleep(random.randint(30, 40))
        self.receive_rewards()
        time.sleep(random.randint(30, 40))

        # 领金币任务、看视频
        self.coin_task()


if __name__ == '__main__':
    env_name = 'CST_TOKEN'
    tokenStr = os.getenv(env_name)
    # tokenStr = 'ohmdTt1TSce70l1uL1U2DGcZmGVU#iH3PGf9ZucSMMEYi4keylA=='
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
