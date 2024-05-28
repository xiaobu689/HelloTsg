
"""
悦享会

路径：悦享会小程序
用途：签到、抽奖赚积分，积分可兑换实物
变量名：YXH_TOKEN
格式： 任意请求头抓 Authorization 值

定时设置：每天一次就行，时间随意
cron: 26 11 * * *
const $ = new Env("悦享会");
"""
import os
import random

import requests

def get_uuid(length=36):
    chars = "0123456789abcdef"
    uuid_list = [random.choice(chars) for _ in range(length)]

    # Set the UUID version (4)
    uuid_list[14] = '4'

    # Set the UUID variant (8, 9, a, or b)
    uuid_list[19] = chars[(int(uuid_list[19], 16) & 0x3) | 0x8]

    # Set the fixed UUID format
    uuid_format = [8, 13, 18, 23]
    for i in uuid_format:
        uuid_list[i] = '-'

    # Join the list into a string
    uuid_str = ''.join(uuid_list)
    print("---------------------uuid_str=", uuid_str)

    return uuid_str
class TTCY():
    def __init__(self, token):
        self.token = token

# //    def login(self):
# //        import requests
# //
# //        headers = {
# //            'Accept': '*/*',
# //            'Accept-Language': 'zh-CN,zh;q=0.9',
# //            'Connection': 'keep-alive',
# //            'Content-Type': 'application/json',
# //            'Referer': 'https://servicewechat.com/wx4e6c5384b429c008/147/page-frame.html',
# //            'Sec-Fetch-Dest': 'empty',
# //            'Sec-Fetch-Mode': 'cors',
# //            'Sec-Fetch-Site': 'cross-site',
# //            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129',
# //            'x-Hrt-Mid-Appid': 'API_AUTH_MINI',
# //            'xweb_xhr': '1',
# //        }
# //
# //        json_data = {
# //            'data': {
# //                'deviceChannel': 'WECHAT',
# //                'businessChannel': 'miniprogram',
# //                'channelCode': 'wechat',
# //                'typeId': '3001',
# //                'code': '0e3FdP100dY16S1mZM0008BhJu0FdP11',
# //            },
# //        }
# //
# //        response = requests.post(
# //            'https://member-gateway.yuexiu.com/gateway/member-process/wxLogin/autoLogin',
# //            headers=headers,
# //            json=json_data,
# //        ).json()
# //        memberId = ''
# //        token = ''
# //        if response['code'] == 'S0A00000':
# //            memberId = response['data']['memberId']
# //            token = response['data']['token']
# //        else:
# //            print('登录失败: ', response['msg'])
# //
# //        return memberId, token

    def sign(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Referer': 'https://servicewechat.com/wx4e6c5384b429c008/147/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129',
            'token': self.token,
            'x-Hrt-Mid-Appid': 'API_AUTH_MINI',
            'xweb_xhr': '1',
        }

        json_data = {
            'data': {
                'dataVerify': '0270921b9953a4c2f23e21122c0b4192a80cb3008d90356c91c8cf5206e52791e14af097fa72d034d8348735f4d836fd265e53f0a4b5e053e38aeeab11f9813549497160277c07843f3dc6dd6e472150d46b6def044f0b61b21813c0ce11d711854552df20019b458e25bf2ca982ccb65ddd14a19eb7c6f24264beb1a600b689c247213c8bb420f7c0873a148705de75a884d1887bb1d63dc87525516eb6b20bdac73a1da578fbce814ceff9111f7d1edaaa8763a29493836b495361780c3c7452cb4e374ac5a67baa907de27c5f14728d1cf0b979c2c0911c3d5143196e97ce2463604dcefba4e8484da42a3413b970d4d211786613e5da4ffa798d9b16259b',
                'pubKeyHash': '06c45a2106c731de3b153401bd0c4f45',  # 公共密钥，固定值
                'deviceChannel': 'WECHAT',  # 固定值
                'businessChannel': 'miniprogram',  # 固定值
                'channelCode': 'wechat',  # 固定值
            },
            'tid': 'cd67071a-e788-4d26-b7a4-03fccfe7a14a',
        }

        response = requests.post('https://member-gateway.yuexiu.com/gateway/memberTask/app/sign/signin',
                                 headers=headers, json=json_data).json()
        print(response)
        if response['code'] == 'S0A00000':
            print('✅签到成功')
        else:
            print('签到失败: ', response['msg'])  # 签到失败:  请求已失效

    def task_list(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Referer': 'https://servicewechat.com/wx4e6c5384b429c008/147/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129',
            'token': self.token,
            'x-Hrt-Mid-Appid': 'API_AUTH_MINI',
            'xweb_xhr': '1',
        }

        json_data = {
            'tid': get_uuid(),
        }

        response = requests.post('https://member-gateway.yuexiu.com/gateway/memberTask/app/task/myList',
                                 headers=headers, json=json_data).json()
        msg = ''
        if response['code'] == 'S0A00000':
            for task in response['data']:
                msg += f'✅{task["eventName"]}\n'
        msg += f'---------------------------------------\n'
        print(msg)

    def query_points(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Referer': 'https://servicewechat.com/wx4e6c5384b429c008/147/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129',
            'token': self.token,
            'x-Hrt-Mid-Appid': 'API_AUTH_MINI',
            'xweb_xhr': '1',
        }

        json_data = {}

        url = 'https://member-gateway.yuexiu.com/gateway/pointsAccount/app/queryAccount'

        response = requests.post(url, headers=headers, json=json_data).json()

        if response['code'] == 'S0A00000':
            msg = f'✅当前积分：{response["data"]["points"]}\n'
            msg += f'✅可用积分：{response["data"]["availablePoints"]}\n'
            msg += f'---------------------------------------\n'
            print(msg)
        else:
            print(response['msg'])

    def lottery(self):
        cookies = {
            'Hm_lpvt_1939de19cbf975b222b1b90095ee4c31': '1715931962',
            'Hm_lvt_1939de19cbf975b222b1b90095ee4c31': '1715931952',
        }

        while True:
            headers = {
                'Host': 'memact.yuexiu.com',
                'apixTimestamp': '1715931968', # 秒级时间戳
                'apixAuth': '1',
                # 'apixSign': '5F5F42003AF6924AAEAA9F959F803F20',
                'Sec-Fetch-Site': 'same-origin',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Sec-Fetch-Mode': 'cors',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x1800312c) NetType/WIFI Language/zh_CN miniProgram/wx4e6c5384b429c008',
                'Referer': 'https://memact.yuexiu.com/zzz_wx_app/star_act/star_act__box/a_001/index.html?sact_type=star_act__niudan&site_id=app.yuexiu&__v=28598866&is_wxapp=1&word=star_act0423',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                # 'Cookie': 'Hm_lpvt_1939de19cbf975b222b1b90095ee4c31=1715931962; Hm_lvt_1939de19cbf975b222b1b90095ee4c31=1715931952',
            }

            params = {
                'master_id': 'samaster-b40de697-2bca-4afa-9881-f24b7273c97c',   # 固定值
                'site_id': 'app.yuexiu',  # 固定值
                'wx_from': '4763271958715100',  # 固定值
                'wx_from_enc': 'dc1535817TkRjMk16STNNVGsxT0RjeE5URXdNQT09',  # 固定值
                '__d': '1715931968851',  # 当前时间毫秒时间戳
            }

            response = requests.get(
                'https://memact.yuexiu.com/__api_java__/z_app/star_act/web/zz_api__api_x__user_chou',
                params=params,
                cookies=cookies,
                headers=headers,
            ).json()
            print(response)
            if response['errcode'] == 0:
                msg = f'✅抽奖结果：{response["data"]["errmsg"]}\n'
                print(msg)
            else:
                print('❌抽奖失败: ', response['errmsg'])
                break





    def main(self):
        self.query_points()
        self.sign()
        self.task_list()
        self.lottery()

        # 通知
        # send(title, msg)


if __name__ == '__main__':
    env_name = 'YXH_TOKEN'
    token = os.getenv(env_name)
    token = '88627e81e05ae24f83955160c390f07e'
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    TTCY(token).main()


