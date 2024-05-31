"""
太平洋汽车抽奖

20240523 每日抽奖已废，新增每日开盲盒

APP：太平洋汽车
变量名：tpyqc_cookie
格式： cookie#手机号#openid#devId
任意请求头获取cookie, 默认手动提现，如设置自动提现进入我的钱包-瓜分现金-提现-授权微信，抓包openid和devid

定时设置：
cron: 0 0 * * *
const $ = new Env("太平洋汽车");
"""
import os
import random
import time
import requests
import json

from common import make_request
from sendNotify import send
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class TPYQCIO():
    name = "太平洋汽车抽奖"

    def __init__(self, cookie_str):
        self.msg = ''
        self.contentIds = []
        self.commentId = 0
        parts = cookie_str.split('#')
        self.auto_cash_out = False
        self.cookie = parts[0]
        self.phone = parts[1]
        if len(parts) == 4:
            self.openid = parts[2]
            self.devid = parts[3]
            self.auto_cash_out = True
        self.headers = {
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
        self.communityHeaders = {
            'Host': 'community-gateway.pcauto.com.cn',
            'Pc-Agent': 'PCGroup Mobile App',
            'Version': '7.1.3',
            'Appsession': '7d30da2005b532639b5f2cd3e335cfde79654bb1',
            'Accept': '*/*',
            'appVersion': '7.1.3',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'App': 'PCAUTO_INFO_IOS',
            'platform': 'PCAUTO_INFO_IOS',
            'traceId': '92ZF9',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'common_session_id=E868681D114A85801EB4AC7ED63FB6549BD9D807FE76CEAA86FB059DF81C2CA9157E2E2BD6F4ADF8AE0C982DE164FF39',
        }

    def receice(self):
        url1 = 'https://act1.pcauto.com.cn/discount/api/series/list'
        data1 = json.dumps({"actId": "19"})
        response1 = requests.post(url1, headers=self.headers, data=data1)
        data2 = response1.json()
        first_item = data2['data'][0]
        brand_id = first_item['brandId']
        brand = first_item['brand']
        serial_group_id = first_item['serialGroupId']
        serial_group_name = first_item['serialGroupName']
        serial_group_pic = first_item['serialGroupPic']
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
        url = 'https://act1.pcauto.com.cn/discount/api/enroll/save'
        response = requests.post(url, headers=self.headers, json=data)
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
        data = {
            'devId': self.devid,
            'openId': self.openid,
            'amount': '0.3'
        }
        response = requests.post(url, headers=self.headers, json=data)
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

    # 发帖
    def do_topic_issue(self):
        msg = ''
        json_data = {
            'clubTags': [
                '799579643900329987',
            ],
            'content': '坚持打卡，加油加油',
            'title': '',
            'themeTags': [
                '804483405201802908',
            ],
            'images': [
                {
                    'url': 'http://img4.pcauto.com.cn/pcauto/images/community/20240531/20616066.jpg',
                    'width': 1170,
                    'height': 2097,
                },
            ],
        }
        url = 'https://community-gateway.pcauto.com.cn/app/topic/issue'
        response = requests.post(url, headers=self.communityHeaders, json=json_data, verify=False)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                msg = f'✅发帖成功'
            else:
                msg = f'❌发帖失败：{response_json["msg"]}'
        else:
            msg = '❌发帖失败，请检查网络'

        self.msg += msg
        print(msg)

    def content_list(self):
        headers = {
            'Host': 'community-gateway.pcauto.com.cn',
            'Accept': '*/*',
            'Appsession': '7d30da2005b532639b5f2cd3e335cfde79654bb1',
            'Version': '7.1.4',
            'appVersion': '7.1.4',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'App': 'PCAUTO_INFO_IOS',
            'platform': 'PCAUTO_INFO_IOS',
            'traceId': 'R7465',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Connection': 'keep-alive',
            'Pc-Agent': 'PCGroup Mobile App',
            'Cookie': 'common_session_id=E868681D114A85801EB4AC7ED63FB6549BD9D807FE76CEAA86FB059DF81C2CA9157E2E2BD6F4ADF8AE0C982DE164FF39',
        }
        params = {
            'firstPageTime': '1717179455000',
            'id': '1',
            'isSuperior': 'false',
            'orderType': '0',
            'pageNo': '1',
            'pageSize': '10',
            'tagType': 'Club',
        }
        url = 'https://community-gateway.pcauto.com.cn/app/tags/contentList'
        response = requests.get(url, params=params, headers=headers)
        if response and response.status_code == 200:
            response_json = response.json()
            list = response_json['data']["data"]
            print(list)
            for item in list:
                contentId = item['contentId']
                content = item['appContent']


    # 查贴
    def issue_list(self):
        params = {
            'accountId': '52792536',
            'sessionId': 'E868681D114A85801EB4AC7ED63FB6549BD9D807FE76CEAA86FB059DF81C2CA9157E2E2BD6F4ADF8AE0C982DE164FF39',
            'pageNo': '1',
            'pageSize': '10',
        }

        response = requests.get('https://community-gateway.pcauto.com.cn/app/user/personContent', params=params, headers=self.communityHeaders)
        if response and response.status_code == 200:
            response_json = response.json()
            list = response_json['data']["data"]
            for item in list:
                self.contentIds.append(item['contentId'])
            # print("self.contentids=",self.contentIds)
        else:
            print('❌获取发帖列表失败，请检查网络')

    # 删帖
    def delete_issue(self):
        if len(self.contentIds) == 0:
            print("没有帖子可以删除")
            return
        print(f'发现{len(self.contentIds)}篇帖子，开始删除......')
        for contentId in self.contentIds:
            json_data = {
                'contentId': contentId,
                'contentType': 'Post',
            }
            url = 'https://community-gateway.pcauto.com.cn/app/user/delete/content'
            response = requests.post(url, headers=self.communityHeaders, json=json_data)
            if response and response.status_code == 200:
                response_json = response.json()
                if response_json['code'] == 200:
                    print(f'✅删除帖子{contentId}成功')
                else:
                    print(f'❌删除帖子{contentId}失败：{response_json["msg"]}')

    def do_comment(self):
        json_data = {
            'contentId': 807919694839284780,
            'contentType': 'Post',
            'content': '城市待久了，这风景看着都心情舒畅',
        }
        url = 'https://community-gateway.pcauto.com.cn/app/social/addComment'
        response = requests.post(url, headers=self.communityHeaders, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'✅评论成功')
            else:
                print(f'❌评论失败：{response_json["msg"]}')

    def delete_comment(self):
        if self.commentId == 0:
            print("没有评论可以删除")
            return
        json_data = {
            'id': self.commentId
        }
        url = 'https://community-gateway.pcauto.com.cn/app/social/delComment'
        response = requests.post(url, headers=self.communityHeaders, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'✅删除评论{self.commentId}成功')
            else:
                print(f'❌删除评论{self.commentId}失败：{response_json["msg"]}')

    def lottery(self):
        headers = {
            'Host': 'community-gateway.pcauto.com.cn',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218fcde0d3c711cf-00fb5d5704d89958-774c1151-329160-18fcde0d3c82846%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmY2RlMGQzYzcxMWNmLTAwZmI1ZDU3MDRkODk5NTgtNzc0YzExNTEtMzI5MTYwLTE4ZmNkZTBkM2M4Mjg0NiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218fcde0d3c711cf-00fb5d5704d89958-774c1151-329160-18fcde0d3c82846%22%7D; u4ad=10ehi2gv; channel=11496; pcsuv=1717146016471.a.717876525; pcuvdata=lastAccessTime=1717146015611|visits=1; sajssdk_2015_cross_new_user=1; common_session_id=E868681D114A85801EB4AC7ED63FB6549BD9D807FE76CEAA86FB059DF81C2CA9157E2E2BD6F4ADF8AE0C982DE164FF39',
            'Origin': 'https://m.pcauto.com.cn',
            'SessionId': 'E868681D114A85801EB4AC7ED63FB6549BD9D807FE76CEAA86FB059DF81C2CA9157E2E2BD6F4ADF8AE0C982DE164FF39',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/PCAutoApp',
            'Referer': 'https://m.pcauto.com.cn/',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin-Type': '*',
            'Sec-Fetch-Dest': 'empty',
        }
        url = 'https://community-gateway.pcauto.com.cn/app/lottery/lottery'
        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'✅{response_json["data"]["title"]}, 奖品：{response_json["data"]["rewardName"]}')
            else:
                print(f'❌抽奖失败：{response_json["msg"]}')





    def main(self):
        # title = "太平洋汽车每日抽奖"
        # msg1 = self.start_receiving()
        # if self.auto_cash_out:
        #     time.sleep(random.randint(15, 20))
        #     msg2 = self.cashOut()
        # else:
        #     msg2 = f'❌余额不足，先不提现，再攒攒吧！\n'
        #     print(msg2)
        #
        # print(msg1 + msg2)

        # self.do_topic_issue()

        # self.issue_list()

        self.content_list()

        # 通知
        # send(title, msg1 + msg2)


if __name__ == '__main__':
    env_name = 'tpyqc_cookie'
    cookie = os.getenv(env_name)
    cookie = 'pcsuv=1715211510009.a.33360290; channel=10927; common_session_id=E868681D114A85801EB4AC7ED63FB6549BD9D807FE76CEAA86FB059DF81C2CA9157E2E2BD6F4ADF8AE0C982DE164FF39; pcuvdata=lastAccessTime=1715211507667; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218f5a92964aa07-0270717f313bc4c-774c1151-329160-18f5a92964baf9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmNWE5Mjk2NGFhMDctMDI3MDcxN2YzMTNiYzRjLTc3NGMxMTUxLTMyOTE2MC0xOGY1YTkyOTY0YmFmOSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218f5a92964aa07-0270717f313bc4c-774c1151-329160-18f5a92964baf9%22%7D#1055239575#oFOGvjhieYfIbabUXNZHLaZNsXRE#7d30da2005b532639b5f2cd3e335cfde79654bb1'
    if not cookie:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    TPYQCIO(cookie).main()
