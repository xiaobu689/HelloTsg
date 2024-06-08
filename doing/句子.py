print("已废")
exit(0)

import os
import random
import re
import threading
import time
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

class JRJZ:
    def __init__(self, token):
        self.token = token
        self.money = 0
        self.openid = ''
        self.headers = {
            'authority': 'api.juzi.co',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': 'https://servicewechat.com/wx3e3540cb2012ea1f/26/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'token': token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }

    def get_no_repeat_sentence(self):
        while True:
            print("💩开始获取句子......")
            time.sleep(random.randint(30, 55))
            quote = daily_one_word()
            print(f'💩句子: {quote}')
            if not quote:
                continue
            data = {'juzi': quote}
            url = 'https://api.juzi.co/sentence/repeatedList'
            response = requests.post(url, headers=self.headers, data=data)

            if response.status_code != 200:
                continue

            response_json = response.json()
            if response_json['code'] != 200:
                continue

            sentences = response_json.get('data', [])
            if len(sentences) <= 0:
                print(f'✅-----句子不重复，可以发布-----✅')
                return quote  # 返回不重复的句子
            else:
                print(f'🤡句子重复 | 重复数量{len(sentences)} | 继续查找......')
                continue

    def write_sentence(self):
        quote = self.get_no_repeat_sentence()
        if quote is not None:
            print("🐹开始发布句子......")
            json_data = {
                'juzi': quote,
                'original': 'false',
                'writer': '',
                'source': '',
                'tagsValue': '随笔',
                'tagslength': '0',
                'tags': '随笔',
            }
            url = 'https://api.juzi.co/sentence/execWrite'
            response = requests.post('https://api.juzi.co/sentence/execWrite', headers=self.headers, data=json_data)
            if response and response.status_code == 200:
                response_json = response.json()
                if response_json and response_json['code'] == 200:
                    print(f'✅今日句子发布成功')
                else:
                    print(f'❌今日句子发布失败 | {response_json["msg"]}')
            else:
                print(f'❌今日句子发布失败：{response.text}')
        else:
            print(f'❌今日句子发布失败, 取消发布')

    def my_info(self):
        response = requests.get('https://api.juzi.co//member/getWalletInfo', headers=self.headers)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                money = f'{response_json["data"]["member"]["money"]}'
                self.money = money
                self.openid = response_json['data']["member"]["openid"]
                print(f'🐹昵称：{response_json["data"]["member"]["nickname"]}')
                print(f'🐶余额：{response_json["data"]["member"]["money"]}')
                print(f'🐱句子数量：{response_json["data"]["member"]["juzi_count"]}')
                print(f'---------------------------')

    def person_first_sentence(self):
        params = {
            'openid': self.openid,  # 用户的openid
            'page': '1',
        }
        try:
            response = requests.get('https://api.juzi.co/member/index', params=params, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            if response_json['code'] != 200:
                return None
            sentences = response_json['data'].get("sentenceAll", [])
            if not sentences:
                return None
            for sentence in sentences:
                print("句子:", sentence)
                if sentence["checkResult"] == "":
                    return sentence
            return None
        except requests.RequestException as e:
            print(f"获取句子列表失败: {e}")
            return None

    def sentence_like(self, sid):
        data = {
            'sid': sid,  # '6625938'
        }
        response = requests.post('https://api.juzi.co/sentence/slike', headers=self.headers, data=data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'❤️对句子{sid}点了赞 | {response_json["msg"]}')  # 喜欢成功
        else:
            print(f'❌对句子{sid}点赞失败 | {response.text}')

    def sentence_share_callback(self, sid):
        # https://api.juzi.co/sentence/makePic?openid=165fccff78fb3d6021f279ced2d5cf93&share=d37850c6d0383eac5edeba21b6e89cf4
        data = {
            'user_openid': self.openid,  # 分享者的openid， url中share对应的值
            #'code': '0e3scs200mechS12rE300dxRKi1scs2e',
            'provider': 'weixin',
            'sentence_id': sid,  # 句子信息的openid  # '4225a8430480a2176a6ffeb36c3caf17'
        }
        print("------------1111111111111data=", data)
        response = requests.post('https://api.juzi.co//sentence/picShareCallback', headers=self.headers, data=data)
        print(response.text)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200 and response_json["msg"] == "ok":
                print(f'分享回调成功 | {response_json["msg"]}')

    def cashout(self):
        print(f'---------------------------')
        print(f'💰余额：{self.money}元, 满足提现条件，开始提现......')
        data = {
            'price': '3',
        }
        response = requests.post('https://api.juzi.co/member/cashOut', headers=self.headers, data=data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'提现成功 | {response_json["msg"]}')
            elif response_json['code'] == 202:
                print(f'余额不足')
            else:
                print(f'提现失败 | {response_json["msg"]}')

    def assist_user(self, sid, token):
        try:
            jrjz_instance = JRJZ(token)
            jrjz_instance.my_info()
            jrjz_instance.sentence_share_callback(sid)
            time.sleep(random.randint(20, 30))
            jrjz_instance.sentence_like(sid)
            time.sleep(random.randint(30, 60))
            logging.info(f"账号{token[:8]} 助力完成")
        except Exception as e:
            logging.error(f"账号{token[:8]} 发生错误：{e}")

    def assist_all_users(self, sentence_openids, tokens):
        threads = []
        for sid in sentence_openids:
            print("第一篇文章sid=", sid)
            for token in tokens:
                if token != self.token:
                    print(f"第一个用户开始给本账号助力")
                    t = threading.Thread(target=self.assist_user, args=(sid, token))
                    threads.append(t)
                    t.start()
        for t in threads:
            t.join()

    def main(self):
        self.person_first_sentence()
        self.my_info()
        # time.sleep(random.randint(15, 30))

        # 发布句子
        # self.write_sentence()
        # time.sleep(random.randint(30, 50))
        if float(self.money) >= 3.0:
            self.cashout()
        else:
            print(f'---------------------------')
            print(f'💰余额不足，跳过提现 | 当前金额：{self.money}元')

if __name__ == '__main__':
    env_name = 'JRJZ_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = 'AVZXVwgAAARUDgVTVFcAVwVWDgdTBgoGAlMBXVVUVAE=&CwEHVw5WUlwCXVtWVAFWCwcKDgNXBwEFBwZVC1RXUFU='
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"今日句子共获取到{len(tokens)}个账号")
    jrjz_instances = []
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        jrjz_instance = JRJZ(token)
        jrjz_instance.main()
        jrjz_instances.append(jrjz_instance)
        print("\n随机等待30-60s进行下一个账号")
        # time.sleep(random.randint(30, 60))

    # 获取所有用户的第一篇文章
    sentence_openids = []
    for jrjz_instance in jrjz_instances:
        first_sentence = jrjz_instance.person_first_sentence()
        if first_sentence:
            sentence_openids.append(first_sentence)

    print("获取到了所有用户的第一篇文章sentence_openids=", sentence_openids)

    # 为所有用户助力
    for jrjz_instance in jrjz_instances:
        print("开始为所有用户助力")
        jrjz_instance.assist_all_users(sentence_openids, tokens)

    print("所有账号助力完成")
