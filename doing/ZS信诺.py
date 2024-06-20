"""
ZS信诺

抓任意包请求头 Authorization
变量名: ZSXN_TOKEN

cron: 0 0 * * *
const $ = new Env("ZS信诺");
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class ZSXN():
    name = "ZS信诺"

    def __init__(self, token):
        self.token = token
        self.lottery_count = 0
        self.headers = {
            'authority': 'vip.ixiliu.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'access-token': token,
            'content-type': 'application/json;charset=utf-8',
            'platform': 'MP-WEIXIN',
            'referer': 'https://servicewechat.com/wx9a2dc52c95994011/91/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sid': '10009',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }

    def user_info(self):
        response = requests.get('https://vip.ixiliu.cn/mp/user/info', headers=self.headers)
        if not response or response.status_code != 200:
            print("获取用户信息失败")
            return
        response_json = response.json()
        if response_json['code'] == 0:
            print(
                f'🐶{response_json["data"]["userInfo"]["mobile"]} | 💰{response_json["data"]["userInfo"]["points_total"]}积分\n')

    def sign(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'userId': '7181805',
            'Referer': 'https://hms.cignacmb.com/wmpages/app-rest/module/activity.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            #'Cookie': 'GPHMS=SV-HMS-80-01; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190351a9974169-0654e9748451c04-2702704-329160-190351a997623e%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMzUxYTk5NzQxNjktMDY1NGU5NzQ4NDUxYzA0LTI3MDI3MDQtMzI5MTYwLTE5MDM1MWE5OTc2MjNlIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22190351a9974169-0654e9748451c04-2702704-329160-190351a997623e%22%7D',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'X-Request-Platform': 'web',
            'X-Device-Id': '163CBC75-91C1-4DC0-8EA4-C3286B29C51E',
            'Origin': 'https://hms.cignacmb.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            # 'Content-Length': '0',
            'X-Request-Version': '5.24.10',
            'Connection': 'keep-alive',
            'Authorization': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Sec-Fetch-Mode': 'cors',
        }

        response = requests.post('https://hms.cignacmb.com/activity/appCheck/appCheckIn', headers=headers)
        print(response.text)
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            print(f'✅签到成功')
        else:
            print(f'❌签到失败：{response_json["msg"]}')

    def init_lottery(self):
        headers = {
            'Host': 'member.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://member.cignacmb.com',
            # 'Content-Length': '12',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://member.cignacmb.com/mb-web/shop/mod/index.html?appVersion=5.24.10',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': 'GPMEM80=SV-MEM-80-01; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219035b17be321ca-0dcea045abdc528-2702704-329160-19035b17be41903%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMzViMTdiZTMyMWNhLTBkY2VhMDQ1YWJkYzUyOC0yNzAyNzA0LTMyOTE2MC0xOTAzNWIxN2JlNDE5MDMifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219035b17be321ca-0dcea045abdc528-2702704-329160-19035b17be41903%22%7D; requestChannel=GHB',
        }

        data = {
            'param': 'e30=',
        }

        response = requests.post(
            'https://member.cignacmb.com/shop/member/interface/initPointsDraw',
            headers=headers,
            data=data,
        )
        print(response.text)
        if not response or response.status_code != 200:
            print("抽奖基础信息异常：", response.text)
            return
        response_json = response.json()
        if response_json['respCode'] == '00':
            lottery_count = response_json['respData']['lotteryCount']
            self.lottery_count = lottery_count
            print(f'现有积分: {response_json["respData"]["integral"]} | 今日剩余抽奖次数: {lottery_count}')
        else:
            print(f'❌抽奖失败基础信息获取失败：{response_json["respDesc"]}')

    def do_lottery(self):
        headers = {
            'Host': 'member.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://member.cignacmb.com',
            # 'Content-Length': '12',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://member.cignacmb.com/mb-web/shop/mod/index.html?appVersion=5.24.10',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': 'GPMEM80=SV-MEM-80-01; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219035b17be321ca-0dcea045abdc528-2702704-329160-19035b17be41903%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMzViMTdiZTMyMWNhLTBkY2VhMDQ1YWJkYzUyOC0yNzAyNzA0LTMyOTE2MC0xOTAzNWIxN2JlNDE5MDMifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219035b17be321ca-0dcea045abdc528-2702704-329160-19035b17be41903%22%7D; requestChannel=GHB',
        }

        data = {
            'param': 'e30=',
        }

        response = requests.post(
            'https://member.cignacmb.com/shop/member/interface/doPointsDraw',
            headers=headers,
            data=data,
        )
        print(response.text)
        if not response or response.status_code != 200:
            print("抽奖异常：", response.text)
            return
        response_json = response.json()
        if response_json['respCode'] == '00':
            print(f'✅抽奖成功 | 抽奖结果: {response_json["respData"]["prizeName"]}')
        else:
            print(f'❌抽奖失败：{response_json["respDesc"]}')

    def points_info(self):
        headers = {
            'Host': 'member.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://member.cignacmb.com',
            # 'Content-Length': '12',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://member.cignacmb.com/mb-web/shop/mod/?appVersion=5.24.10',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': 'GPMEM80=SV-MEM-80-01; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219035b59f4c197f-027101559d408b6-2702704-329160-19035b59f4d23b2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMzViNTlmNGMxOTdmLTAyNzEwMTU1OWQ0MDhiNi0yNzAyNzA0LTMyOTE2MC0xOTAzNWI1OWY0ZDIzYjIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219035b59f4c197f-027101559d408b6-2702704-329160-19035b59f4d23b2%22%7D; requestChannel=GHB',
        }

        data = {
            'param': 'e30=',
        }

        response = requests.post(
            'https://member.cignacmb.com/shop/member/interface/queryScoreStatisticsMonth',
            headers=headers,
            data=data,
        )
        print(response.text)
        if not response or response.status_code != 200:
            print('获取积分信息失败')
            return
        response_json = response.json()
        if response_json['respCode'] == '00':
            print(
                f'💰总积分: {response_json["respData"]["totalScore"]} | 💰已使用积分: {response_json["respData"]["expenseScore"]}')
        else:
            print(f'获取积分信息失败: {response_json["respDesc"]}')

    # def user_info(self):

    def user_task_list(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Authorization': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'userId': '7181805',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'Connection': 'keep-alive',
            # 'Cookie': 'GPHMS=SV-HMS-80-02; live800_userid=8890359000; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22889060107244%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_latest_iq_id%22%3A%22APPZY%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMzVkOTFmMmMyMzAtMDczMmEzNWNjNzJlNmM4LTI3MDI3MDQtMzI5MTYwLTE5MDM1ZDkxZjJlN2NkIiwiJGlkZW50aXR5X2Fub255bW91c19pZCI6Ijg4OTA2MDEwNzI0NCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219035d91f2c230-0732a35cc72e6c8-2702704-329160-19035d91f2e7cd%22%7D; sajssdk_2015_cross_new_user=1',
            'Sec-Fetch-Dest': 'empty',
        }

        response = requests.get('https://hms.cignacmb.com/activity/cignaInvestment/getUserTaskList', headers=headers)
        if not response or response.status_code != 200:
            print('获取任务列表失败')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            list = response_json['data']['allTask']
            return list
        else:
            return None

    def get_task_recordId(self, taskCode):
        recordId = 0
        list = self.user_task_list()
        for task in list:
            if task['taskCode'] == taskCode:
                recordId = task['recordId']
                break
        return recordId

    def do_candy_task(self):
        list = self.user_task_list()
        if list is None:
            return
        for task in list:
            # 如果实名认证和完善资料则跳过
            if task['taskName'] == '实名认证' or task['taskName'] == '完善个人信息':
                continue
            # 执行任务
            # -1|待完成， 1|已完成
            if task['status'] != -1:
                continue
            self.update_task_status(task["taskCode"])
            time.sleep(random.randint(15, 20))
            recordId = self.get_task_recordId(task["taskCode"])
            if recordId != 0:
                self.receive_candy(recordId)

    def update_task_status(self, taskCode):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'userId': '7181805',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Origin': 'https://hms.cignacmb.com',
            # 'Content-Length': '12',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': 'GPHMS=SV-HMS-80-02; live800_userid=8890359000; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22889060107244%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_latest_iq_id%22%3A%22APPZY%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMzVkOTFmMmMyMzAtMDczMmEzNWNjNzJlNmM4LTI3MDI3MDQtMzI5MTYwLTE5MDM1ZDkxZjJlN2NkIiwiJGlkZW50aXR5X2Fub255bW91c19pZCI6Ijg4OTA2MDEwNzI0NCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219035d91f2c230-0732a35cc72e6c8-2702704-329160-19035d91f2e7cd%22%7D; sajssdk_2015_cross_new_user=1',
        }

        data = {
            'taskCode': taskCode,
        }

        response = requests.post(
            'https://hms.cignacmb.com/activity/cignaInvestmentTask/updateTaskStatus', headers=headers, data=data)
        if not response or response.status_code != 200:
            print('更新任务状态异常')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            print('更新任务状态成功')
        else:
            print('更新任务状态失败')

    def receive_candy(self, recordId):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'userId': '7181805',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Origin': 'https://hms.cignacmb.com',
            # 'Content-Length': '17',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': 'GPHMS=SV-HMS-80-02; live800_userid=8890359000; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22889060107244%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_latest_iq_id%22%3A%22APPZY%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMzVkOTFmMmMyMzAtMDczMmEzNWNjNzJlNmM4LTI3MDI3MDQtMzI5MTYwLTE5MDM1ZDkxZjJlN2NkIiwiJGlkZW50aXR5X2Fub255bW91c19pZCI6Ijg4OTA2MDEwNzI0NCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219035d91f2c230-0732a35cc72e6c8-2702704-329160-19035d91f2e7cd%22%7D; sajssdk_2015_cross_new_user=1',
        }

        data = {
            'recordId': recordId,
        }

        response = requests.post(
            'https://hms.cignacmb.com/activity/cignaInvestment/receiveCandy', headers=headers, data=data)
        if not response or response.status_code != 200:
            print('领取糖果异常')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            print(f'领取糖果成功 | 糖果+{response_json["data"]["disposableCandyNum"]}')
        else:
            print('领取糖果失败，', response_json['msg'])

    def main(self):
        # self.user_info()
        # time.sleep(random.randint(15, 30))
        self.points_info()
        self.init_lottery()

        # 每日签到
        self.sign()
        time.sleep(random.randint(15, 20))

        # 糯米转盘
        # for i in range(self.lottery_count):
        #     self.do_lottery()
        #     time.sleep(random.randint(15, 20))

        # 一诺庄园
        self.do_candy_task()


if __name__ == '__main__':
    env_name = 'JSB_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"ZS信诺共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        ZSXN(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
