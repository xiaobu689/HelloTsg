"""
华为AITO
抓包任意url请求头token

定时设置：
cron: 40 6 * * *
const $ = new Env("华为AITO");
"""

print("已废")
exit(0)

import datetime
import os

import requests

# from sign.notify import notify_pushPlus
# print("This script is disabled.")
# exit(0)


class AITO:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Host': 'aim.longwisedata.com',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003127) NetType/WIFI Language/zh_CN',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate, br'
        }

    def sign_account_info(self):
        message = ''
        url = 'https://aim.longwisedata.com/lwmarketing_user_api/selectPersonInfoOne?token=0935a6ee0205880cfa36c049a4ceb38c&timestamp=1716279435019&sig=025cc4e7ebda0cba452c9e2c075d162a'
        response = requests.get(url, headers=self.headers).json()
        print(response)
        data = response
        if response["result"] == 0:
            integral = response["data"]["integral"]
            message += f"✅帐号：{data.get('data').get('nick')}\n"
            message += f"✅积分：{data.get('data').get('integral')}\n"
        else:
            message += f"❌帐号：{data.get('data').get('nick')}获取失败，可能cookie失效！\n"
            print(message)

        return message, data.get('data').get('integral')

    # 京东礼品卡列表
    def gift_list(self):
        url = 'https://mall.longwisedata.com/api/product/v1/card/defs/40/detail'
        response = requests.get(url, headers=self.headers).json()
        print(response)
        return response["result"]["skus"]

    # 签到
    def sign_in(self):
        message = ""
        # 签到
        url = 'https://aim.longwisedata.com/lwmarketing_user_api/taskSquare/signIn/signIn'
        data = {
            'token': '0935a6ee0205880cfa36c049a4ceb38',
            'timestamp': '1716279435019',
            'sig': '025cc4e7ebda0cba452c9e2c075d162a'
        }

        response = requests.post(url, headers=self.headers, data=data)
        data = response.json()
        print(response.text)
        if data.get('result') == '200' or data.get('result') == '0':
            message += "✅签到结果：签到成功，"
            print(message)
        else:
            message = "❌签到结果：签到失败"
            print(message)

        return message

    def sign_task_list(self):
        url = 'https://aim.longwisedata.com/lwmarketing_user_api/taskList?token=0935a6ee0205880cfa36c049a4ceb38c&timestamp=1716279435019&sig=025cc4e7ebda0cba452c9e2c075d162a&pageNum=1&pageSize=10'
        response = requests.get(url, headers=self.headers)
        # print(response.text)
        data = response.json()
        if data.get('result') == '0':
            task_list = data.get('list', [])
            print("Task List:", task_list)
            for task in task_list:
                print("Task=", task)
                if task.get('task_subtype') == 0:
                    task_id = task.get('task_id')
                    task_type = task.get('task_type')
                    article_title = task.get('name')
                    article_url = task.get('article_url')
                    print("Article Title:", article_title)
                    print("Article URL:", article_url)
                    # 领取任务
                    url = 'https://aim.longwisedata.com/lwmarketing_user_api/taskForward/receiveTask'
                    data = {
                        'token': '0935a6ee0205880cfa36c049a4ceb38',
                        'timestamp': '1716279435019',
                        'sig': '025cc4e7ebda0cba452c9e2c075d162a',
                        'taskId': task_id,
                        'taskType': task_type
                    }

                    response = requests.post(url, headers=self.headers, data=data)
                    print("任务领取成功：", response.text)
        else:
            print("Failed to get task list.")  # {"result":"0","msg":"success"}

    def sign_my_tasklist(self):
        url = 'https://aim.longwisedata.com/lwmarketing_user_api/myTaskList?token=431d27a0ddb0aa1959c40af487aa4da9&timestamp=1714828633254&sig=fe0ca62a0b3ae9f4dce0e224fa3a257f&pageNum=1&pageSize=10&type=2'
        response = requests.get(url, headers=self.headers)
        data = response.json()
        # print(response.text)
        if data.get('result') == '0':
            task_list = data.get('list', [])
            # print("Task List:", task_list)
            for task in task_list:
                if task.get('task_subtype') == 0 and task.get('browse_reward') > 0:
                    end_time = datetime.datetime.strptime(task.get('end_time'), '%Y-%m-%d %H:%M:%S')
                    # print("------------------测试打印结束时间=", end_time)
                    # 获取当前时间
                    current_time = datetime.datetime.now()
                    # 判断是否 end_time 小于当前时间
                    if end_time >= current_time:
                        print("task=", task)
                        task_id = task.get('task_id')
                        task_type = task.get('task_type')
                        article_title = task.get('name')
                        article_url = task.get('article_url')
                        real_url = task.get('real_url')
                        print(f'Task ID:', task_id)
                        print("real_url:", real_url)
                        print("article_url:", article_url)
                        print("article_title:", article_title)
                        print("------------------------------")
    # 浏览助力
    def help_task(self):
        headers = {
            'Host': 'aim.longwisedata.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://aim.longwisedata.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003132) NetType/WIFI Language/zh_CN',
            'Referer': 'https://aim.longwisedata.com/wxauth/894536/auth1.html?code=031j8W000jObeS1SZN2002UiIJ3j8W0s&state=790443582997286912&appid=wxabafb4839d3d03b9',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Cookie': 'acw_tc=2760774217173970366643242e4ec161aa4a34aac38a98dd3c5eacc64b97ac',
        }

        data = {
            'lat': '',
            'lng': '',
            'shareId': '790443582997286912',
            'code': '031j8W000jObeS1SZN2002UiIJ3j8W0s',
            'state': '790443582997286912',
            'timestamp': '20240603150330044',
            'sig': '28ec716b8197a6b8c49da968b03881d0',
        }

        url = 'https://aim.longwisedata.com/lwmarketing-provider-wxdata/wxBrowseTaskNew'

        response = requests.post(url, headers=headers, data=data)

    def main(self):
        title = "AIOT之声签到"
        push_msg = ''
        msg1, integral1 = self.sign_account_info()
        if "失败" in msg1:
            print("账号信息获取失败，请检查cookie是否正确")
            return
        else:
            msg2 = self.sign_in()
            # 积分进度
            msg3, integral3 = self.sign_account_info()
            diff_integra=  integral3 - integral1
            _msg = f'积分 + {diff_integra}'
            push_msg += msg1 + msg2 + msg3 + _msg
            result = self.gift_list()
            first_gift_price = result["result"]["skus"][0]["price"]
            tmp_msg = ''
            if integral3 >= first_gift_price:
                tmp_msg = f"已达标，可前往兑换奖品！\n"
            else:
                tmp_msg = f'{integral3}/{first_gift_price}'
            push_msg += f'✅{first_gift_price}进度: {tmp_msg}\n'
            push_msg += f'✅{first_gift_price}库存: {result["result"]["skus"][0]["stock"]}'

            # 推送
            # notify_pushPlus(title, push_msg)

        # 获取活动广场任务列表
        self.sign_task_list()
        # 获取我的转发任务列表【带转发奖励的】
        self.sign_my_tasklist()


if __name__ == '__main__':
    env_name = 'AITO_COOKIE'
    AITO_TOKEN = os.getenv(env_name)
    AITO_TOKEN = 'acw_tc=2760820e17162794286216565e54f6e07624769e97723698a67bec1d189464'
    if not AITO_TOKEN:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)


    print(AITO(AITO_TOKEN).main())
