"""
上海黄浦

抓任意包请求头 token
变量名: SHHP_TOKEN

cron: 33 15 * * *
const $ = new Env("上海黄浦");
"""
import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

from common import qianwen_messages, make_request

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class SHHP():
    name = "上海黄浦"

    def __init__(self, account_info):
        self.token = account_info.split('#')[0]
        self.isComment = account_info.split('#')[1]
        self.verify = False
        self.play_ids = []
        self.play_comment_ids = []
        self.headers = {
            'Host': 'hpapi.shmedia.tech',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'token': self.token,
            'Content-Type': 'application/json; charset=utf-8',
            'deviceId': 'af223dabdc3b484c8eae7809f6da7ba6',
            'User-Agent': 'StandardApplication/6.2.7 (iPhone; iOS 16.6; Scale/3.00)',
            'Connection': 'keep-alive'
        }

    def login_score(self):
        json_data = {}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/points/login/add'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        # print(response)
        if response and response['code'] == 0:
            print("登录任务执行成功")

    def sign(self):
        json_data = {}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/personal/score/sign'
        response = make_request(url, json_data, 'post', self.headers)
        # print(response)
        if response and response['code'] == 0:
            print(f'✅{response["data"]["title"]}')
        else:
            print(f'❌{response["msg"]}')

    def total_score(self):
        json_data = {}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/personal/score/total'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print(f'✅当前总积分：{response["data"]["score"]}')
        else:
            print(f'❌总积分获取失败：{response}')

    def today_score(self):
        json_data = {}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/personal/score/info'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print(f'✅今日新增积分：{response["data"]["todayIncreasePoint"]}')
            # return response["data"]["jobs"]
        else:
            print(f'❌今日积分获取失败：{response}')

    def task_list(self):
        json_data = {}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/personal/score/info'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print("-----------------------")
            print(f'🐹🐹🐹任务列表🐹🐹🐹')
            print("-----------------------")
            for i in response['data']['jobs']:
                if "完善个人资料" in i["title"] or "填写邀请码" in i["title"]:
                    continue
                print(f'👻{i["title"]}: {"已完成" if i["status"] == "1" else "未完成"}')

    def article_list(self):
        json_data = {
            'orderBy': 'release_desc',
            'channel': {
                'id': 'ed5f1618a5274c43a8e33478f5f01515',
            },
            'pageSize': 50,
            'pageNo': 1,
        }
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/news/content/list'
        response = make_request(url, json_data, 'post', self.headers)

        return response["data"]["records"]

    def article_read_points_add(self):
        json_data = {}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/points/read/add'
        make_request(url, json_data, 'post', self.headers)

    def article_count_usage_desc(self, id):
        json_data = {
            'id': id,
            'countType': 'contentRead',
        }
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/common/count/usage/inc'
        make_request(url, json_data, 'post', self.headers)

    def article_content(self, id):
        json_data = {'id': id}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/news/content/get'
        response = make_request(url, json_data, 'post', self.headers)
        return response

    def article_read(self, id):
        response = self.article_content(id)
        if response and response['code'] == 0:
            self.article_read_points_add()
            self.article_count_usage_desc(id)
            print(f'✅文章阅读成功')
        else:
            print(f'❌阅读失败，{response}')


    def article_favor(self, id):
        json_data = {'id': id}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/news/content/favor'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print(f'✅文章收藏成功')
        else:
            print(f'❌收藏失败，{response}')

    def article_favor_task(self, id):
        response_content = self.article_content(id)
        if response_content and response_content['code'] == 0:
            if response_content['data']['count']["favorite"] is False:
                self.article_favor(id)
            elif response_content['data']['count']["favorite"]:
                print(f'已经收藏过了，不再重复收藏')
            else:
                print(f'❌收藏失败，{response_content}')
        else:
            print(f'❌获取文章失败，{response_content}')

    def article_share(self, id):
        json_data = {}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/points/share/add'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print(f'✅文章分享成功')
        else:
            print(f'❌文章分享失败，{response}')

    def video_view_task(self):
        json_data = {}
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/points/video/add'
        response = requests.post(url, headers=self.headers, json=json_data, verify=self.verify).json()
        if response and response['code'] == 0:
            print(f'✅看片儿完成+1')
        else:
            print(f'❌看片儿失败：{response}')


    def get_gpt_comment(self, id):
        basic_news_question = '我需要你针对下面的文章，从一个民众的角度进行评论，我希望你的输出只有评论内容，没有别的无关紧要的词语，回复格式是：芝麻开门#你的评论#， 评论语气要尽可能生活化、日常化，字数一定要限制在5-15字之间，下面是我需要你发表评论的文章内容：'
        article_concent = ''
        response = self.article_content(id)
        comment = ''
        commentCount = 0
        if response and response['code'] == 0:
            commentCount = response["data"]["count"]["commentCount"]
            if commentCount <= 0:
                content = response["data"]["txt"]
                soup = BeautifulSoup(content, 'html.parser')
                content_text = soup.get_text()
                message = qianwen_messages(basic_news_question, content_text)
                comment = message

        return comment

    def article_comment_add(self, id, content):
        json_data = {
            'displayResources': [],
            'content': content,
            'targetType': 'content',
            'targetId': id,
        }
        url = 'https://hpapi.shmedia.tech/media-basic-port/api/app/common/comment/add'
        response = requests.post(url, headers=self.headers, json=json_data).json()
        if response and response["code"] == 0:
            print(f'✅文章评论成功')
        else:
            print(f'❌文章评论失败，{response}')

    def article_comment_task(self, id):
        comment = self.get_gpt_comment(id)
        if comment == '':
            print(f'😢未知错误或者文章可能评论过，算了吧，下一个')
        else:
            parts = comment.split('#')
            if len(parts) > 1:
                comment = parts[1].strip()
            print(f'🐌预评论内容：【{comment}】, 你没意见我就在20s后评论了哈......')
            time.sleep(random.randint(20, 25))
            self.article_comment_add(id, comment)

    def gift_list(self):
        # TODO
        print('--------------------')
        print('🐹🐹🐹可兑换商品列表🐹🐹🐹')
        print('--------------------')
        print('😂积分太少啦，暂无商品可兑换')


    def user_mall_info(self):
        # cookies = {
        #     '_pk_id.195.92db': 'beb3fe11a18a5040.1716795245.2.1718304651.1718304651.',
        #     '_pk_ref.195.92db': '%5B%22%22%2C%22%22%2C1718304651%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D',
        #     '_pk_ses.195.92db': '1',
        #     '_pk_testcookie.195.92db': '1',
        #     'acw_tc': '3daa4d2c17183046498594012e618fa07296e4527397152ee0a9c7dc08',
        #     'tfstk': 'fHNEBaTZE82wad9yLcGr04zjCVIKsXjbr7iSrz4oRDm3R9QPzcZZAaeQVQyarkDQdgeIaRzY0WZStYOraln_VQaQVeeTcrAQO9hWaXG-ZisfGsgLJbhuyzhrYHnirqCSrbclu0mhoisfG1aLJbhlc8ZCt0UZycYHEYqojcmtuBcoxYxMIqmiqbcuqfAiy4RHZbDlscAgnlqCR2HhokO-zrRHoAo0-DYMSRxjKpEKbQAuKIMEm_iwZQVZ-PUuh4AfXAyzlWMZS_8r7-zg2D4haUua3PqZh5t14nR-SgaQwJ-kEvAS7m_NSiTOrt6NqZCWeLHKeVofSBpJev0t7m_N7Lp-dH3ZcNAd.',
        # }
        headers = {
            'Host': 'hpweb.shmedia.tech',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3MjkwMWNkOWI4YWVjNDdkMGMxMzcyOWNlMDZiZDM2ZiIsImF1dGgiOiJST0xFX01FTUJFUiIsInR5cGUiOiJtZW1iZXIiLCJleHAiOjE3MTg5MDk0NTEsImlhdCI6MTcxODMwNDY1MSwianRpIjoiMjZlNjkxMjAtNGNmOC00YTNjLWJmOWEtNzM1ZjEwOTViOTQ5IiwidXNlcm5hbWUiOiLkvJrlkZg4Mzg0MDAyNCJ9.kX0HX8cCG6Sm69wq4g29m9Ztwwf_whVe6GHJFVceFrKOCrhh98vK-SZ0KSiPCnDUy1SHEDujn95SDKP3KSxJyPEw8tfJsJsW_6uxHF8mRT9uUr2XXCqq7tMYiKdZfdsmQHMjlEt-1CEwSyg7syqebYnLxVvdDhtX6HJxsA77hUyMHUhMV1D52ojKf2O3x1i1o2oXtbvno3uIWp07Xzt_0VQyedvpILS_lFN2f55MdN13TwxqBghqFCvHLtkm6RyOTR1kP1SZH49DQnx-Xftgva_gZZAvv1uX1lTkZ3O-kmlSPE66oMXKybVQr78-nzmijPK85iBwgTemokIr6ib3XQ',
            # 'Authorization': f"Bearer {self.token}",
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://hpweb.shmedia.tech',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/HuangPu; Version/2.1.5',
            'Referer': 'https://hpweb.shmedia.tech/show-life-front/',
            'Connection': 'keep-alive',
            # 'Cookie': '_pk_id.195.92db=beb3fe11a18a5040.1716795245.2.1718304651.1718304651.; _pk_ref.195.92db=%5B%22%22%2C%22%22%2C1718304651%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D; _pk_ses.195.92db=1; _pk_testcookie.195.92db=1; acw_tc=3daa4d2c17183046498594012e618fa07296e4527397152ee0a9c7dc08; tfstk=fHNEBaTZE82wad9yLcGr04zjCVIKsXjbr7iSrz4oRDm3R9QPzcZZAaeQVQyarkDQdgeIaRzY0WZStYOraln_VQaQVeeTcrAQO9hWaXG-ZisfGsgLJbhuyzhrYHnirqCSrbclu0mhoisfG1aLJbhlc8ZCt0UZycYHEYqojcmtuBcoxYxMIqmiqbcuqfAiy4RHZbDlscAgnlqCR2HhokO-zrRHoAo0-DYMSRxjKpEKbQAuKIMEm_iwZQVZ-PUuh4AfXAyzlWMZS_8r7-zg2D4haUua3PqZh5t14nR-SgaQwJ-kEvAS7m_NSiTOrt6NqZCWeLHKeVofSBpJev0t7m_N7Lp-dH3ZcNAd.',
            'Sec-Fetch-Dest': 'empty',
        }
        response = requests.post('https://hpweb.shmedia.tech/show-life-api/front/member/info', headers=headers)
        if not response or response.status_code != 200:
            print(f'❌获取用户信息失败，{response.text}')
            return
        response_json = response.json()
        if response_json and response_json["code"] == 0:
            print(f'✅{response_json["data"]["nickname"]} | {response_json["data"]["mobile"]} |{response_json["data"]["exp"]}活跃值')

    def play_mall_task(self):
        # cookies = {
        #     '_pk_id.195.92db': 'beb3fe11a18a5040.1716795245.2.1718304651.1718304651.',
        #     '_pk_ref.195.92db': '%5B%22%22%2C%22%22%2C1718304651%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D',
        #     '_pk_ses.195.92db': '1',
        #     '_pk_testcookie.195.92db': '1',
        #     'acw_tc': '3daa4d2c17183046498594012e618fa07296e4527397152ee0a9c7dc08',
        #     'tfstk': 'fHNEBaTZE82wad9yLcGr04zjCVIKsXjbr7iSrz4oRDm3R9QPzcZZAaeQVQyarkDQdgeIaRzY0WZStYOraln_VQaQVeeTcrAQO9hWaXG-ZisfGsgLJbhuyzhrYHnirqCSrbclu0mhoisfG1aLJbhlc8ZCt0UZycYHEYqojcmtuBcoxYxMIqmiqbcuqfAiy4RHZbDlscAgnlqCR2HhokO-zrRHoAo0-DYMSRxjKpEKbQAuKIMEm_iwZQVZ-PUuh4AfXAyzlWMZS_8r7-zg2D4haUua3PqZh5t14nR-SgaQwJ-kEvAS7m_NSiTOrt6NqZCWeLHKeVofSBpJev0t7m_N7Lp-dH3ZcNAd.',
        # }

        headers = {
            'Host': 'hpweb.shmedia.tech',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3MjkwMWNkOWI4YWVjNDdkMGMxMzcyOWNlMDZiZDM2ZiIsImF1dGgiOiJST0xFX01FTUJFUiIsInR5cGUiOiJtZW1iZXIiLCJleHAiOjE3MTg5MDk0NTEsImlhdCI6MTcxODMwNDY1MSwianRpIjoiMjZlNjkxMjAtNGNmOC00YTNjLWJmOWEtNzM1ZjEwOTViOTQ5IiwidXNlcm5hbWUiOiLkvJrlkZg4Mzg0MDAyNCJ9.kX0HX8cCG6Sm69wq4g29m9Ztwwf_whVe6GHJFVceFrKOCrhh98vK-SZ0KSiPCnDUy1SHEDujn95SDKP3KSxJyPEw8tfJsJsW_6uxHF8mRT9uUr2XXCqq7tMYiKdZfdsmQHMjlEt-1CEwSyg7syqebYnLxVvdDhtX6HJxsA77hUyMHUhMV1D52ojKf2O3x1i1o2oXtbvno3uIWp07Xzt_0VQyedvpILS_lFN2f55MdN13TwxqBghqFCvHLtkm6RyOTR1kP1SZH49DQnx-Xftgva_gZZAvv1uX1lTkZ3O-kmlSPE66oMXKybVQr78-nzmijPK85iBwgTemokIr6ib3XQ',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://hpweb.shmedia.tech',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/HuangPu; Version/2.1.5',
            'Referer': 'https://hpweb.shmedia.tech/show-life-front/',
            # 'Content-Length': '0',
            'Connection': 'keep-alive',
            # 'Cookie': '_pk_id.195.92db=beb3fe11a18a5040.1716795245.2.1718304651.1718304651.; _pk_ref.195.92db=%5B%22%22%2C%22%22%2C1718304651%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D; _pk_ses.195.92db=1; _pk_testcookie.195.92db=1; acw_tc=3daa4d2c17183046498594012e618fa07296e4527397152ee0a9c7dc08; tfstk=fHNEBaTZE82wad9yLcGr04zjCVIKsXjbr7iSrz4oRDm3R9QPzcZZAaeQVQyarkDQdgeIaRzY0WZStYOraln_VQaQVeeTcrAQO9hWaXG-ZisfGsgLJbhuyzhrYHnirqCSrbclu0mhoisfG1aLJbhlc8ZCt0UZycYHEYqojcmtuBcoxYxMIqmiqbcuqfAiy4RHZbDlscAgnlqCR2HhokO-zrRHoAo0-DYMSRxjKpEKbQAuKIMEm_iwZQVZ-PUuh4AfXAyzlWMZS_8r7-zg2D4haUua3PqZh5t14nR-SgaQwJ-kEvAS7m_NSiTOrt6NqZCWeLHKeVofSBpJev0t7m_N7Lp-dH3ZcNAd.',
            'Sec-Fetch-Dest': 'empty',
        }

        response = requests.post('https://hpweb.shmedia.tech/show-life-api/front/task/list',
                                headers=headers)
        if not response or response.status_code != 200:
            print(f'❌获取任务列表失败，{response.text}')
            return
        response_json = response.json()
        if response_json and response_json["code"] == 0:
            for task in response_json["data"]:
                if task["name"] == "每日访问":
                    self.login_score()
                    time.sleep(random.randint(5, 10))
                elif task["name"] == "搜索":
                    self.play_search()
                    time.sleep(random.randint(15, 30))
                elif task["name"] == "浏览剧目":
                    for i in range(task["dailyLimit"]):
                        self.search_play_list()
                        time.sleep(random.randint(5, 10))
                        self.play_view()
                        time.sleep(random.randint(5, 10))
                # elif task["name"] == "评论剧目":
                #     for i in range(task["dailyLimit"]):
                #         self.video_view_task()
                elif task["name"] == "点赞评论":
                    for i in range(task["dailyLimit"]):
                        self.great_comment_list()
                        self.comment_like()
                        time.sleep(random.randint(15, 30))
                elif task["name"] == "分享剧目":
                    for i in range(task["dailyLimit"]):
                        self.play_share_complate()
                        time.sleep(random.randint(15, 30))
                        self.play_share_add()
                        time.sleep(random.randint(15, 30))
        else:
            print(f'❌获取任务列表失败，{response.text}')

    def play_search(self):
        headers = {
            'Host': 'hpweb.shmedia.tech',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3MjkwMWNkOWI4YWVjNDdkMGMxMzcyOWNlMDZiZDM2ZiIsImF1dGgiOiJST0xFX01FTUJFUiIsInR5cGUiOiJtZW1iZXIiLCJleHAiOjE3MTg5NTQyNDgsImlhdCI6MTcxODM0OTQ0OCwianRpIjoiNzA4YjdlNmItZWNmZS00OWM1LWE4ZWItZGE1MzUzM2EyYjkxIiwidXNlcm5hbWUiOiLkvJrlkZg4Mzg0MDAyNCJ9.L0Z4vlQ11K4TSMnZaagyadym2DxtRnOIw8Sb8Usn-ePMlGyhup1BBMmkdtSCo__UMumzclgu3XobbfZ7kcnKUCqsNjVfO7vphJHRtQgLdlnlPuBcthiBdlDG4Eaz0imA5VxGtWPFhGs2bsEdZSMsrG4A0KjMePYtV4CQLCluSuCOSgq8UhMjx9CUN8LM9AQdboCcoPKugvM1JbnL_20DF6CVz76OQcG18triCSoUySGdOPnOnUCyFnUxn-Mc3wu__BK6nCwAsZKTFU0NDMkksSCjc_CffYkegNnaX6V5H_uvWyuIqxplXe5nPvujfrEz4Qn6qbl9Y3csFHCY8UiDHA',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://hpweb.shmedia.tech',
            # 'Content-Length': '55',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/HuangPu; Version/2.1.5',
            'Referer': 'https://hpweb.shmedia.tech/show-life-front/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': '_pk_id.195.92db=beb3fe11a18a5040.1716795245.3.1718349449.1718349449.; _pk_ref.195.92db=%5B%22%22%2C%22%22%2C1718349449%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D; _pk_ses.195.92db=1; _pk_testcookie.195.92db=1; acw_tc=3daa4d2717183494483777916e083bdf190bdf1af119e08371c7a8bec9; tfstk=fHtSwz0NOvMyBhR_1aHVfTGE0mIkOBiwJJ6pIpEzpgIJAMODMaQP42mIdC544BJrE9iBTsrezbxeGwdwOM7pY6-Idgx2zk5rZM9p_wGZ_cowELjGvflwlL399MBKY6dOaj6OxMhZgcowELjH_g7wUD9xhTWNpMC8vx_ABsERpuBLMx6hM6IdyknAM9B79uIdpCszOtVV_LMb5n7tQlCHesZQhn1RPzvRGkEpcl756W5bvkKfeKvp79EZiZTBQ37fHDwChF9vt_p-AJ6X5Kdf7nPV4lPN16J4R-_gvtaohxa38n1n5mbjrSiNytXV4xMb8UQRnt1Zhxa3-aBcnJkjhy8R.',
        }

        json_data = {
            'pageNo': 1,
            'pageSize': 10,
            'type': 0,
            'keywords': '恋爱',
        }

        response = requests.post(
            'https://hpweb.shmedia.tech/show-life-api/front/index/serch',
            headers=headers,
            json=json_data,
        )

    def search_play_list(self):
        headers = {
            'Host': 'hpweb.shmedia.tech',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3MjkwMWNkOWI4YWVjNDdkMGMxMzcyOWNlMDZiZDM2ZiIsImF1dGgiOiJST0xFX01FTUJFUiIsInR5cGUiOiJtZW1iZXIiLCJleHAiOjE3MTg5NTQyNDgsImlhdCI6MTcxODM0OTQ0OCwianRpIjoiNzA4YjdlNmItZWNmZS00OWM1LWE4ZWItZGE1MzUzM2EyYjkxIiwidXNlcm5hbWUiOiLkvJrlkZg4Mzg0MDAyNCJ9.L0Z4vlQ11K4TSMnZaagyadym2DxtRnOIw8Sb8Usn-ePMlGyhup1BBMmkdtSCo__UMumzclgu3XobbfZ7kcnKUCqsNjVfO7vphJHRtQgLdlnlPuBcthiBdlDG4Eaz0imA5VxGtWPFhGs2bsEdZSMsrG4A0KjMePYtV4CQLCluSuCOSgq8UhMjx9CUN8LM9AQdboCcoPKugvM1JbnL_20DF6CVz76OQcG18triCSoUySGdOPnOnUCyFnUxn-Mc3wu__BK6nCwAsZKTFU0NDMkksSCjc_CffYkegNnaX6V5H_uvWyuIqxplXe5nPvujfrEz4Qn6qbl9Y3csFHCY8UiDHA',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://hpweb.shmedia.tech',
            # 'Content-Length': '79',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/HuangPu; Version/2.1.5',
            'Referer': 'https://hpweb.shmedia.tech/show-life-front/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': 'acw_tc=3daa4d2517183512514716538ed5ea206fb81d200300b2133160492799; _pk_id.195.92db=beb3fe11a18a5040.1716795245.3.1718349449.1718349449.; _pk_ref.195.92db=%5B%22%22%2C%22%22%2C1718349449%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D; _pk_testcookie.195.92db=1; tfstk=fHtSwz0NOvMyBhR_1aHVfTGE0mIkOBiwJJ6pIpEzpgIJAMODMaQP42mIdC544BJrE9iBTsrezbxeGwdwOM7pY6-Idgx2zk5rZM9p_wGZ_cowELjGvflwlL399MBKY6dOaj6OxMhZgcowELjH_g7wUD9xhTWNpMC8vx_ABsERpuBLMx6hM6IdyknAM9B79uIdpCszOtVV_LMb5n7tQlCHesZQhn1RPzvRGkEpcl756W5bvkKfeKvp79EZiZTBQ37fHDwChF9vt_p-AJ6X5Kdf7nPV4lPN16J4R-_gvtaohxa38n1n5mbjrSiNytXV4xMb8UQRnt1Zhxa3-aBcnJkjhy8R.',
        }

        json_data = {
            'pageNo': 1,
            'pageSize': 50,
            'type': 1,
            'typeId': '95ab9c086c335fda0683c4a7598f7c5f',
        }

        response = requests.post(
            'https://hpweb.shmedia.tech/show-life-api/front/index/serch',
            headers=headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            list = response_json['data']['records']
            for item in list:
                self.play_ids.append(item['id'])


    def play_view(self):
        headers = {
            'Host': 'hpweb.shmedia.tech',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3MjkwMWNkOWI4YWVjNDdkMGMxMzcyOWNlMDZiZDM2ZiIsImF1dGgiOiJST0xFX01FTUJFUiIsInR5cGUiOiJtZW1iZXIiLCJleHAiOjE3MTg5NTQyNDgsImlhdCI6MTcxODM0OTQ0OCwianRpIjoiNzA4YjdlNmItZWNmZS00OWM1LWE4ZWItZGE1MzUzM2EyYjkxIiwidXNlcm5hbWUiOiLkvJrlkZg4Mzg0MDAyNCJ9.L0Z4vlQ11K4TSMnZaagyadym2DxtRnOIw8Sb8Usn-ePMlGyhup1BBMmkdtSCo__UMumzclgu3XobbfZ7kcnKUCqsNjVfO7vphJHRtQgLdlnlPuBcthiBdlDG4Eaz0imA5VxGtWPFhGs2bsEdZSMsrG4A0KjMePYtV4CQLCluSuCOSgq8UhMjx9CUN8LM9AQdboCcoPKugvM1JbnL_20DF6CVz76OQcG18triCSoUySGdOPnOnUCyFnUxn-Mc3wu__BK6nCwAsZKTFU0NDMkksSCjc_CffYkegNnaX6V5H_uvWyuIqxplXe5nPvujfrEz4Qn6qbl9Y3csFHCY8UiDHA',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://hpweb.shmedia.tech',
            # 'Content-Length': '41',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/HuangPu; Version/2.1.5',
            'Referer': 'https://hpweb.shmedia.tech/show-life-front/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': 'acw_tc=3daa4d2517183512514716538ed5ea206fb81d200300b2133160492799; _pk_id.195.92db=beb3fe11a18a5040.1716795245.3.1718349449.1718349449.; _pk_ref.195.92db=%5B%22%22%2C%22%22%2C1718349449%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D; _pk_testcookie.195.92db=1; tfstk=fHtSwz0NOvMyBhR_1aHVfTGE0mIkOBiwJJ6pIpEzpgIJAMODMaQP42mIdC544BJrE9iBTsrezbxeGwdwOM7pY6-Idgx2zk5rZM9p_wGZ_cowELjGvflwlL399MBKY6dOaj6OxMhZgcowELjH_g7wUD9xhTWNpMC8vx_ABsERpuBLMx6hM6IdyknAM9B79uIdpCszOtVV_LMb5n7tQlCHesZQhn1RPzvRGkEpcl756W5bvkKfeKvp79EZiZTBQ37fHDwChF9vt_p-AJ6X5Kdf7nPV4lPN16J4R-_gvtaohxa38n1n5mbjrSiNytXV4xMb8UQRnt1Zhxa3-aBcnJkjhy8R.',
        }

        id = random.choice(self.play_ids)

        json_data = {
            'id': id,
        }

        response = requests.post(
            'https://hpweb.shmedia.tech/show-life-api/front/play/info',
            headers=headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            print(f'✅浏览剧目完成')
        else:
            print(f'浏览剧目失败')

    def play_share_complate(self):
        # import requests
        #
        # cookies = {
        #     '_pk_id.195.92db': 'beb3fe11a18a5040.1716795245.4.1718354348.1718352555.',
        #     '_pk_ses.195.92db': '1',
        #     '_pk_testcookie.195.92db': '1',
        #     'tfstk': 'fWRrwp4VKpvVsreUUi1Fb8uTyIoRw_m6-BsC-eYhPgjkPY3E8itVV2pWAWJ2-3XWFDp5TK89bQtCZ9NFTnIXAWTWAzpvfFVWNYCQT_1dtcis1f_Jy6ChBIH01gLDkwfgN3jMyUCLkcis1fT8LnCEuD5Hxj2c8iVl-HXhoq7hRu23ZHYmuwI0ZkXutt2c-azuECNXm3g5yT0M07Hq-o_RUGYPLW2eg56PjUj4tZdVzXIMriP3TgKVWa8Xsv4lAdLc7aJq--jklQ8FzKu3ngYHWCp14nPdoDTW9Lr3KTVCuGgqocax-AMqxVhQpJBRpZSso7eLpTbAuGgquJedFuQVfqVR.',
        #     'acw_tc': '79e4bc1317183537548383136e390d9acff81831cd521d9d4e2ddf493f',
        #     '_pk_ref.195.92db': '%5B%22%22%2C%22%22%2C1718352555%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D',
        # }

        headers = {
            'Host': 'hpweb.shmedia.tech',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3MjkwMWNkOWI4YWVjNDdkMGMxMzcyOWNlMDZiZDM2ZiIsImF1dGgiOiJST0xFX01FTUJFUiIsInR5cGUiOiJtZW1iZXIiLCJleHAiOjE3MTg5NTkxNDgsImlhdCI6MTcxODM1NDM0OCwianRpIjoiMjg5ZWViNTAtNjIxMi00ODgxLWFiMGQtY2ZjYmNlNjQ1OGRmIiwidXNlcm5hbWUiOiLkvJrlkZg4Mzg0MDAyNCJ9.D5NMrgKlFXrcabFDIMlW3Z5KAO3cyQnyFhCdcMkJ6jmB9HQ86qfQfJ35eIwmFbF0YeeXGtYBzSIouLrpyLkjxpazKvRaQ6TSVn0MbyiK5xiw33vgRRPQyhXtGy0AHWH75UvhRgkRDpDX8v9dzDyzMRMCMCugxhupdOWYliVaXzuohgKjvxSALIu0o7sE1bT7MFlohYh9anC1FbNEsr9QU55Nn7Ntv3Mkk2gaqdUufqgOtltuJ2ZuM-XuevhCmv572r8ct7nX85NWwttWJKWt8Fdwql0FM2HzvFuAJvehlHytTQsEBKd18nx7EDScoFrqIoC9Dchk2wp5brPazlfpAg',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://hpweb.shmedia.tech',
            # 'Content-Length': '640',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/HuangPu; Version/2.1.5',
            'Referer': 'https://hpweb.shmedia.tech/show-life-front/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': '_pk_id.195.92db=beb3fe11a18a5040.1716795245.4.1718354348.1718352555.; _pk_ses.195.92db=1; _pk_testcookie.195.92db=1; tfstk=fWRrwp4VKpvVsreUUi1Fb8uTyIoRw_m6-BsC-eYhPgjkPY3E8itVV2pWAWJ2-3XWFDp5TK89bQtCZ9NFTnIXAWTWAzpvfFVWNYCQT_1dtcis1f_Jy6ChBIH01gLDkwfgN3jMyUCLkcis1fT8LnCEuD5Hxj2c8iVl-HXhoq7hRu23ZHYmuwI0ZkXutt2c-azuECNXm3g5yT0M07Hq-o_RUGYPLW2eg56PjUj4tZdVzXIMriP3TgKVWa8Xsv4lAdLc7aJq--jklQ8FzKu3ngYHWCp14nPdoDTW9Lr3KTVCuGgqocax-AMqxVhQpJBRpZSso7eLpTbAuGgquJedFuQVfqVR.; acw_tc=79e4bc1317183537548383136e390d9acff81831cd521d9d4e2ddf493f; _pk_ref.195.92db=%5B%22%22%2C%22%22%2C1718352555%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D',
        }

        json_data = {
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3MjkwMWNkOWI4YWVjNDdkMGMxMzcyOWNlMDZiZDM2ZiIsImF1dGgiOiJST0xFX01FTUJFUiIsInR5cGUiOiJtZW1iZXIiLCJleHAiOjE3MTg5NTkxNDgsImlhdCI6MTcxODM1NDM0OCwianRpIjoiMjg5ZWViNTAtNjIxMi00ODgxLWFiMGQtY2ZjYmNlNjQ1OGRmIiwidXNlcm5hbWUiOiLkvJrlkZg4Mzg0MDAyNCJ9.D5NMrgKlFXrcabFDIMlW3Z5KAO3cyQnyFhCdcMkJ6jmB9HQ86qfQfJ35eIwmFbF0YeeXGtYBzSIouLrpyLkjxpazKvRaQ6TSVn0MbyiK5xiw33vgRRPQyhXtGy0AHWH75UvhRgkRDpDX8v9dzDyzMRMCMCugxhupdOWYliVaXzuohgKjvxSALIu0o7sE1bT7MFlohYh9anC1FbNEsr9QU55Nn7Ntv3Mkk2gaqdUufqgOtltuJ2ZuM-XuevhCmv572r8ct7nX85NWwttWJKWt8Fdwql0FM2HzvFuAJvehlHytTQsEBKd18nx7EDScoFrqIoC9Dchk2wp5brPazlfpAg',
        }

        response = requests.post(
            'https://hpweb.shmedia.tech/show-life-api/front/task/complete/share',
            headers=headers,
            json=json_data,
        )


    def play_share_add(self):
        # import requests
        #
        # cookies = {
        #     'tfstk': 'fHtSwz0NOvMyBhR_1aHVfTGE0mIkOBiwJJ6pIpEzpgIJAMODMaQP42mIdC544BJrE9iBTsrezbxeGwdwOM7pY6-Idgx2zk5rZM9p_wGZ_cowELjGvflwlL399MBKY6dOaj6OxMhZgcowELjH_g7wUD9xhTWNpMC8vx_ABsERpuBLMx6hM6IdyknAM9B79uIdpCszOtVV_LMb5n7tQlCHesZQhn1RPzvRGkEpcl756W5bvkKfeKvp79EZiZTBQ37fHDwChF9vt_p-AJ6X5Kdf7nPV4lPN16J4R-_gvtaohxa38n1n5mbjrSiNytXV4xMb8UQRnt1Zhxa3-aBcnJkjhy8R.',
        # }

        headers = {
            'Host': 'hpapi.shmedia.tech',
            'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1ZjhjYmFjOWIxNWQ0NmU1YmIwOWU3NTNiMjk4MWM0ZjRkMjQ7MzEwMTAxIiwiaWF0IjoxNzE2NzkyODMxLCJleHAiOjI3NTM1OTI4MzF9.v53Nat0gEXQKSPBimVjSNMYQlgC7MQJyWj1gY96FmvuAM1YLINl7pXdBR5QEMpOITW6SYfftfStmTNOgylwWPw',
            'Content-Type': 'application/json; charset=utf-8',
            'deviceId': '8272a4f8ff99467994de1a502833d39c',
            'User-Agent': 'HuangPu/2.1.5 (iPhone; iOS 16.6; Scale/3.00)',
            'Connection': 'keep-alive',
            # 'Content-Length': '2',
            'siteId': '310101',
            # 'Cookie': 'tfstk=fHtSwz0NOvMyBhR_1aHVfTGE0mIkOBiwJJ6pIpEzpgIJAMODMaQP42mIdC544BJrE9iBTsrezbxeGwdwOM7pY6-Idgx2zk5rZM9p_wGZ_cowELjGvflwlL399MBKY6dOaj6OxMhZgcowELjH_g7wUD9xhTWNpMC8vx_ABsERpuBLMx6hM6IdyknAM9B79uIdpCszOtVV_LMb5n7tQlCHesZQhn1RPzvRGkEpcl756W5bvkKfeKvp79EZiZTBQ37fHDwChF9vt_p-AJ6X5Kdf7nPV4lPN16J4R-_gvtaohxa38n1n5mbjrSiNytXV4xMb8UQRnt1Zhxa3-aBcnJkjhy8R.',
        }

        json_data = {}

        response = requests.post(
            'https://hpapi.shmedia.tech/media-basic-port/api/app/points/share/add',
            headers=headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            print(f'✅分享剧目完成')
        else:
            print(f'分享剧目失败')


    def great_comment_list(self):
        headers = {
            'Host': 'hpweb.shmedia.tech',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3MjkwMWNkOWI4YWVjNDdkMGMxMzcyOWNlMDZiZDM2ZiIsImF1dGgiOiJST0xFX01FTUJFUiIsInR5cGUiOiJtZW1iZXIiLCJleHAiOjE3MTg5NTczNTUsImlhdCI6MTcxODM1MjU1NSwianRpIjoiODBhYjhkMGItODQ1My00NDZhLTkwMjUtYTc4NDlhNGFiODVkIiwidXNlcm5hbWUiOiLkvJrlkZg4Mzg0MDAyNCJ9.qD3_k_4lwbT0OvQ2WlzGMMs_ZUSfwxVQiwzOfH-BCD4QbsCR-2EI-mS9Kgs308TKjHGB5ve6qKD75jKlP00-TPA6y2YAly8-fF2BAypAjkzS_5UretN3CARpLPZuvxNdTL1JrK4u58PO3XMf46Ek6919djnGUqAmdAxGP6DlkgYrmCcRznAeHT7yaqv01b_wd-3r0CgUKU1XudFPDUQhbfK7CxVG-8CeJp_BkgN6X3KpvdJSkhhgZLGgA1P4Xl0QS6321JxlrXpqFvTdaVXX6kEN32pFtci9ET4SAzjYX8Mn4F5mfYAvjJWPkbv2crgAAb_uT_IIFHNp_yKAlMmuWQ',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://hpweb.shmedia.tech',
            # 'Content-Length': '26',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/HuangPu; Version/2.1.5',
            'Referer': 'https://hpweb.shmedia.tech/show-life-front/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': '_pk_id.195.92db=beb3fe11a18a5040.1716795245.4.1718352555.1718352555.; _pk_ref.195.92db=%5B%22%22%2C%22%22%2C1718352555%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D; _pk_ses.195.92db=1; _pk_testcookie.195.92db=1; tfstk=fqR-wT4G9-FE8-pHnUMD-7V8g-5J9BLrH38_tMjudnKvmHChtUTkv9KkcLXCqBAL9h--z9snzMUdcevozHYQJwtDcHBEzMjCvHYBEahisU8PT6OKjfcile8fZQIQx6gOAggsjcciiU8PT6iMK32G-EQFczwCdHsfhi73O6s5dowf5isCO6tChE_C5aNCdMsXlCOSWMcV0WppFyygJXs8OWOf6TQ9PJVQOIQRe885DLvkMaBRXtY8myRydQdfQBot5sOJ2Q6vqvNOGQKJNtKsmSKF42tMXeg4jGQ3eqdQLJW5o3_lBqTe29flkG0mKJyFeQ_Ajq3YLJW5uZIiu3yULTd5.; acw_tc=3daa4d2517183512514716538ed5ea206fb81d200300b2133160492799',
        }

        json_data = {
            'pageNo': 1,
            'pageSize': 20,
        }

        response = requests.post(
            'https://hpweb.shmedia.tech/show-life-api/front/index/comment/great',
            headers=headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            list = response_json['data']['records']
            for item in list:
                self.play_comment_ids.append(item['id'])
        else:
            print(f'获取好评列表失败')



    def comment_like(self):
        headers = {
            'Host': 'hpweb.shmedia.tech',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3MjkwMWNkOWI4YWVjNDdkMGMxMzcyOWNlMDZiZDM2ZiIsImF1dGgiOiJST0xFX01FTUJFUiIsInR5cGUiOiJtZW1iZXIiLCJleHAiOjE3MTg5NTczNTUsImlhdCI6MTcxODM1MjU1NSwianRpIjoiODBhYjhkMGItODQ1My00NDZhLTkwMjUtYTc4NDlhNGFiODVkIiwidXNlcm5hbWUiOiLkvJrlkZg4Mzg0MDAyNCJ9.qD3_k_4lwbT0OvQ2WlzGMMs_ZUSfwxVQiwzOfH-BCD4QbsCR-2EI-mS9Kgs308TKjHGB5ve6qKD75jKlP00-TPA6y2YAly8-fF2BAypAjkzS_5UretN3CARpLPZuvxNdTL1JrK4u58PO3XMf46Ek6919djnGUqAmdAxGP6DlkgYrmCcRznAeHT7yaqv01b_wd-3r0CgUKU1XudFPDUQhbfK7CxVG-8CeJp_BkgN6X3KpvdJSkhhgZLGgA1P4Xl0QS6321JxlrXpqFvTdaVXX6kEN32pFtci9ET4SAzjYX8Mn4F5mfYAvjJWPkbv2crgAAb_uT_IIFHNp_yKAlMmuWQ',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://hpweb.shmedia.tech',
            # 'Content-Length': '41',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/HuangPu; Version/2.1.5',
            'Referer': 'https://hpweb.shmedia.tech/show-life-front/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            # 'Cookie': '_pk_id.195.92db=beb3fe11a18a5040.1716795245.4.1718352555.1718352555.; _pk_ref.195.92db=%5B%22%22%2C%22%22%2C1718352555%2C%22https%3A%2F%2Fmall-mobile.shmedia.tech%2F%22%5D; _pk_ses.195.92db=1; _pk_testcookie.195.92db=1; tfstk=fqR-wT4G9-FE8-pHnUMD-7V8g-5J9BLrH38_tMjudnKvmHChtUTkv9KkcLXCqBAL9h--z9snzMUdcevozHYQJwtDcHBEzMjCvHYBEahisU8PT6OKjfcile8fZQIQx6gOAggsjcciiU8PT6iMK32G-EQFczwCdHsfhi73O6s5dowf5isCO6tChE_C5aNCdMsXlCOSWMcV0WppFyygJXs8OWOf6TQ9PJVQOIQRe885DLvkMaBRXtY8myRydQdfQBot5sOJ2Q6vqvNOGQKJNtKsmSKF42tMXeg4jGQ3eqdQLJW5o3_lBqTe29flkG0mKJyFeQ_Ajq3YLJW5uZIiu3yULTd5.; acw_tc=3daa4d2517183512514716538ed5ea206fb81d200300b2133160492799',
        }

        comment_id = random.choice(self.play_comment_ids)

        json_data = {
            'id': comment_id,
        }

        response = requests.post(
            'https://hpweb.shmedia.tech/show-life-api/front/comment/like',
            headers=headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            print(f'✅评论点赞完成')
        else:
            print(f'评论点赞失败')



    def main(self):
        counter = 0
        self.login_score()
        self.sign()
        for j in range(5):
            self.video_view_task()
            time.sleep(random.randint(20, 30))
        article_list = self.article_list()
        for i in range(15):
            article_id = random.choice(article_list)["id"]
            print('--------------------------------------------------------------------')
            print(f'🐹随机抓取到一篇文章{article_id}，开始做任务......')
            self.article_read(article_id)
            time.sleep(random.randint(20, 35))
            if counter <= 1:
                if self.isComment == '1':
                    self.article_comment_task(article_id)
                    time.sleep(random.randint(20, 40))
                else:
                    print("未开启自动评论, 如要开启，请更改环境变量配置")
                    time.sleep(random.randint(10, 25))
                self.article_favor_task(article_id)
                time.sleep(random.randint(10, 20))
                self.article_share(article_id)
                time.sleep(random.randint(10, 25))
                # TODO 观看直播
                # self.live_streaming()
            counter += 1
        # TODO 商城活跃值任务（活跃值解锁兑换卡券）
        print(f"\n======== ▷ 商城活跃值任务 ◁ ========")
        self.user_mall_info()
        self.play_mall_task()
        self.task_list()
        self.total_score()
        self.today_score()
        self.gift_list()


if __name__ == '__main__':
    env_name = 'SHHP_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1ZjhjYmFjOWIxNWQ0NmU1YmIwOWU3NTNiMjk4MWM0ZjRkMjQ7MzEwMTAxIiwiaWF0IjoxNzE2NzkyODMxLCJleHAiOjI3NTM1OTI4MzF9.v53Nat0gEXQKSPBimVjSNMYQlgC7MQJyWj1gY96FmvuAM1YLINl7pXdBR5QEMpOITW6SYfftfStmTNOgylwWPw#0'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"上海黄浦共获取到{len(tokens)}个账号")
    for i, account_info in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        SHHP(account_info).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
