"""
同程旅行

抓任意包请求头 token
变量名: CST_TOKEN

cron: 12 8 * * *
const $ = new Env("同程旅行");
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


class TCLX():
    name = "城市通"

    def __init__(self, token):
        self.token = token
        self.verify = False
        self.totalScore = 0
        self.taskCode = ''
        self.recordNo = ''
        self.coinTaskCode = ''
        self.coinRecordNo = ''
        self.headers = {
            'authority': 'wx.17u.cn',
            'content-type': 'application/json',
            'referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/637/page-frame.html',
            'sectoken': token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
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

    def user_info(self):
        headers = {
            'authority': 'wx.17u.cn',
            'content-type': 'application/json',
            'referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/637/page-frame.html',
            'sectoken': 'ZfOeS2YX9IStsHx-3-C4u55HGG4a1VzUdjSidLoEmxnzdrLYBr8gIjaaVSgeSx66TNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxKFClixfwReI3NErOq2H1vXMPagVCgb5Gzg8Q1yt0o8A**4641',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
        }

        json_data = {
            'openId': 'o498X0eXH7H5mw5wfFUeTtw6XrbM',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'aesOpenId': 'xTVUJzgpAYKjXXDHQ9w2STLUZDXT6SkXQQ1qem5oRHQ=',
            'aesUnionId': 'CHDyxVWD2s1Mr/hQARDcr6yrm5jhknIXNLG3Qf2Pqs8=',
        }

        response = requests.post('https://wx.17u.cn/appapi/wxUserInfo/getUserInfo', headers=headers, json=json_data)
        if not response and response.status_code != 200:
            print("请求异常：", response.text)
            return
        response_json = response.json()
        if response_json["retCode"] == 0:
            print(f'🐱账户: {response_json["retObj"]["nickName"]}')
        else:
            print("获取用户信息失败：", response_json["retMsg"])

    def point_info(self):
        headers = {
            'authority': 'tcmobileapi.17usoft.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'apmat': 'o498X0eXH7H5mw5wfFUeTtw6XrbM|202406131704|018475',
            'content-type': 'application/json',
            'referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/637/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'tc-mall-client': 'API_CLIENT',
            'tc-mall-dept-code': 'iH3PGf9ZucSMMEYi4keylA==',
            'tc-mall-os-type': 'Android',
            'tc-mall-platform-code': 'WX_MP',
            'tc-mall-user-token': self.token,
            'tcprivacy': '1',
            'tcreferer': 'page%2Fhome%2Fmallassist%2Fmallhome%2Fmall',
            # 'tcsectk': self.token,
            'tcxcxversion': '6.5.3',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }

        params = {
            'acceptLicense': '1',
            'osType': '0',
        }
        response = requests.get(
            'https://tcmobileapi.17usoft.com/mallgatewayapi/userApi/mileages/remain',
            params=params,
            headers=headers,
        )
        if not response and response.status_code != 200:
            print("请求异常：", response.text)
            return
        response_json = response.json()
        if response_json["code"] == 200:
            print(
                f'🐱积分: {response_json["data"]["remainMileageTitle"]} | 等价: {response_json["data"]["deductionPrice"]}元')
        else:
            print("获取积分信息失败：", response_json["msg"])

    def receive_suspend_integral(self):
        headers = {
            'authority': 'wx.17u.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'apmat': 'o498X0eXH7H5mw5wfFUeTtw6XrbM|202406131744|565557',
            'content-type': 'application/json',
            'referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/637/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'tc-mall-platform-code': 'WX_MP',
            'tc-mall-user-token': 'ZfOeS2YX9IStsHx-3-C4u55HGG4a1VzUdjSidLoEmxnzdrLYBr8gIjaaVSgeSx66TNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxKFClixfwReI3NErOq2H1vXMPagVCgb5Gzg8Q1yt0o8A**4641',
            'tcprivacy': '1',
            'tcreferer': 'page%2FAC%2Fsign%2Fmsindex%2Fmsindex',
            'tcsectk': 'ZfOeS2YX9IStsHx-3-C4u55HGG4a1VzUdjSidLoEmxnzdrLYBr8gIjaaVSgeSx66TNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxKFClixfwReI3NErOq2H1vXMPagVCgb5Gzg8Q1yt0o8A**4641',
            'tcxcxversion': '6.5.3',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }

        # 4|历史收益 2|桌面奖励 12|首页来访 7|度假收益 11|社群奖励
        # 12|travelCenter
        json_data = {
            'incomeId': '',
            'type': 12,
            'channelCode': 'travelCenter',
        }

        response = requests.post('https://wx.17u.cn/wxmpsign/home/receiveIncome', headers=headers, json=json_data)
        print("222222222222222222222:", response.text)
        if response.status_code == 200:
            response_json = response.json()
            if response_json["code"] == 200:
                print("领取成功")
            else:
                print("领取失败", response_json["msg"])
        else:
            print("未知错误", response.text)

    # 签到悬浮气泡
    def suspend_integral_list(self):
        type_ids = []
        import requests
        headers = {
            'authority': 'wx.17u.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'apmat': 'o498X0eXH7H5mw5wfFUeTtw6XrbM|202406131758|996956',
            'content-type': 'application/json',
            'referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/637/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'tc-mall-platform-code': 'WX_MP',
            'tc-mall-user-token': 'ZfOeS2YX9IStsHx-3-C4u55HGG4a1VzUdjSidLoEmxnzdrLYBr8gIjaaVSgeSx66TNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxKFClixfwReI3NErOq2H1vXMPagVCgb5Gzg8Q1yt0o8A**4641',
            'tcprivacy': '1',
            'tcreferer': 'page%2FAC%2Fsign%2Fmsindex%2Fmsindex',
            'tcsectk': 'ZfOeS2YX9IStsHx-3-C4u55HGG4a1VzUdjSidLoEmxnzdrLYBr8gIjaaVSgeSx66TNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxKFClixfwReI3NErOq2H1vXMPagVCgb5Gzg8Q1yt0o8A**4641',
            'tcxcxversion': '6.5.3',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }

        json_data = {
            'version': 1,
            'channelCode': '',
        }

        response = requests.post('https://wx.17u.cn/wxmpsign/home/bubble', headers=headers, json=json_data)
        print(response.text)
        if not response and response.status_code != 200:
            return
        response_json = response.json()
        if response_json["code"] == 200:
            list = response_json["data"]["bubbles"]
            for item in list:
                print(f'{item}\n')
                type_ids.append(item["type"])
            print(type_ids)


    # 每日抽奖
    def lottery(self):
        cookies = {
            '__tctmb': '217272534.4204815072036401.1718273729830.1718273744139.12',
            '__tctmc': '217272534.252338255',
            '__tctmd': '217272534.252338255',
            '__tctma': '217272534.1718190554968783.1718190554193.1718256006750.1718273615042.5',
            '__tctmu': '217272534.0.0',
            '__tctmz': '217272534.1718273615042.5.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none)',
            '__tctrack': '0',
            'longKey': '1718190554968783',
            'CooperateTcWxUser': 'CooperateUserId=oOCyauMrN8McvBov2-A7Fn-P6atM&openid=oOCyauMrN8McvBov2-A7Fn-P6atM&MemberId=H9DxzH0N%2fUoKfYX95mXgIQ%3d%3d&token=81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU&MemberSysId=33&Key=YHEW%2fC%2b75WV4GhUCKq5332GzraFYXCsDKujxpGISJc5nnMEX%2fAg6xg%3d%3d&unionid=ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'CooperateWxUser': 'CooperateUserId=oOCyauMrN8McvBov2-A7Fn-P6atM&openid=oOCyauMrN8McvBov2-A7Fn-P6atM&MemberId=H9DxzH0N%2fUoKfYX95mXgIQ%3d%3d&token=81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU&MemberSysId=33&Key=YHEW%2fC%2b75WV4GhUCKq5332GzraFYXCsDKujxpGISJc5nnMEX%2fAg6xg%3d%3d&unionid=ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'TcHomeElInfo': '',
            'WxAppScene': 'wxappscene=1089',
            'WxUser': 'openid=oOCyauMrN8McvBov2-A7Fn-P6atM&token=81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU&userid=H9DxzH0N/UoKfYX95mXgIQ==&unionid=ohmdTt1TSce70l1uL1U2DGcZmGVU&sectoken=ZfOeS2YX9IStsHx-3-C4u0EUvGZ8AWFrUMY9ZOnDcyxvZhv76ID2gHtLqrzQV-593nhEifURu7LSo_espjTiuodztoTIvzEsQgFljpRXreBs6lXHgW54FtHZaOGDZDEZpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYyDx_8emvgaEjCQCJIOfF5ZmThIaY9ysHNjxrrLYAXK3g**4641&refreshtoken=81_i31kLjReSbYP8c585VIsVRkV4dqNJ3OHwtGUJlXiERG4fcPxf9FwIeCr433qOlPPQK19Nz9S3SeCbgj1NyHsz3UUNF86-V4RWSg7bJxwByg&wxtcinfo=S2rQcjjs24Gvx6HJqQtXMPmKzfcYWl%252fR3lhM4SdfekV5t%252f1s9tdhN2fFpwDPdT1nJqebikw9B1JK0lX9Efk0wuFPONK7y30l%252fbJq6%252fIS%252fclrUysf6%252bYu8iDPo%252bb9IRzN',
            'cookieOpenSource': 'openid=oOCyauMrN8McvBov2-A7Fn-P6atM&token=81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU',
            'ASP.NET_SessionId': '0c1st0t2b23yhewdh4mrp5dc',
            'route': '5ab0c3cebdd1b5723181f27cdf5cc159',
        }

        headers = {
            'Host': 'wx.17u.cn',
            # 'Cookie': '__tctmb=217272534.4204815072036401.1718273729830.1718273744139.12; __tctmc=217272534.252338255; __tctmd=217272534.252338255; __tctma=217272534.1718190554968783.1718190554193.1718256006750.1718273615042.5; __tctmu=217272534.0.0; __tctmz=217272534.1718273615042.5.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); __tctrack=0; longKey=1718190554968783; CooperateTcWxUser=CooperateUserId=oOCyauMrN8McvBov2-A7Fn-P6atM&openid=oOCyauMrN8McvBov2-A7Fn-P6atM&MemberId=H9DxzH0N%2fUoKfYX95mXgIQ%3d%3d&token=81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU&MemberSysId=33&Key=YHEW%2fC%2b75WV4GhUCKq5332GzraFYXCsDKujxpGISJc5nnMEX%2fAg6xg%3d%3d&unionid=ohmdTt1TSce70l1uL1U2DGcZmGVU; CooperateWxUser=CooperateUserId=oOCyauMrN8McvBov2-A7Fn-P6atM&openid=oOCyauMrN8McvBov2-A7Fn-P6atM&MemberId=H9DxzH0N%2fUoKfYX95mXgIQ%3d%3d&token=81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU&MemberSysId=33&Key=YHEW%2fC%2b75WV4GhUCKq5332GzraFYXCsDKujxpGISJc5nnMEX%2fAg6xg%3d%3d&unionid=ohmdTt1TSce70l1uL1U2DGcZmGVU; TcHomeElInfo=; WxAppScene=wxappscene=1089; WxUser=openid=oOCyauMrN8McvBov2-A7Fn-P6atM&token=81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU&userid=H9DxzH0N/UoKfYX95mXgIQ==&unionid=ohmdTt1TSce70l1uL1U2DGcZmGVU&sectoken=ZfOeS2YX9IStsHx-3-C4u0EUvGZ8AWFrUMY9ZOnDcyxvZhv76ID2gHtLqrzQV-593nhEifURu7LSo_espjTiuodztoTIvzEsQgFljpRXreBs6lXHgW54FtHZaOGDZDEZpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYyDx_8emvgaEjCQCJIOfF5ZmThIaY9ysHNjxrrLYAXK3g**4641&refreshtoken=81_i31kLjReSbYP8c585VIsVRkV4dqNJ3OHwtGUJlXiERG4fcPxf9FwIeCr433qOlPPQK19Nz9S3SeCbgj1NyHsz3UUNF86-V4RWSg7bJxwByg&wxtcinfo=S2rQcjjs24Gvx6HJqQtXMPmKzfcYWl%252fR3lhM4SdfekV5t%252f1s9tdhN2fFpwDPdT1nJqebikw9B1JK0lX9Efk0wuFPONK7y30l%252fbJq6%252fIS%252fclrUysf6%252bYu8iDPo%252bb9IRzN; cookieOpenSource=openid=oOCyauMrN8McvBov2-A7Fn-P6atM&token=81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU; ASP.NET_SessionId=0c1st0t2b23yhewdh4mrp5dc; route=5ab0c3cebdd1b5723181f27cdf5cc159',
            'userToken': 'ZfOeS2YX9IStsHx-3-C4u0EUvGZ8AWFrUMY9ZOnDcyxvZhv76ID2gHtLqrzQV-593nhEifURu7LSo_espjTiuodztoTIvzEsQgFljpRXreBs6lXHgW54FtHZaOGDZDEZpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYyDx_8emvgaEjCQCJIOfF5ZmThIaY9ysHNjxrrLYAXK3g**4641',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003134) NetType/WIFI Language/zh_CN miniProgram/wx336dcaf6a1ecf632',
            'openId': 'oOCyauMrN8McvBov2-A7Fn-P6atM',
            'Referer': 'https://wx.17u.cn/memberlc/mileageshop/luckyWheel?refid=1486690823&isRdUserId=1&isRefresh=refresh&needwrap=1&wxrefid=null',
            'platformSub': 'WX_MP',
            'userKey': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'Origin': 'https://wx.17u.cn',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            # 'Content-Length': '455',
            'platform': 'WX_MP',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'accountSystem': '1',
            'osType': '1',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=utf-8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
        }

        json_data = {
            'openId': 'oOCyauMrN8McvBov2-A7Fn-P6atM',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'access_token': '81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU',
            'secToken': '81_wFx61YZeksNHBp98sLKp8D_wvZfIxwlMaW1pwhbtiv9256eoBJhcI-akJae9pluZVS8cqBD-_H9pds4t8iJMrqmIheLDxsV5og-uHBPEVTU',
            'osType': 1,
            'onceFlag': True,
            'hostFakeUid': '',
            'playId': 'IXuH79YDGkYNShOZEHy69g==',
            'nickName': '骑狗跨大海',
            'taskNo': '',
        }

        response = requests.post('https://wx.17u.cn/wcrewardshopapiv2/roulette/lottery', cookies=cookies,
                                 headers=headers, json=json_data)
        print(response.text)


    # 收取添加桌面奖励
    def receive_integral_desktop(self):
        headers = {
            'Host': 'wx.17u.cn',
            'Connection': 'keep-alive',
            # 'Content-Length': '745',
            'TCxcxVersion': '6.5.4',
            'TC-MALL-PLATFORM-CODE': 'WX_MP',
            'TCPrivacy': '1',
            'content-type': 'application/json',
            'TCReferer': 'page%2FAC%2Fsign%2Fmsindex%2Fmsindex',
            'TC-MALL-USER-TOKEN': 'ZfOeS2YX9IStsHx-3-C4u8860gYPCWGdNOOveOywDWN9vDae6yYp1vfKE2BcsboSTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxSL8GQrMVbTIZRutBK4_mj6DonvE3sZ478jikU0Ww2TQ**4641',
            'apmat': 'o498X0eXH7H5mw5wfFUeTtw6XrbM|202406132101|962313',
            'TCSecTk': 'ZfOeS2YX9IStsHx-3-C4u8860gYPCWGdNOOveOywDWN9vDae6yYp1vfKE2BcsboSTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxSL8GQrMVbTIZRutBK4_mj6DonvE3sZ478jikU0Ww2TQ**4641',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003134) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/638/page-frame.html',
        }

        json_data = {
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'openId': 'o498X0eXH7H5mw5wfFUeTtw6XrbM',
            'userIcon': 'https://file.40017.cn/img140017cnproduct/touch/pushcode/qiandao/2020a/icon_defaultheader.png',
            'nickName': '匿名好友',
            'isFromWindow': True,
            'version': 7,
            'encryptedData': '90435961c1876ee1255a92a828cbd375c31bd856435eaf30f03646daaa18d277c3b25b34dd7212f842cae20a9329d355101338761d573e9cb0595d1bd509f6928d0829af16cae99d5081b9e358178f40aec4f4a2d00b7e16e395032f59b88c3c7189a1ffc4a7a2fbdc838fd68af07fb19ed0c554626483a3c48afe5af07003a09a467d8887348a878f31048c70478e572948877275e28554364f58d7f7d1eca3e61a31277f39ddd39c8b58822c69331c6b79139f13db1139d09f22f57851918054d55126389044fb4b2d383bc7b6a49c799c927017f39fc8f8258d16fd5eda02cf2bb891c36f0e3a084e6c44a7101102',
        }

        response = requests.post('https://wx.17u.cn/wxmpsign/sign/retrieveDesktopReward', headers=headers,
                                 json=json_data)
        print(response.text)

    def get_task_list(self):
        headers = {
            'Host': 'wx.17u.cn',
            'Connection': 'keep-alive',
            # 'Content-Length': '82',
            'TCxcxVersion': '6.5.4',
            'TCPrivacy': '1',
            'content-type': 'application/json',
            'TCReferer': 'page%2FAC%2Fsign%2Fmsindex%2Fmsindex',
            'wxapp': '0',
            'sectoken': 'ZfOeS2YX9IStsHx-3-C4u8860gYPCWGdNOOveOywDWN9vDae6yYp1vfKE2BcsboSTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxSL8GQrMVbTIZRutBK4_mj6DonvE3sZ478jikU0Ww2TQ**4641',
            'apmat': 'o498X0eXH7H5mw5wfFUeTtw6XrbM|202406132112|083014',
            'TCSecTk': 'ZfOeS2YX9IStsHx-3-C4u8860gYPCWGdNOOveOywDWN9vDae6yYp1vfKE2BcsboSTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxSL8GQrMVbTIZRutBK4_mj6DonvE3sZ478jikU0Ww2TQ**4641',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003134) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/638/page-frame.html',
        }

        json_data = {
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'openId': 'o498X0eXH7H5mw5wfFUeTtw6XrbM',
        }

        response = requests.post('https://wx.17u.cn/wcsign/SignTask/GetTaskList', headers=headers, json=json_data)
        if not response or response.status_code != 200:
            return None
        response_json = response.json()
        if response_json["rspCode"] == 0:
            list = response_json["data"]
            status = ''
            for task in list:
                print(task)
                if task["completeStatus"] == 0:
                    status = "未完成"
                    self.save_action(task["taskId"], task["activityId"], task["taskType"])
                    time.sleep(random.randint(10, 20))
                    self.receive_award_task(task["taskId"])
                    time.sleep(random.randint(10, 20))

    def save_action(self, taskId, activityId, taskType):
        import requests
        headers = {
            'Host': 'wx.17u.cn',
            'Connection': 'keep-alive',
            # 'Content-Length': '190',
            'TCxcxVersion': '6.5.4',
            'TCPrivacy': '1',
            'content-type': 'application/json',
            'TCReferer': 'page%2FAC%2Fsign%2Fmsindex%2Fmsindex',
            'wxapp': '0',
            'sectoken': 'ZfOeS2YX9IStsHx-3-C4u3EeZzJLzPGdrPcDNY0A-SVvTo8pyRDX8KS7S5ph27KMTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxDF2wwoiz1CxB-cHkvVxBJqZO3HwjWoWnXWqhqGSl7QQ**4641',
            'apmat': 'o498X0eXH7H5mw5wfFUeTtw6XrbM|202406132207|058830',
            'TCSecTk': 'ZfOeS2YX9IStsHx-3-C4u3EeZzJLzPGdrPcDNY0A-SVvTo8pyRDX8KS7S5ph27KMTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxDF2wwoiz1CxB-cHkvVxBJqZO3HwjWoWnXWqhqGSl7QQ**4641',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003134) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/638/page-frame.html',
        }

        json_data = {
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'openId': 'o498X0eXH7H5mw5wfFUeTtw6XrbM',
            'taskId': taskId,
            'activityId': activityId,
            'taskType': taskType,
        }

        response = requests.post('https://wx.17u.cn/wcsign/SignTask/SaveTaskAction', headers=headers, json=json_data)
        print("保存动作: ", response.text)


    def receive_award_task(self, taskId):
        headers = {
            'Host': 'wx.17u.cn',
            'Connection': 'keep-alive',
            # 'Content-Length': '126',
            'TCxcxVersion': '6.5.4',
            'TCPrivacy': '1',
            'content-type': 'application/json',
            'TCReferer': 'page%2FAC%2Fsign%2Fmsindex%2Fmsindex',
            'wxapp': '0',
            'sectoken': 'ZfOeS2YX9IStsHx-3-C4uzDBro9bD6tGGP_mI71wqRB9vDae6yYp1vfKE2BcsboSTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYyD0kP1elVlIUJLNeDrfUA0WOyfdWhYsnXFxExmm6ZmOg**4641',
            'apmat': 'o498X0eXH7H5mw5wfFUeTtw6XrbM|202406132149|566761',
            'TCSecTk': 'ZfOeS2YX9IStsHx-3-C4uzDBro9bD6tGGP_mI71wqRB9vDae6yYp1vfKE2BcsboSTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYyD0kP1elVlIUJLNeDrfUA0WOyfdWhYsnXFxExmm6ZmOg**4641',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003134) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/638/page-frame.html',
        }

        json_data = {
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'openId': 'o498X0eXH7H5mw5wfFUeTtw6XrbM',
            'taskId': taskId,
        }

        response = requests.post('https://wx.17u.cn/wcsign/SignTask/ReceiveTaskAward', headers=headers, json=json_data)
        print("任务完成情况：", response.text)


    def sign_cash(self):
        import requests

        headers = {
            'Host': 'wx.17u.cn',
            'Connection': 'keep-alive',
            # 'Content-Length': '460',
            'TC-USER-TOKEN': 'ZfOeS2YX9IStsHx-3-C4u3EeZzJLzPGdrPcDNY0A-SVvTo8pyRDX8KS7S5ph27KMTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxDF2wwoiz1CxB-cHkvVxBJqZO3HwjWoWnXWqhqGSl7QQ**4641',
            'TCxcxVersion': '6.5.4',
            'TC-PLATFORM-CODE': 'WX_MP',
            'TC-OS-TYPE': '1',
            'TCPrivacy': '1',
            'content-type': 'application/json',
            'TCReferer': 'page%2Factivetemplate%2FzqLite%2Findex',
            'apmat': 'o498X0eXH7H5mw5wfFUeTtw6XrbM|202406132231|782453',
            'TCSecTk': 'ZfOeS2YX9IStsHx-3-C4u3EeZzJLzPGdrPcDNY0A-SVvTo8pyRDX8KS7S5ph27KMTNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxDF2wwoiz1CxB-cHkvVxBJqZO3HwjWoWnXWqhqGSl7QQ**4641',
            # 'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003134) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx336dcaf6a1ecf632/638/page-frame.html',
        }

        json_data = {
            'encryptedData': '05239ad6b73fa111b6b67f61e03a7626311d56963e890622cac64925a0e09785bcde02d5470a7bb66c7590ad3c1e8d3aed700c1f2891a17566f6214041d4cda1b139e9088659a8d0e4f16b0280491f777eccf66695c3348abeb61e05f2b216e36f2a49613a2af72ee269dbd30d337d21',
            'iv': 8,
            'headImgUrl': 'https://thirdwx.qlogo.cn/mmopen/vi_32/0dMdN7VsdZsQJvpbOia4qPQr5Lsf6AoYPtliauQ6n1AicjWtEJf6vP88r0gZmBABcbK5icAPmVewCGGPz6ibVs18ZOQ/132',
            'nickName': '骑狗跨大海',
            'shareGuOid': '',
            'shareGuid': '',
        }

        response = requests.post('https://wx.17u.cn/platformflowpool/sign/cash', headers=headers, json=json_data)
        print(response.text)

    def main(self):
        # 签到
        self.sign()
        time.sleep(random.randint(30, 40))

        self.user_info()

        self.point_info()

        self.receive_suspend_integral()
        self.receive_integral_desktop()

        self.suspend_integral_list()
        self.lottery()

        # -----------------------------------\
        self.get_task_list()


        # 每日领现金
        self.sign_cash()


if __name__ == '__main__':
    env_name = 'TCLX_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = 'ZfOeS2YX9IStsHx-3-C4u55HGG4a1VzUdjSidLoEmxnzdrLYBr8gIjaaVSgeSx66TNm3bBq0ymLe2HluCZA4FEyG2HmPsTbvL0Cy8PTaQsAz5qmrMQtiAzhiLhXRsY8WpxPh196mvKyGfXncqS3qw9ETiLz06ENAOtW1BKeyXYxKFClixfwReI3NErOq2H1vXMPagVCgb5Gzg8Q1yt0o8A**4641'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"同程旅行共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        TCLX(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
