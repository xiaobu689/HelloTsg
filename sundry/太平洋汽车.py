"""
太平洋汽车抽奖

---------------------------------
20240523 每日抽奖已废，新增每日开盲盒
---------------------------------

APP：太平洋汽车
变量名：tpyqc_cookie
格式： cookie#account_id
任意请求头获取cookie和account_id

定时设置：
cron: 0 0 * * *
const $ = new Env("太平洋汽车");
"""
import os
import random
import re
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
        parts = cookie_str.split('#')
        cookie = parts[0]
        self.cookie = cookie
        self.session_id = cookie.split('; ')[2].split('=')[1]
        self.account_id = parts[1]
        self.contentIds = []
        self.commentId = 0
        self.lotteryCount = 0
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
            'Accept': '*/*',
            'appVersion': '7.1.3',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'App': 'PCAUTO_INFO_IOS',
            'platform': 'PCAUTO_INFO_IOS',
            'traceId': '92ZF9',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': self.cookie
        }

    # 发帖
    def do_topic_issue(self):
        print('开始发帖......')
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
        current_time_millis = int(time.time() * 1000)
        params = {
            'firstPageTime': current_time_millis,
            'id': '1',
            'isSuperior': 'false',
            'orderType': '0',
            'pageNo': '1',
            'pageSize': '10',
            'tagType': 'Club',
        }
        url = 'https://community-gateway.pcauto.com.cn/app/tags/contentList'
        response = requests.get(url, params=params, headers=self.communityHeaders)
        if response and response.status_code == 200:
            response_json = response.json()
            list = response_json['data']["data"]
            print(list)
            for item in list:
                contentId = item['contentId']
                content = item['appContent']
                self.contentIds += int(contentId)

    # 查贴
    def my_issue_list(self):
        params = {
            'accountId': self.account_id,
            'sessionId': self.session_id,
            'pageNo': '1',
            'pageSize': '10',
        }
        response = requests.get('https://community-gateway.pcauto.com.cn/app/user/personContent', params=params,
                                headers=self.communityHeaders)
        if response and response.status_code == 200:
            response_json = response.json()
            list = response_json['data']["data"]
            for item in list:
                self.contentIds.append(item['contentId'])
        else:
            print('❌获取发帖列表失败，请检查网络')

    # 删帖
    def delete_issue(self):
        print('🐹开始删帖......')
        if len(self.contentIds) == 0:
            print("🐹没有帖子可以删除")
            return
        print(f'🐹发现{len(self.contentIds)}篇帖子，开始删除......')
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

    # 评论
    def do_comment(self):
        print('🐹开始评论......')
        # 随机从content_ids中随机取一个id
        id = random.choice(self.contentIds)
        json_data = {
            'contentId': id,
            'contentType': 'Post',
            'content': '城市待久了，这风景看着都心情舒畅',
        }
        url = 'https://community-gateway.pcauto.com.cn/app/social/addComment'
        response = requests.post(url, headers=self.communityHeaders, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'✅评论成功')
                print("----------评论id=", response_json["data"]["id"])
                self.commentId = response_json['data']['id']
                print("----------赋值后的self的评论id=", response_json["data"]["id"])
            else:
                print(f'❌评论失败：{response_json["msg"]}')

    def delete_comment(self):
        print('🐹开始删评论......')
        if self.commentId == 0:
            print("🐹没有评论可以删除")
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

    def share_task(self):
        print('🐹开始分享......')
        url = 'https://community-gateway.pcauto.com.cn/app/lottery/share/record'
        response = requests.post(url, headers=self.communityHeaders)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'✅分享成功')
            else:
                print(f'❌分享失败：{response_json["msg"]}')

    def lottery(self):
        print('🐹开始抽奖......')
        if self.lotteryCount == 0:
            print("❌没有抽奖次数")
            return
        url = 'https://community-gateway.pcauto.com.cn/app/lottery/lottery'
        response = requests.post(url, headers=self.communityHeaders)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'✅{response_json["data"]["title"]} | {response_json["data"]["rewardName"]}')
            else:
                print(f'❌抽奖失败：{response_json["msg"]}')

    def my_piece_list(self):
        json_data = {
            'date': None,
            'pageNo': 1,
            'pageSize': 10,
        }
        url = 'https://community-gateway.pcauto.com.cn/app/lottery/piece/list'
        response = requests.post(url, headers=self.communityHeaders, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                remain_pieces = response_json["data"]["pieceRecordStatistic"]["remain"]
                self.lotteryCount = remain_pieces // 3
                print(f'✅碎片：{remain_pieces} | ✅抽奖次数：{self.lotteryCount}')

    def my_reward_list(self):
        params = {
            'type': 'real',
            'pageNo': '1',
            'pageSize': '10',
        }
        url = 'https://community-gateway.pcauto.com.cn/app/lottery/my/reward'
        response = requests.get(url, params=params, headers=self.communityHeaders)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                rewards = response_json["data"]["data"]
                if len(rewards) == 0:
                    print('❌还没有获得奖励')
                else:
                    for reward in rewards:
                        print('--------------------')
                        print('🐹🐹🐹奖品列表🐹🐹🐹')
                        print('--------------------')
                        print(f'✅{reward["name"]}')

    def main(self):
        self.content_list()
        time.sleep(random.randint(15, 25))

        # 发帖
        self.do_topic_issue()
        time.sleep(random.randint(30, 60))

        # 评论
        self.do_comment()
        time.sleep(random.randint(15, 35))

        # 分享
        self.share_task()
        time.sleep(random.randint(15, 35))

        # 抽奖
        self.my_piece_list()
        self.lottery()
        time.sleep(random.randint(15, 45))

        # 删贴|删评论
        self.my_issue_list()
        time.sleep(random.randint(15, 25))
        self.delete_issue()

        time.sleep(random.randint(15, 25))
        self.delete_comment()

        self.my_reward_list()
        time.sleep(random.randint(15, 25))

        # 通知
        # send(title, msg1 + msg2)


if __name__ == '__main__':
    env_name = 'tpyqc_cookie'
    cookies = os.getenv(env_name)
    if not cookies:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    cookies = re.split(r'&', cookies)
    print(f"太平洋汽车共获取到{len(cookies)}个账号")
    for i, cookie in enumerate(cookies, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        TPYQCIO(cookie).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
