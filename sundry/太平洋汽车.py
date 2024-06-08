"""
太平洋汽车

---------------------------------
20240604 每日抽奖活动结束，新增每日攒碎片开盲盒，可中实物、卡券
20240523 每日抽奖必得现金，自动抽奖自动提现
---------------------------------

APP：太平洋汽车

变量名：tpyqc_data
格式： 账号#密码，多号用 & 隔开

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
from common import make_request, daily_one_word
from sendNotify import send
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class TPYQC():
    name = "太平洋汽车抽奖"

    def __init__(self, account_info):
        username, password = account_info.split('#')
        self.username = username
        self.password = password
        self.account_id = 0
        self.msg = ''
        self.cookie = ''
        self.session_id = ''
        self.contentIds = []
        self.commentId = 0
        self.lotteryCount = 0
        self.myIsues = []
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
        self.loginHeaders = {
            'Host': 'mrobot.pcauto.com.cn',
            'Pc-Agent': 'PCGroup Mobile App',
            'Accept': '*/*',
            'Version': '7.1.4',
            'appVersion': '7.1.4',
            'Accept-Language': 'zh-cn',
            'App': 'PCAUTO_INFO_IOS',
            'platform': 'PCAUTO_INFO_IOS',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }

    def login(self):
        data = {
            'appName': 'PCAUTO_APP',
            'auto_login': '90',
            'password': self.password,
            'username': self.username,
        }
        url = 'https://mrobot.pcauto.com.cn/auto_passport3_back_intf/passport3/rest/login_new.jsp'
        response = requests.post(url, headers=self.loginHeaders, data=data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['status'] == 0:
                self.session = response_json['session']
                self.account_id = response_json['userId']
                common_session_id = response_json["common_session_id"]
                self.cookie = f'common_session_id={common_session_id};'
                self.headers['Cookie'] = self.cookie
                self.communityHeaders['Cookie'] = self.cookie
                print(f"账号【{self.account_id}】登录成功\n")
            else:
                self.msg += f"账号 {self.account_id} 登录失败，原因 {response_json['msg']}\n"

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
                msg = f'✅发帖帖子【{response_json["data"]}】成功'
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
            for item in list:
                contentId = item['contentId']
                self.contentIds.append(int(contentId))

    # 查贴
    def my_issue_list(self):
        params = {
            'accountId': self.account_id,
            'sessionId': self.session_id,
            'pageNo': '1',
            'pageSize': '10',
        }
        url = 'https://community-gateway.pcauto.com.cn/app/user/personContent'
        response = requests.get(url, params=params, headers=self.communityHeaders)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                issue_list = response_json['data']["data"]
                if len(issue_list) == 0:
                    print('🐹空空如也，没有发帖')
                    return
                for item in issue_list:
                    self.myIsues.append(item["issueId"])

    # 删帖
    def delete_issue(self):
        print('🐹开始删帖......')
        if len(self.myIsues) == 0:
            print("🐹没有帖子可以删除")
            return
        print(f'🐹发现{len(self.myIsues)}篇帖子，开始删除......')
        for issueId in self.myIsues:
            json_data = {
                'contentId': issueId,
                'contentType': 'Post',
            }
            url = 'https://community-gateway.pcauto.com.cn/app/user/delete/content'
            response = requests.post(url, headers=self.communityHeaders, json=json_data)
            if response and response.status_code == 200:
                response_json = response.json()
                if response_json['code'] == 200:
                    print(f'✅删除帖子【{issueId}】成功')
                else:
                    print(f'❌删除帖子【{issueId}失败】：{response_json["msg"]}')

    # 评论
    def do_comment(self):
        print('🐹开始评论......')
        id = random.choice(self.contentIds)
        content = daily_one_word()
        if content == '':
            content = '这沿途的风景只能边走边看，陌生人，祝你们万事顺遂'
        json_data = {
            'contentId': id,
            'contentType': 'Post',
            'content': content,
        }
        url = 'https://community-gateway.pcauto.com.cn/app/social/addComment'
        response = requests.post(url, headers=self.communityHeaders, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                comment_id = response_json['data']['id']
                print(f'✅评论成功, 评论ID:{comment_id}')
                self.commentId = comment_id
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
        for i in range(self.lotteryCount):
            url = 'https://community-gateway.pcauto.com.cn/app/lottery/lottery'
            response = requests.post(url, headers=self.communityHeaders)
            if response and response.status_code == 200:
                response_json = response.json()
                if response_json['code'] == 200:
                    print(f'✅第{i + 1}次 | {response_json["data"]["title"]} | {response_json["data"]["rewardName"]}')
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
                print('---------🐹🐹🐹奖品列表🐹🐹🐹---------')
                if len(rewards) == 0:
                    print('❌还没有获得奖励')
                else:
                    for reward in rewards:
                        print(f'✅{reward["name"]}')

    def main(self):
        self.login()
        time.sleep(random.randint(15, 25))

        self.content_list()
        time.sleep(random.randint(15, 25))

        # 发帖
        self.do_topic_issue()
        time.sleep(random.randint(10, 15))

        # 评论
        self.do_comment()
        time.sleep(random.randint(15, 35))

        # 分享
        self.share_task()
        time.sleep(random.randint(15, 35))

        # 抽奖
        self.my_piece_list()
        time.sleep(random.randint(15, 20))
        self.lottery()
        time.sleep(random.randint(15, 20))

        # 删贴|删评论
        self.my_issue_list()
        time.sleep(random.randint(5, 15))
        self.delete_issue()
        time.sleep(random.randint(15, 25))
        self.delete_comment()

        self.my_reward_list()
        time.sleep(random.randint(15, 25))

        # 通知
        # send(title, msg1 + msg2)


if __name__ == '__main__':
    env_name = 'tpyqc_data'
    account_infos_str = os.getenv(env_name)
    if not account_infos_str:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    account_infos = re.split(r'&', account_infos_str)
    print(f"太平洋汽车共获取到{len(account_infos)}个账号")
    for i, account_info in enumerate(account_infos, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        TPYQC(account_info).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
