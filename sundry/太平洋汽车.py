"""
太平洋汽车抽奖

20240523 每日抽奖已废，新增每日开盲盒

APP：太平洋汽车
变量名：tpyqc_cookie
格式： cookie#手机号#openid#devId
任意请求头获取cookie, 默认手动提现，如设置自动提现进入我的钱包-瓜分现金-提现-授权微信，抓包openid和devid

定时设置：
cron: 37 9 * * *
const $ = new Env("太平洋汽车");
"""
import os
import random
import time
import requests
import json

from sendNotify import send


class TPYQCIO():
    name = "太平洋汽车抽奖"

    def __init__(self, cookie_str):
        parts = cookie_str.split('#')
        self.auto_cash_out = False
        self.cookie = parts[0]
        self.phone = parts[1]
        if len(parts) == 4:
            self.openid = parts[2]
            self.devid = parts[3]
            self.auto_cash_out = True

    def receice(self):
        url1 = 'https://act1.pcauto.com.cn/discount/api/series/list'
        headers = {
            'Host': 'act1.pcauto.com.cn',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://www1.pcauto.com.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Referer': 'https://www1.pcauto.com.cn/',
            'Content-Length': '14',  # 注意：这个值通常由库自动处理，所以通常不需要手动设置
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty'
        }
        data1 = json.dumps({"actId": "19"})
        response1 = requests.post(url1, headers=headers, data=data1)
        data2 = response1.json()
        first_item = data2['data'][0]
        brand_id = first_item['brandId']
        brand = first_item['brand']
        serial_group_id = first_item['serialGroupId']
        serial_group_name = first_item['serialGroupName']
        serial_group_pic = first_item['serialGroupPic']
        headers = {
            'Host': 'act1.pcauto.com.cn',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://www1.pcauto.com.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Referer': 'https://www1.pcauto.com.cn/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Cookie': self.cookie
        }

        playRecordId = random.randint(100000, 106271)
        print(f'本次即将尝试领取 {playRecordId} 记录的奖励')
        data = {
            "playRecordId": playRecordId,  # 104271
            "locationVersion": 1,
            "locationMessage": "",
            "phone": self.phone,
            "pcsuv": 52792536,
            "actId": 19,
            "source": 2,
            "sourceDetail": 5,
            "currentFrom": "https://www1.pcauto.com.cn/zt/discount-topics/app-wap/index.html#/?actId=19&sourceDetail=5&isActivity=1&app_ver=7.1.2",
            "city": "上海",
            "seriesBOList": [
                {
                    "serialGroupPic": serial_group_pic,
                    "brand": brand,
                    "brandId": brand_id,
                    "serialGroupId": serial_group_id,
                    "serialGroupName": serial_group_name
                }
            ],
            "locationType": 4,
            "cityId": "3"
        }
        response = requests.post(
            'https://act1.pcauto.com.cn/discount/api/enroll/save',
            headers=headers,
            json=data
        )
        print(response.text)
        resp = response.json()
        if resp['code'] == 200 and resp['data']['code'] == 0:
            msg = f'领取成功\n'
        else:
            msg = f'领取失败, {resp["data"]["msg"]}\n'
        return msg

    def start_receiving(self):
        msg = '开始领取红包......\n'
        print(msg)
        while True:
            msg += self.receice()
            if "领取成功" in msg:
                print("✅领取成功，退出循环\n")
                msg += "✅领取成功，退出循环\n"
                break
            sleep_time = random.randint(15, 45)
            print(f"❌本次领取失败，{sleep_time} 秒后进行下一次尝试......\n")
            time.sleep(sleep_time)
        return msg

    def cashOut(self):
        msg = "开始提现......\n"
        print(msg)
        # 定义URL和请求头
        url = 'https://act1.pcauto.com.cn/discount/api/cash/out'
        headers = {
            'Host': 'act1.pcauto.com.cn',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://www1.pcauto.com.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Referer': 'https://www1.pcauto.com.cn/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Cookie': self.cookie
        }
        data = {
            'devId': self.devid,
            'openId': self.openid,
            'amount': '0.3'
        }
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        if response_json['code'] == 200:
            if response_json['data']['code'] == 0:
                msg1 = f'✅提现成功：{response_json["data"]["msg"]}'
                msg += msg1
            elif response_json['data']['code'] == 3:
                msg2 = f'❌提现失败：余额不足0.3，再攒攒吧'
                msg += msg2
        else:
            msg3 = f'❌提现失败：{response_json["msg"]}'
            msg += msg3

        return msg

    def main(self):
        title = "太平洋汽车每日抽奖"
        msg1 = self.start_receiving()
        if self.auto_cash_out:
            time.sleep(random.randint(15, 20))
            msg2 = self.cashOut()
        else:
            msg2 = f'❌余额不足，先不提现，再攒攒吧！\n'
            print(msg2)

        print(msg1+msg2)
        # 通知
        send(title, msg1 + msg2)


if __name__ == '__main__':
    env_name = 'tpyqc_cookie'
    cookie = os.getenv(env_name)
    if not cookie:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    TPYQCIO(cookie).main()
