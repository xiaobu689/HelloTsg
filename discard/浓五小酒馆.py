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

class TTCY():
    def __init__(self, token):
        self.token = token

    def nwbar_sign(self):
        headers = {
            'authority': 'stdcrm.dtmiller.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': self.token,
            'content-type': 'application/json',
            'referer': 'https://servicewechat.com/wxed3cf95a14b58a26/199/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129',
            'xweb_xhr': '1',
        }

        params = {
            'promotionId': 'PI65e0c0230791e3000a083cd4',
        }

        url = 'https://stdcrm.dtmiller.com/scrm-promotion-service/promotion/sign/today'

        response = requests.get(url, params=params, headers=headers, verify=False).json()
        # print(response)
        msg = '--------------- 开始签到 ---------------\n'
        if response['code'] == 0:
            score = response['data']['score']
            msg += f'✅签到成功，获得{score}, 已签到{response["data"]["signDays"]}\n'
            print(msg)
        else:
            msg += f'❌签到失败，{response["msg"]}'
            print(msg)

        return msg

    def main(self):
        self.nwbar_sign()

        # 通知
        # send(title, msg)


if __name__ == '__main__':
    env_name = 'nwbar'
    token = os.getenv(env_name)
    token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJtaW5pYXBwX2N1c3RvbWVyIiwic3ViIjoib0JMbkk1ZnllSnMzWU5WY2hpeFZWdXRCaHlETSIsImV4cCI6MTcxNjAyMzgxOH0.CWd7MeG-0Cl0P9Z-VpuAweeWxMY5Y82rWvtzEswuz9snbD8r-icU_Z3T8A6jfAsrdpassy7JLt7S_0hu-guQEg'
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    TTCY(token).main()
