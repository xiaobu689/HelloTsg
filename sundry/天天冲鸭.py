"""
天天冲鸭

路径：ZFB搜索 “天天冲鸭”
用途：签到领积分，积分兑换话费，仅支持电信手机号
变量名：ttcy_token
格式： 任意请求头抓 Authorization 值

定时设置：每天一次就行，时间随意
cron: 33 8 * * *
const $ = new Env("天天冲鸭");
"""
import requests


class TTCY():
    def __init__(self):
        self.cookie = ''

    def duck_sign(self):
        headers = {
            'Host': 'gdbizweb.alipay-eco.com',
            'Accept': '*/*',
            'Accept-Charset': 'utf-8',
            'userId': '2088612491318281',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Content-Type': 'application/json',
            'Content-Length': '24',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 ChannelId(8) Ariver/1.1.0 AliApp(AP/10.5.88.6000) Nebula WK RVKType(0) AlipayDefined(nt:WIFI,ws:390|844|3.0) AlipayClient/10.5.88.6000 Language/zh-Hans Region/CN NebulaX/1.0.0 XRiver/10.2.58.1',
            'Connection': 'keep-alive',
            'Referer': 'https://2021004113642010.hybrid.alipay-eco.com/2021004113642010/0.2.2404241615.37/index.html#pages/index/index',
        }

        params = {
            'channelSource': 'self',
            'token': 'e2d658a4d7d24d3dad8e7cd12bdf3baa',
        }

        json_data = {
            'channelSource': 'self',
        }

        response = requests.post(
            'https://gdbizweb.alipay-eco.com/gdbizweb/task/signin/execute/v2',
            params=params,
            headers=headers,
            json=json_data,
        ).json()
        print(response)

    def main(self):
        self.duck_sign()

        # 通知
        # send(title, msg)


if __name__ == '__main__':
    # # env_name = 'TTCY_COOKIE'
    # # cookie = os.getenv(env_name)
    # # # if not cookie:
    # # #     print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
    # # #     exit(0)
    # token = ''

    TTCY().main()
