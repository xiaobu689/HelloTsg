"""
CK测活

cron: */10 * * * *

const $ = new Env("CK测活");
"""


import requests
from sendNotify import send


def TCLX():
    headers = {
        'authority': 'wx.17u.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apmat': 'o498X0eXH7H5mw5wfFUeTtw6XrbM|202406182226|927738',
        'content-type': 'application/json',
        'referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/639/page-frame.html',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sectoken': 'ZfOeS2YX9IStsHx-3-C4uxbmAms8Bwph9r2lmbVUD-eFW-PtV2ue9FyE2o2YihOuTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYwt4YZL_Qpw_L7XjlVDqkhJs3wYZfKsfi2TEqA_NwPplw**4641',
        'tcprivacy': '1',
        'tcreferer': 'page%2Fhome%2Fmy%2Fmy',
        'tcsectk': 'ZfOeS2YX9IStsHx-3-C4uxbmAms8Bwph9r2lmbVUD-eFW-PtV2ue9FyE2o2YihOuTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYwt4YZL_Qpw_L7XjlVDqkhJs3wYZfKsfi2TEqA_NwPplw**4641',
        'tcxcxversion': '6.5.5',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
        'xweb_xhr': '1',
    }
    json_data = {
        'openId': 'o498X0eXH7H5mw5wfFUeTtw6XrbM',
        'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
        'aesOpenId': 'xTVUJzgpAYKjXXDHQ9w2STLUZDXT6SkXQQ1qem5oRHQ=',
        'aesUnionId': 'CHDyxVWD2s1Mr/hQARDcr6yrm5jhknIXNLG3Qf2Pqs8=',
    }
    url = 'https://wx.17u.cn/appapi/wxUserInfo/getUserInfo'
    response = requests.post(url, headers=headers, json=json_data)
    if not response and response.status_code != 200:
        print("请求异常：", response.text)
        send("同程旅行测活", "请求异常：" + response.text)
        return
    response_json = response.json()
    if response_json["retCode"] == 0:
        print(f'🐱账户: {response_json["retObj"]["nickName"]}')
    else:
        send("同程旅行测活检测", "获取用户信息失败，CK已失效")
        print("获取用户信息失败：", response_json["retMsg"])


if __name__ == '__main__':
    TCLX()

