"""
中国人保

抓任意包请求头 Access-Token
变量名: JSB_TOKEN

cron: 35 6 * * *
const $ = new Env("中国人保");
"""
import os
import random
import re
import time
import random
import time
import requests
from datetime import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class ZGRB():
    name = "中国人保"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Host': 'mp.picclife.cn',
            # 'Cookie': 'app-token=7b22757365724964223a226130346563663832633733363466313361393963396464656562373530353063222c2273657373696f6e4964223a2234316164623031302d336163362d343235652d623665612d323865653761666130626465222c2263726561746554696d65223a313731393035303532303435387d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221903f653b792e5-0a47eb3602634f8-75070f20-329160-1903f653b7acf2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwM2Y2NTNiNzkyZTUtMGE0N2ViMzYwMjYzNGY4LTc1MDcwZjIwLTMyOTE2MC0xOTAzZjY1M2I3YWNmMiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221903f653b792e5-0a47eb3602634f8-75070f20-329160-1903f653b7acf2%22%7D; sajssdk_2015_cross_new_user=1',
            'x-app-auth-type': 'APP',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 PBrowser/3.16.0 PiccApp/6.22.6 &&webViewInfo=3.16.0&&appInfo=piccApp&&appVersion=6.22.6',
            'Referer': 'https://mp.picclife.cn/dop/scoremall/mall/',
            'x-app-auth-token': '7b22757365724964223a226130346563663832633733363466313361393963396464656562373530353063222c2273657373696f6e4964223a2231303437303031382d313737662d343332322d383331332d633639646461636237336461222c2263726561746554696d65223a313731393035363931323537377d',
            'x-app-score-channel': 'picc-app001',
            'Origin': 'https://mp.picclife.cn',
            'x-app-auth-url': 'https://mp.picclife.cn/dop/scoremall/mall/#/dailyAttendance?apply=app',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            # 'Content-Length': '397',
            'X-Tingyun': 'c=B|tV_cscse5A0;x=2aa29c6c1b4c4c5e',
            'x-app-score-platform': 'picc-app',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
        }

    def sign(self):
        json_data = {}
        response = requests.post(
            'https://mp.picclife.cn/dop/scoremall/coupon/ut/signIn/get',
            headers=self.headers,
            json=json_data,
        )
        print(response.text)
        if not response or response.status_code != 200:
            print('签到异常')
            return
        response_json = response.json()
        if response_json['resultCode'] == "0000":
            totalSignInDays = response_json['result']['totalSignInDays']
            print(f'签到成功 | 总签到天数：{totalSignInDays}天')
        else:
            print(f'签到失败 | {response_json["resultMsg"]}')

    def do_task(self):
        json_data = {
            'type': 1,
            'ver': 'AZzqU5arEd+1YXgLSgr0wyGpIm9skwPB6eiUvGy/Zr3hIdPaVurjPj7RIWkj/pajI55+k4Tl4DD3FXynTceGXJl38rlK4ZPkDSUXaHlQjcwuOlJAdJ0hubpv0NYfkbDa93UQj1uTftP2GMaRydkmca/TuZXKMJVoVcPzZj8uUnCS/EN2BpTSWJ/YvZ9zgSOz6C1GWZO6MwF8kcEE2aR50RlH9230JqqIUIWrAFO9VQ1UBUmBSZOzDyDxUaBlHVAkUPeOM0YaT7wd/kXk/JmCgduy2k3fy974XyNObW+xDBssgpZa72k6DOHot/gCoZZnAfF4OgFEesMRz80TcfsgPQ==',
            'localizedModel': '',
            'platform': '',
        }

        response = requests.post(
            'https://mp.picclife.cn/dop/scoremall/coupon/ut/task/list',
            headers=self.headers,
            json=json_data,
        )
        print(response.text)
        if not response or response.status_code != 200:
            print('获取任务列表信息异常')
            return
        response_json = response.json()
        if response_json['resultCode'] == "0000":
            list = response_json['result']['taskList']
            for task in list:
                name = task['name']
                doneTime = task['doneTime']
                if doneTime == 0:
                    self.complate_task(task['id'], name)
                    time.sleep(random.randint(20, 30))
        else:
            print(f'获取任务列表失败 | {response_json["resultMsg"]}')

    def get_points(self):
        json_data = {}
        response = requests.post(
            'https://mp.picclife.cn/dop/scoremall/score/internal/scoreAccount/queryMyScoreAccount',
            headers=self.headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            print('获取积分信息异常')
            return
        response_json = response.json()
        if response_json['resultCode'] == "0000":
            totalScore = response_json["result"]["totalScore"]
            availableScore = response_json["result"]["availableScore"]
            print(f'🐱总积分: {totalScore} | 可用积分：{availableScore}')
        else:
            print(f'获取积分余额失败 | {response_json["resultMsg"]}')

    def complate_task(self, taskId, name):
        json_data = {
            'businessId': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'taskId': taskId,
        }

        response = requests.post(
            'https://mp.picclife.cn/dop/scoremall/coupon/ut/task/complete',
            headers=self.headers,
            json=json_data,
        )
        print(response.text)
        if not response or response.status_code != 200:
            print('任务完成异常')
            return
        response_json = response.json()
        if response_json['resultCode'] == "0000":
            print(f'🐱{name} | ✅任务完成')
        else:
            print(f'🐱{name} | ❌任务失败 | {response_json["resultMsg"]}')

    def main(self):
        # self.get_points()
        self.do_task()
        # time.sleep(random.randint(15, 30))
        # self.sign()


if __name__ == '__main__':
    env_name = 'JSB_TOKEN'
    token = os.getenv(env_name)
    token = 'eee'
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    ZGRB(token).main()
