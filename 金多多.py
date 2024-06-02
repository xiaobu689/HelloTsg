"""
金多多

抓任意包请求头 Cookie
变量名: JDD_COOKIE

cron: 30 6 * * *
const $ = new Env("金多多");
"""
import os
import random
import re
import time
import requests

from sendNotify import send


class JDD():
    name = "金多多"

    def __init__(self, cookie):
        self.cookie = cookie.split('#')[0]
        self.mid = cookie.split('#')[1]
        self.verify = False
        self.credit = 0
        self.coin = 0
        self.msg = ''
        self.headers = {
            'Host': 'www.jindd.shop',
            'Accept': '*/*',
            'Authorization': 'Basic bnVsbDpudWxs',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://www.jindd.shop',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003131) NetType/WIFI Language/zh_CN',
            'Referer': 'https://www.jindd.shop/addons/yun_shop/?menu',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Cookie': self.cookie,
        }

    def userinfo(self):
        params = {
            'i': '12',
            'uuid': '0',
            'type': '1',
            'version': 'v1.1.137',
            'validate_page': '1',
            'basic_info': '1',
            'route': 'member.member.member-data',
        }

        json_data = {
            'v': 2,
            'basic_info': 1,
        }

        response = requests.post('https://www.jindd.shop/addons/yun_shop/api.php', params=params, headers=self.headers,
                                 json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json["result"] == 1:
                credit = response_json["data"]["member"]["credit"].get("data")
                coin = response_json["data"]["member"]["love_show"].get("usable_data")
                self.credit = credit
                self.coin = coin
            else:
                print("❌获取用户信息失败, ", response_json["msg"])

    def view_product(self):
        msg =''
        params = {
            'i': '12',
            'uuid': '0',
            'type': '1',
            'mid': f'{self.mid}',
            'version': 'v1.1.137',
            'validate_page': '1',
            'scope': 'pass',
            'route': 'plugin.qmtask.api.qmtask.confirm_qmtask',
        }

        json_data = {
            'goods_id': None,
        }

        url = 'https://www.jindd.shop/addons/yun_shop/api.php'
        response = requests.post(url, params=params, headers=self.headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json["result"] == 1:
                msg = f'✅成功浏览商品+1'
            else:
                msg = "❌浏览商品失败, ", response_json["msg"]
        self.msg += msg
        print(msg)

    def finish_today_task(self):
        params = {
            'i': '12',
            'uuid': '0',
            'type': '1',
            'mid': f'{self.mid}',
            'version': 'v1.1.137',
            'validate_page': '1',
            'scope': 'pass',
            'route': 'plugin.qmtask.api.qmtask.confirm_qmtask',
        }
        json_data = {
            'goods_id': None,
        }
        url = 'https://www.jindd.shop/addons/yun_shop/api.php'
        msg = ''
        response = requests.post(url, params=params, headers=self.headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json["result"] == 1 or response_json["result"] == 0:
                msg = f'✅每日任务完成'
            else:
                msg = f'"❌每日任务失败, ", {response_json["msg"]}'
        self.msg += msg
        print(msg)

    # 签到
    def signin(self):
        msg = ''
        response = requests.get(
            'https://www.jindd.shop/addons/yun_shop/api.php?i=12&uuid=0&type=1&mid=24109&version=v1.1.137&validate_page=1&route=plugin.sign.Frontend.Modules.Sign.Controllers.sign.sign&',
            headers=self.headers)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json["result"] == 1 or response_json["result"] == 0:
                msg = f'✅账号【{self.mid}】签到成功'
            else:
                msg = f'❌账号【{self.mid}】签到失败'
        self.msg += msg
        print(msg)

    # 元宝转换余额
    def coin_to_money(self):
        msg = ''
        print("🐹开始元宝转余额......")
        params = {
            'i': '12',
            'uuid': '0',
            'type': '1',
            'mid': f'{self.mid}',
            'version': 'v1.1.137',
            'validate_page': '1',
            'route': 'plugin.love.Frontend.Modules.Love.Controllers.withdraw.index',
            'change_value': f'{self.coin}',
            'withdraw_type': '4',
        }

        response = requests.get('https://www.jindd.shop/addons/yun_shop/api.php', params=params, headers=self.headers)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json["result"] == 1:
                msg = f'✅元宝转换余额成功, 本次转换元宝数量: {self.coin}'
            else:
                msg = f'❌元宝转换余额失败, {response_json["msg"]}'
        self.msg += msg
        print(msg)

    def money_to_wx(self):
        msg = ''
        params = {
            'i': '12',
            'uuid': '0',
            'type': '1',
            'mid': f'{self.mid}',
            'version': 'v1.1.137',
            'validate_page': '1',
            'route': 'finance.balance-withdraw.withdraw',
            'withdraw_type': '1',
            'withdraw_money': f'{self.credit}',
        }

        response = requests.get('https://www.jindd.shop/addons/yun_shop/api.php', params=params, headers=self.headers)
        if response and response.status_code == 200:
            response_json = response.json()
            print(response_json)
            if response_json["result"] == 1:
                msg = f'✅提现成功，本次提现金额: {self.credit}元'
            else:
                msg = f'❌提现失败, {response_json["msg"]}'
        self.msg += msg
        print(msg)

    def main(self):
        self.signin()
        time.sleep(random.randint(15, 20))

        for i in range(5):
            self.view_product()
            time.sleep(random.randint(20, 40))

        self.finish_today_task()
        time.sleep(random.randint(15, 45))

        self.userinfo()
        self.coin_to_money()
        time.sleep(random.randint(20, 40))

        if int(float(self.credit)) >= 5:
            msg = f'✅余额大于5元, 满足条件，开始提现......\n'
            self.msg += msg
            print(msg)
            self.money_to_wx()
        else:
            msg = f'❌余额:{self.credit}元, 不足5元, 不满足提现条件\n'
            self.msg += msg
            print(msg)

        # 推送
        send("金多多", self.msg)


if __name__ == '__main__':
    env_name = 'JDD_COOKIE'
    cookieStr = os.getenv(env_name)
    if not cookieStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    cookies = re.split(r'&', cookieStr)
    print(f"金多多共获取到{len(cookies)}个账号")
    for i, cookie in enumerate(cookies, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        JDD(cookie).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(20, 30))
