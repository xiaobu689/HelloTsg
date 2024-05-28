"""
哈罗单车

路径：哈罗单车APP
用途：签到、看视频得鼓励金，鼓励金兑骑行券、话费
变量名：hello_token
格式： 任意请求头抓 Authorization 值

定时设置：每天一次就行，时间随意
cron: 26 11 * * *
const $ = new Env("哈罗单车");
"""
import os

import requests

from sendNotify import send


class TTCY():
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Host': 'api.hellobike.com',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://m.hellobike.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 Ariver/1.0.15  NebulaSDK; app=easybike; version=6.62.5 WK RVKType(1) NebulaX/1.0.0',
            'Referer': 'https://m.hellobike.com/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }

    # 签到
    def hello_sign(self):
        json_data = {
            'from': 'h5',
            'systemCode': 61,
            'platform': 4,
            'version': '6.62.5',
            'action': 'common.welfare.signAndRecommend',
            'token': self.token,
        }
        url = 'https://api.hellobike.com/api?common.welfare.signAndRecommend'
        response = requests.post(url, headers=self.headers, json=json_data).json()
        # print(response)
        if response['code'] == 0 and response['data']['didSignToday']:
            msg = f'✅签到成功, 奖励金：+{response["data"]["bountyCountToday"]}'
        else:
            msg = '❌签到失败， cookie可能已失效！'

        print(msg)
        return msg

    # 查询奖励金
    def hello_point(self):
        json_data = {
            'from': 'h5',
            'systemCode': 61,
            'platform': 4,
            'version': '6.63.0',
            'action': 'user.taurus.pointInfo',
            'token': self.token,
            'pointType': 1,
        }
        url = 'https://api.hellobike.com/api?user.taurus.pointInfo'
        response = requests.post(url, headers=self.headers, json=json_data).json()
        if response['code'] == 0:
            msg = f'✅可用奖励金：{response["data"]["amount"]}'
        else:
            msg = '❌查询奖励金失败， cookie可能已失效！'

        print(msg)
        return msg

    def main(self):
        msg1 = self.hello_sign()
        msg2 = self.hello_point()

        send("哈啰单车", msg1 + msg2)


if __name__ == '__main__':
    env_name = 'HELLO_TOKEN'
    token = os.getenv(env_name)
    if not token:
        print(f'⛔️未获取到token变量：请检查变量 {env_name} 是否填写')
        exit(0)

    TTCY(token).main()
