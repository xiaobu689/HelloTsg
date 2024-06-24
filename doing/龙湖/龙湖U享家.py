"""
龙湖U享家

抓任意包请求头 Access-Token
变量名: LHYXJ_TOKEN
注意登录后手机上如果再登陆会顶号

cron: 35 6 * * *
const $ = new Env("龙湖U享家");
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class LH():
    name = "龙湖U享家"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://servicewechat.com/wx2afa3f76abf7bd29/530/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'X-Gaia-Api-Key': 'a32fd551-8554-43a5-8eaf-4835079d9c14',
            'X-Tingyun': 'c=B|6jgbXJsLBgM',
            'apiversion': '2.0',
            'appversion': '1.0',
            'dxdeviceid': '6677b200z4EiTeinCIjbqrElZ6jqnAISGT4xCDD4',
            'lmId': '22082948',
            'openid': 'oVvTl5UYrNhqBIBs7HzWOZMEOM94',
            'phone': '17854279565',
            'refer': 'xcx',
            'user-source-channel': '{"mediaId":"","actionId":"source2","channelId":5,"customId":"","campaignId":"","serviceId":"0","serviceType":"cGFnZXMvcHVibGljVmlkZW8vcHVibGljVmlkZW8=","clickId":"","areaId":"","projectId":"","posterId":"","posterOwner":"","posterOwnerId":"","channelProjectId":"","fromActivityId":""}',
            'userId': 'e6319a4b-91b5-4e5d-9860-b5127f10141c',
            'x-authentication-id': 'e6319a4b-91b5-4e5d-9860-b5127f10141c',
            'x-authentication-token': 'dc2e0a19838543563971e373b409b6eb48b4e4fa7e8b7771b5f467bed0be8069ae75ee3b25908627ce1ac4306f1fa90ab78664b5b27b3c4114a500b98c0705b8505f185515f9d8c9fe26a9dc23fc14f5f75ac4268805706fa6c89bb715062fdca21b1125110da99e422424b504c9971d7d3b0ba00b658225a274d731c23534d45566e037e67d069d94665d41a493657be6c21063000ee37480e3a7dff765df59b9547061ac2f4f48251a65c97b49546f9390c87e70335c96794b37f52868cf495026bf28d3c7d1264a67aba310a477fef2bd1d8c58071570953c947b52586cf8b22e6db69c17b8113f1fc09c09f0c0eaab83f17d97440e73419f67c6acca4d73aeb79ca12108de6e74d0d5d3af3cfed8d00843db1ab9a1ee11ad5d0a957e472f9c302753de563e3b353ae953081b31381b2231ff31ccbd5e16f6cf0a66187bfdb1408f6250d1ef0b41197864297f4de8a185c55bc6a5dfecca4499b9c188bed7f4516379aa8a0607088cc3fa7314a61e603a410549bbf3f9d25acb734a2c39c09048b61709f44a76785782e5f19de61fa2293a75d74a8012ac094f62d0e87d69',
            'xweb_xhr': '1',
        }

    def user_info(self):
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://servicewechat.com/wx2afa3f76abf7bd29/530/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'X-Gaia-Api-Key': 'a32fd551-8554-43a5-8eaf-4835079d9c14',
            'X-Tingyun': 'c=B|6jgbXJsLBgM',
            'apiversion': '2.0',
            'appversion': '1.0',
            'dxdeviceid': '6677b200z4EiTeinCIjbqrElZ6jqnAISGT4xCDD4',
            'lmId': '22082948',
            'openid': 'oVvTl5UYrNhqBIBs7HzWOZMEOM94',
            'phone': '17854279565',
            'refer': 'xcx',
            'user-source-channel': '{"mediaId":"","actionId":"source2","channelId":5,"customId":"","campaignId":"","serviceId":"0","serviceType":"cGFnZXMvcHVibGljVmlkZW8vcHVibGljVmlkZW8=","clickId":"","areaId":"","projectId":"","posterId":"","posterOwner":"","posterOwnerId":"","channelProjectId":"","fromActivityId":""}',
            'userId': 'e6319a4b-91b5-4e5d-9860-b5127f10141c',
            'x-authentication-id': 'e6319a4b-91b5-4e5d-9860-b5127f10141c',
            'x-authentication-token': 'dc2e0a19838543563971e373b409b6eb48b4e4fa7e8b7771b5f467bed0be8069ae75ee3b25908627ce1ac4306f1fa90ab78664b5b27b3c4114a500b98c0705b8505f185515f9d8c9fe26a9dc23fc14f5f75ac4268805706fa6c89bb715062fdca21b1125110da99e422424b504c9971d7d3b0ba00b658225a274d731c23534d45566e037e67d069d94665d41a493657be6c21063000ee37480e3a7dff765df59b9547061ac2f4f48251a65c97b49546f9390c87e70335c96794b37f52868cf495026bf28d3c7d1264a67aba310a477fef2bd1d8c58071570953c947b52586cf8b22e6db69c17b8113f1fc09c09f0c0eaab83f17d97440e73419f67c6acca4d73aeb79ca12108de6e74d0d5d3af3cfed8d00843db1ab9a1ee11ad5d0a957e472f9c302753de563e3b353ae953081b31381b2231ff31ccbd5e16f6cf0a66187bfdb1408f6250d1ef0b41197864297f4de8a185c55bc6a5dfecca4499b9c188bed7f4516379aa8a0607088cc3fa7314a61e603a410549bbf3f9d25acb734a2c39c09048b61709f44a76785782e5f19de61fa2293a75d74a8012ac094f62d0e87d69',
            'xweb_xhr': '1',
        }


        json_data = {
            'cityCode': '100000',
        }

        response = requests.post('https://gw2c-hw-open.longfor.com/mzapi-open-prod/web/api/member/info',
                                 headers=headers, json=json_data)
        if not response or response.status_code != 200:
            print("获取用户信息失败")
            return
        response_json = response.json()
        if response_json['errcode'] == '0':
            nickName = response_json['data']["nickName"]
            levelName = response_json['data']["levelName"]
            expiringLz = response_json["data"]["expiringLz"]
            balance = response_json['data']["balance"]
            growthValue = response_json["data"]["growthValue"]
            nextGrowthValue = response_json["data"]["nextGrowthValue"]
            nextLevelGrowthValue = response_json["data"]["nextLevelGrowthValue"]
            print(f'🐶{nickName}')
            print(f'🐹等级: {levelName} | {growthValue}/{nextGrowthValue} | 升至下一级还需要: {nextLevelGrowthValue}成长值')
            print(f'💰龙珠余额: {balance} | 即将过期龙珠: {expiringLz}')
        else:
            print(f'获取用户信息失败: {response_json["errmsg"]}')

    def sign(self):
        response = requests.get('https://vip.ixiliu.cn/mp/sign/applyV2', headers=self.headers)
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['status'] == 200 or response_json['status'] == 500:
            print(f'✅签到成功 | {response_json["message"]}')
        else:
            print(f'❌签到失败：{response_json["message"]}')

    def main(self):
        self.user_info()
        # time.sleep(random.randint(15, 30))
        # self.sign()


if __name__ == '__main__':
    env_name = 'LHYXJ_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = 'dewgfer'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"龙湖U享家共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        LH(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
