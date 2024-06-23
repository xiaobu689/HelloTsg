"""
浓五的酒馆
路径：浓五小酒馆小程序
变量名：nwbar
格式： 任意请求头抓 Authorization 值
定时设置：每天一次就行，时间随意
cron: 33 8 * * *
const $ = new Env("浓五小酒馆");
"""
import os
import requests

# print("This script is disabled.")
# exit(0)

class WLY():
    def __init__(self, token):
        self.token = token
        self.headers = {
            'authority': 'stdcrm.dtmiller.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': token,
            'content-type': 'application/json',
            'referer': 'https://servicewechat.com/wxed3cf95a14b58a26/200/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }

    def user_info(self):
        response = requests.get('https://stdcrm.dtmiller.com/scrm-promotion-service/mini/wly/user/info',
                                headers=self.headers)
        if not response or response.status_code != 200:
            print('❌获取用户信息失败')
            return
        response_json = response.json()
        if response_json['code'] == 0:
            nick_name = response_json['data']['member']['nick_name']
            mobile = response_json['data']['member']['mobile']
            points = response_json['data']['member']['points']
            print(f'🎉 {nick_name} | {mobile} | {points}积分')
        else:
            print(f'❌获取用户信息失败 | {response_json["msg"]}')

    def nwbar_sign(self):
        params = {
            'promotionId': 'PI66596f56185fc0000a529e7d',  # 每一期固定不变，新一期重新获取
        }
        response = requests.get(
            'https://stdcrm.dtmiller.com/scrm-promotion-service/promotion/sign/today',
            params=params,
            headers=self.headers,
        )
        print(response.text)
        msg = '--------------- 开始签到 ---------------\n'
        if not response or response['code'] != 0:
            print('❌签到异常')
            return
        response_json = response.json()
        if response_json['code'] == 0:
            award = response_json['data']['prize']['goodsName']
            print(f'✅签到成功 | 获得{award}')
        else:
            msg += f'❌签到失败，{response_json["msg"]}'
    def main(self):
        self.user_info()
        self.nwbar_sign()


if __name__ == '__main__':
    env_name = 'nwbar'
    token = os.getenv(env_name)
    token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJtaW5pYXBwX2N1c3RvbWVyIiwic3ViIjoib0JMbkk1ZnllSnMzWU5WY2hpeFZWdXRCaHlETSIsImV4cCI6MTcxOTA3NzE4NX0.VGehIiTwsyndtDRPKRcMwPBda--ZVWgQTfgqI_xDheh3AD8vZ1xS0QyWlogsfMGc7q7dez0gG_clfYpXNlNbeA'
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    WLY(token).main()