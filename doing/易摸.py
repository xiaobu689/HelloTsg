"""
NO易摸

抓任意包请求头 cookie
变量名: NOYM_TOKEN

cron: 35 6 * * *
const $ = new Env("NO易摸");
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class NOYM():
    name = "NO易摸"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Host': '761291517.cms.n.weimob.com',
            'Referer': 'https://761291517.cms.n.weimob.com/bos/cms/761291517/6016606679517/14309763517/design/usercenter',
            'Cookie': self.token,
            'x-wmsdk-close-store': 'v2',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003135) NetType/WIFI Language/zh_CN',
            'x-cmssdk-vidticket': '11641-1718785533.963-saas-w1-1092-32388365885',
            'x-wmsdk-bc': '1 1718785534199',
            'Origin': 'https://761291517.cms.n.weimob.com',
            'Sec-Fetch-Dest': 'empty',
            'weimob-bosId': '4021996812517',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'x-wmsdk-vid': '6016606679517',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'x-cms-sdk-request': '1.5.51',
            'Sec-Fetch-Mode': 'cors',
        }

    def user_info(self):
        json_data = {
            'basicInfo': {
                'vid': 6016606679517,
                'vidType': 2,
                'bosId': 4021996812517,
                'productId': 1,
                'productInstanceId': 14309763517,
                'productVersionId': '36000',
                'merchantId': 2000354510517,
                'cid': 761291517,
                'tcode': 'weimob',
            },
            'extendInfo': {
                'source': 0,
                'channelsource': 5,
                'refer': 'cms-usercenter',
            },
            'queryParameter': None,
            'i18n': {
                'language': 'zh',
                'timezone': '8',
            },
            'targetBasicInfo': {
                'productInstanceId': 14309764517,
            },
            'request': {},
        }

        response = requests.post(
            'https://761291517.cms.n.weimob.com/api3/onecrm/point/myPoint/getSimpleAccountInfo',
            headers=self.headers,
            json=json_data,
        )

        if not response or response.status_code != 200:
            print("获取用户信息失败")
            return
        response_json = response.json()
        print(response_json)
        if response_json['errcode'] == '0':
            print(f'🐶{response_json["data"]["sumTotalPoint"]}积分\n')

    def sign(self):
        json_data = {
            'basicInfo': {
                'vid': 6016606679517,
                'vidType': 2,
                'bosId': 4021996812517,
                'productId': 146,
                'productInstanceId': 14309764517,
                'productVersionId': '10003',
                'merchantId': 2000354510517,
                'cid': 761291517,
                'tcode': 'weimob',
            },
            'extendInfo': {
                'source': 0,
                'channelsource': 5,
            },
            'queryParameter': None,
            'i18n': {
                'language': 'zh',
                'timezone': '8',
            },
            'customInfo': {
                'source': 0,
                'wid': 11179209591,
            },
        }
        response = requests.post(
            'https://761291517.crm.n.weimob.com/api3/onecrm/mactivity/sign/misc/sign/activity/core/c/sign',
            headers=self.headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['errcode'] == 0:
            print(f'✅签到成功 | +{response_json["data"]["fixedReward"]["points"]}')
        else:
            print(f'❌签到失败：{response_json["errmsg"]}')

    def main(self):
        self.user_info()
        time.sleep(random.randint(15, 30))
        self.sign()


if __name__ == '__main__':
    env_name = 'NOYM_TOKEN'
    tokenStr = os.getenv(env_name)
    # tokenStr = 'rprm_appShowId2=-lxkrrrg25b3mnha7hf4; rprm_cuid=8737230478iekkcdlifs; rprm_cuid_time=1718737230478; rprm_session_id=; rprm_uuid=8737230478iekkcdlifs; tgw_l7_route=87c01adfd751837e97228403e5b95cec; bos.h5.session=s%3Aa6wFT0xpa4fN_xnvyFdbZeWoJNm6peic.wQQLQU32b4476CDBtmvfL2lDlXCcGC26EYdg0mww7do'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"NO易摸共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        NOYM(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
