import os

import requests
from pyquery import PyQuery
from requests import Session, HTTPError, ReadTimeout


class Jd_bean:
    job_name = '京东会员页签到领京豆'

    index_url = 'https://vip.jd.com'
    info_url = 'https://vip.jd.com/member/getUserInfo.html'
    sign_url = 'https://vip.jd.com/sign/index'
    test_url = 'https://vip.jd.com/member/myJingBean/index.html'
    login_url = test_url

    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'Cookie': cookie,
        }

    def is_signed(self):
        info_url = 'https://vip.jd.com/member/getUserInfo.html'
        response = requests.post(info_url, headers=self.headers)
        print(response.text)
        # detail = self.session.get(self.info_url).json()
        # if detail.get('success'):
        #     user_info = detail['result']['userInfo']
        #     beans_count = user_info['userJingBeanNum']
        #     print('今日已签到: {}; 现在有 {} 个京豆.'.format(signed, beans_count))
        #
        # else:
        #     print('今日已签到: {}'.format(signed))
        #
        # return signed

    def sign(self):
        # 请求地址和参数
        # url = "https://api.m.jd.com/client.action"
        url = "https://api.m.jd.com/client.action?functionId=signBeanAct&body=%7B%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22rnVersion%22%3A%223.9%22%7D&appid=ld&client=apple&clientVersion=10.0.4&networkType=wifi&osVersion=14.8.1"
        #
        # params = {
        #     "functionId": "signBeanAct",
        #     "appid": "ld",
        #     "client": "apple",
        # }
        # 发送 POST 请求
        response = requests.post(url, headers=self.headers)
        print(response.text)

        # 检查响应
        if response.status_code == 200:
            result = response.json()
            print(result)  # 处理响应结果
        else:
            print(f"请求失败，状态码：{response.status_code}")




    def run(self):
        self.is_signed()
        # self.sign()
        # 假设 run 方法执行 is_signed 和 sign 方法
        # signed = self.is_signed()
        # if not signed:
        #     self.sign()


if __name__ == '__main__':
    env_name = 'JD_COOKIE'
    cookieStr = os.getenv(env_name)
    print("-----------------获取cookie:", cookieStr)
    if not cookieStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    bean_instance = Jd_bean(cookieStr)
    bean_instance.run()
