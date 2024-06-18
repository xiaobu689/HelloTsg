"""
海天美味馆

抓任意包请求头 Authorization
变量名: HT_TOKEN

cron: 05 6 * * *
const $ = new Env("海天美味馆");
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class HT():
    name = "海天美味馆"

    def __init__(self, token):
        self.token = token
        self.lottery_counts = 0
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': token,
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/599/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'envVersion': 'release',
            'uuid': 'uqfogZeESsqNOFybDTUe',
            'xweb_xhr': '1',
        }

    def user_info(self):
        response = requests.get('https://cmallapi.haday.cn/buyer-api/members', headers=self.headers)
        if not response or response.status_code != 200:
            print("获取用户信息失败")
            return
        response_json = response.json()
        print(f'🐶{response_json["uname"]} | 💰{response_json["consum_point"]}积分\n')

    def sign(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': self.token,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/599/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'envVersion': 'release',
            'uuid': 'uqfogZeESsqNOFybDTUe',
            'xweb_xhr': '1',
        }
        json_data = {
            'activity_code': '202404',
            'fill_date': '',
        }
        url = 'https://cmallapi.haday.cn/buyer-api/sign/activity/sign'
        response = requests.post(url, headers=headers, json=json_data)
        # if not response or response.status_code != 200 or response != 200:
        #     print("签到异常：", response.text)
        #     return
        response_json = response.json()
        if "is_sign" in response_json and response_json['is_sign'] == "true":
            print('✅签到成功')
        elif "code" in response_json and response_json['code'] == '1019':
            print('✅今天已经签到过了')
        else:
            print('❌签到失败')

    def lottery(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': self.token,
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/599/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'envVersion': 'release',
            'uuid': 'uqfogZeESsqNOFybDTUe',
            'xweb_xhr': '1',
        }
        params = {
            'activityCode': 'jfcj0527',
        }
        url = 'https://cmallapi.haday.cn/buyer-api/lucky/activity/extract'
        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        print("-------------------response_json:", response_json)
        if "lucky_record_vo" in response_json and response_json['lucky_record_vo'] is None:
            print("✅抽奖结果 | 谢谢参与")
        else:
            print(
                f'✅{response_json["lucky_record_vo"]["activity_name"]} | 抽奖结果：{response_json["lucky_record_vo"]["prize_name"]}')

    def lottery_task_list(self):
        url = 'https://cmallapi.haday.cn/buyer-api/lucky/task/package/jfcj0527'
        response = requests.get(url, headers=self.headers)
        response_json = response.json()
        list = response_json["task_list"]
        for item in list:
            print(item)
            print(f'🐹{item["task_name"]} | {item["task_content"]}')

    def can_lottery_count(self):
        import requests
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjExODY1NTMsInN1YiI6IkJVWUVSIiwib3BlbklkIjoib2NnNnk0bU5JdlFOQldpTmh0WnI4Q3dPek45RSIsInJvbGVzIjpbIkJVWUVSIl0sImV4cCI6MTcxOTIxMjMyOCwidXVpZCI6InVxZm9nWmVFU3NxTk9GeWJEVFVlIiwidXNlcm5hbWUiOiJtXzkyODUxMzY4NDE3In0.n6BABwVkXjIKg_SOV6Z-J36fqwm7cOZwcZMwgD9lAJq5LMxmD9ioSYj5XJ7rpNYCOTxpchH7STKDTsho5mAUGw',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/599/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'envVersion': 'release',
            'uuid': 'uqfogZeESsqNOFybDTUe',
            'xweb_xhr': '1',
        }

        params = {
            'activityCode': 'jfcj0527',
        }

        url = 'https://cmallapi.haday.cn/buyer-api/lucky/activity/opporturnity'

        response = requests.get(url, params=params, headers=headers)
        if not response or response.status_code != 200:
            print("获取抽奖次数异常：", response.text)
            return
        response_json = response.json()
        can_lottery_count = response_json["can_use"]
        self.lottery_counts = can_lottery_count
        print(f'✅可抽奖次数：{can_lottery_count}')

    def add_router(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjExODY1NTMsInN1YiI6IkJVWUVSIiwib3BlbklkIjoib2NnNnk0bU5JdlFOQldpTmh0WnI4Q3dPek45RSIsInJvbGVzIjpbIkJVWUVSIl0sImV4cCI6MTcxOTIxMjMyOCwidXVpZCI6InVxZm9nWmVFU3NxTk9GeWJEVFVlIiwidXNlcm5hbWUiOiJtXzkyODUxMzY4NDE3In0.n6BABwVkXjIKg_SOV6Z-J36fqwm7cOZwcZMwgD9lAJq5LMxmD9ioSYj5XJ7rpNYCOTxpchH7STKDTsho5mAUGw',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/599/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'envVersion': 'release',
            'uuid': 'uqfogZeESsqNOFybDTUe',
            'xweb_xhr': '1',
        }

        data = {
            'route': 'tpl-module/page-view',
            'identification_id': 'ulY5OwiPmWeFGOdujSlh',
            'explain_information': 'undefined',
            'query': '{"page_type":"jfcj202406","tag":"cjqdtc"}',
        }

        response = requests.post('https://cmallapi.haday.cn/buyer-api/members/statistics/addRouter', headers=headers,
                                 data=data)
        print(response.text)

    def get_view(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjExODY1NTMsInN1YiI6IkJVWUVSIiwib3BlbklkIjoib2NnNnk0bU5JdlFOQldpTmh0WnI4Q3dPek45RSIsInJvbGVzIjpbIkJVWUVSIl0sImV4cCI6MTcxOTIxMjMyOCwidXVpZCI6InVxZm9nWmVFU3NxTk9GeWJEVFVlIiwidXNlcm5hbWUiOiJtXzkyODUxMzY4NDE3In0.n6BABwVkXjIKg_SOV6Z-J36fqwm7cOZwcZMwgD9lAJq5LMxmD9ioSYj5XJ7rpNYCOTxpchH7STKDTsho5mAUGw',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/599/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'envVersion': 'release',
            'uuid': 'uqfogZeESsqNOFybDTUe',
            'xweb_xhr': '1',
        }

        params = {
            'pageUrl': '/points-module/pages/home',
        }

        response = requests.get(
            'https://cmallapi.haday.cn/buyer-api/lucky/task/browse/page/end/jfcj0527',
            params=params,
            headers=headers,
        )
        print(response.text)

    # 积分兑换抽奖机会
    def redeem_lottery_choice(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjExODY1NTMsInN1YiI6IkJVWUVSIiwib3BlbklkIjoib2NnNnk0bU5JdlFOQldpTmh0WnI4Q3dPek45RSIsInJvbGVzIjpbIkJVWUVSIl0sImV4cCI6MTcxOTIxMjMyOCwidXVpZCI6InVxZm9nWmVFU3NxTk9GeWJEVFVlIiwidXNlcm5hbWUiOiJtXzkyODUxMzY4NDE3In0.n6BABwVkXjIKg_SOV6Z-J36fqwm7cOZwcZMwgD9lAJq5LMxmD9ioSYj5XJ7rpNYCOTxpchH7STKDTsho5mAUGw',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/599/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'envVersion': 'release',
            'uuid': 'uqfogZeESsqNOFybDTUe',
            'xweb_xhr': '1',
        }

        params = {
            'activityCode': 'jfcj0527',
        }

        response = requests.get('https://cmallapi.haday.cn/buyer-api/lucky/activity/redeem', params=params,
                                headers=headers)
        print(response.text)

    def get_today_question(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjExODY1NTMsInN1YiI6IkJVWUVSIiwib3BlbklkIjoib2NnNnk0bU5JdlFOQldpTmh0WnI4Q3dPek45RSIsInJvbGVzIjpbIkJVWUVSIl0sImV4cCI6MTcxOTI5MTg4NywidXVpZCI6InVxZm9nWmVFU3NxTk9GeWJEVFVlIiwidXNlcm5hbWUiOiJtXzkyODUxMzY4NDE3In0.7K-8nMbxf7qlwPsE8MnQ7Qe458FlBrz6V3ZxH6m7nJEkLonGwFVx6ipt1eO0oPhXZQLxmV1qGeGWkOeOYG_t-w',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/600/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'envVersion': 'release',
            'uuid': 'uqfogZeESsqNOFybDTUe',
            'xweb_xhr': '1',
        }

        params = {
            'id': '13',
        }

        response = requests.get('https://cmallapi.haday.cn/buyer-api/quiz/getTodayQuizQuestion', params=params,
                                headers=headers)
        if not response or response.json()['code'] != 200:
            print("获取今日题目失败")
            return
        response_json = response.json()
        if response_json['code'] == 200:
            print(f'{response_json["data"]["id"]} | {response_json["data"]["question"]}')

    def question_do_answer(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjExODY1NTMsInN1YiI6IkJVWUVSIiwib3BlbklkIjoib2NnNnk0bU5JdlFOQldpTmh0WnI4Q3dPek45RSIsInJvbGVzIjpbIkJVWUVSIl0sImV4cCI6MTcxOTI5MTg4NywidXVpZCI6InVxZm9nWmVFU3NxTk9GeWJEVFVlIiwidXNlcm5hbWUiOiJtXzkyODUxMzY4NDE3In0.7K-8nMbxf7qlwPsE8MnQ7Qe458FlBrz6V3ZxH6m7nJEkLonGwFVx6ipt1eO0oPhXZQLxmV1qGeGWkOeOYG_t-w',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/600/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'envVersion': 'release',
            'uuid': 'uqfogZeESsqNOFybDTUe',
            'xweb_xhr': '1',
        }
        data = '{}'
        url = 'https://cmallapi.haday.cn/buyer-api/quiz/doAnswer?quiz_id=13&quiz_question_id=25&answer=0,1,2,3'
        response = requests.post(url, headers=headers, data=data)
        response_json = response.json()
        if response_json['code'] == 200:
            print(f'✅答题成功')
        elif response_json['code'] == '601':
            print(f'❌{response_json["message"]}')
        else:
            print(f'❌答题失败')

    def gen_token(self):
        headers = {
            'Host': 'cmallwap.haday.cn',
            'Connection': 'keep-alive',
            'envVersion': 'release',
            'content-type': 'application/json',
            'uuid': 'uiZsYnMG4OcHHmGGpLAZ',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003135) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/600/page-frame.html',
        }

        json_data = {
            'access_token': 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjExODY1NTMsInN1YiI6IkJVWUVSIiwib3BlbklkIjoib2NnNnk0bU5JdlFOQldpTmh0WnI4Q3dPek45RSIsInJvbGVzIjpbIkJVWUVSIl0sImV4cCI6MTcxOTI5MzA5NCwidXVpZCI6InVpWnNZbk1HNE9jSEhtR0dwTEFaIiwidXNlcm5hbWUiOiJtXzkyODUxMzY4NDE3In0.g87pdFvSy4HqWuG6PJTCFcINRftc2-pOlL8zfTXICdqtoJ-mxQY2bP_2rW-MHJsZ-GEvosgw7f6VRA-Fx9pRhg',
        }

        response = requests.post('https://cmallwap.haday.cn/haday/wx/auth/loginByToken', headers=headers,
                                 json=json_data)
        print(response.json())

    def try_task(self):
        # 2|进行中
        params = {
            'page_no': '1',
            'page_size': '10',
            'activity_status': '2',
        }

        response = requests.get('https://cmallapi.haday.cn/buyer-api/promotions/zero/activity/list', params=params,
                                headers=self.headers)
        response_json = response.json()
        list = response_json['data']
        for item in list:
            activity_id = item['activity_id']
            if activity_id == 38:
                print(item)
            tag_id_string, questionnaire_id, goods_name, error_occurred = self.do_try_pre(activity_id)
            if not error_occurred:  # 检查是否发生了错误
                self.do_try(activity_id, tag_id_string, questionnaire_id, goods_name)
            else:
                print("在执行新品试用资料填写时发生了错误，不继续执行新品试用")

    def do_try_pre(self, activity_id):
        response = requests.get(f'https://cmallapi.haday.cn/buyer-api/promotions/zero/activity/{activity_id}',
                                headers=self.headers)
        response_json = response.json()
        questionnaire_id = response_json["questionnaire_id"]
        goods_name = response_json["third_goods_name"]
        question_list = response_json["member_tag_questionnaire_vo"]["member_tag_questions_vo"]
        tag_ids = []
        error_occurred = False
        for item in question_list:
            try:
                member_tag_vos = item.get("member_tag_vos")
                id = random.choice(member_tag_vos)["id"]
                tag_ids.append(str(id))
            except Exception as e:
                error_occurred = True  # 更新错误跟踪变量
                continue

        return ','.join(tag_ids), questionnaire_id, goods_name, error_occurred

    def do_try(self, activityId, tag_id_string, questionnaire_id, goods_name):
        data = {
            'tagId': tag_id_string,
            'fillAnswer': '',
            'activityId': activityId,
            'questionnaireId': questionnaire_id,
            'addrId': '1085384',  # 自己的地址
            'direct': '0',
        }

        response = requests.post('https://cmallapi.haday.cn/buyer-api/promotions/zero/exp/addexprience',
                                 headers=self.headers, data=data)
        response_json = response.json()
        print(response_json)
        if response_json["code"] == '503':
            print(f"{goods_name} | 您已经有一条申请啦")
        elif response_json["status"] == 1:
            print(f"{goods_name} | 申请成功")
        else:
            print(f"{goods_name} | 申请失败")

    def main(self):
        self.user_info()
        self.lottery_task_list()
        time.sleep(random.randint(15, 30))

        # 签到
        self.sign()
        time.sleep(random.randint(15, 30))

        # 浏览
        self.add_router()
        self.get_view()

        # 积分兑换
        for i in range(2):
            self.redeem_lottery_choice()
            time.sleep(random.randint(15, 30))

        print(f"\n======== ▷ 每日抽奖 ◁ ========")
        self.can_lottery_count()
        if int(self.lottery_counts) > 0:
            for i in range(self.lottery_counts):
                self.lottery()
                time.sleep(random.randint(15, 30))
        else:
            print("抽奖次数不足")

        print(f"\n======== ▷ 每日答题 ◁ ========")
        self.get_today_question()
        self.question_do_answer()
        time.sleep(random.randint(15, 30))

        print(f"\n======== ▷ 新品试用 ◁ ========")
        self.try_task()


if __name__ == '__main__':
    env_name = 'HT_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjExODY1NTMsInN1YiI6IkJVWUVSIiwib3BlbklkIjoib2NnNnk0bU5JdlFOQldpTmh0WnI4Q3dPek45RSIsInJvbGVzIjpbIkJVWUVSIl0sImV4cCI6MTcxOTIxMjMyOCwidXVpZCI6InVxZm9nWmVFU3NxTk9GeWJEVFVlIiwidXNlcm5hbWUiOiJtXzkyODUxMzY4NDE3In0.n6BABwVkXjIKg_SOV6Z-J36fqwm7cOZwcZMwgD9lAJq5LMxmD9ioSYj5XJ7rpNYCOTxpchH7STKDTsho5mAUGw'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"海天美味馆共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        HT(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
