import requests
"""
华润通

抓任意包请求头 token
变量名: HYT

cron: 35 10 * * *
const $ = new Env("华润通");
"""
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class HYT():
    name = "华润通"

    def __init__(self, tokenStr):
        self.token = tokenStr
        self.headers = {
            'Host': 'appnews.qingdaonews.com',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            #'Cookie': 'appnews_deviceInfo=YTo1OntzOjEyOiJtYWNoaW5lX2NvZGUiO3M6MzY6IjFGMEQzRDBGLTI3ODEtNEMxMS05QUU3LTkyMzc5ODA2MzU0RSI7czo3OiJ1c2VyX2lkIjtzOjg6IjExNzc5NzMxIjtzOjk6InVzZXJfdHlwZSI7aToxO3M6OToidHlwZV90ZXN0IjtzOjM6ImFwaSI7czo5OiJ0X3VzZXJfaWQiO3M6ODoiMTQzMjY4MjEiO30%3D; NSC_bqqofxt=ffffffff09022cbc45525d5f4f58455e445a4a423660; sto-id-20480-appnews_pool=KNDCAKAKFAAA; password=9i%2FNdBIygBSRfCVNaIgoWzwkPMuk9ncH; password_NS_Sig=oenCV6idkGc14wbC; token=9i%2FNdBIygBSRfCVNaIgoWzwkPMuk9ncH; uid=11779731; username=TZA7%2BiiCuW5rks5Gnrjvkw%3D%3D; username_NS_Sig=oenCV6iZ_VRRqFbO; PHPSESSID=664b075b787c13.93774969; PHPSESSID_NS_Sig=oenCV6manzgktFOz',
            #'vtoken': 'GKxKSCYLrVWSuTZrL-VmJ1Md5Gp_ZcxNxkqt8CrvwwLkEOaFAbN5lLaPhnMb78GIyYuVOFkbJssUlesI0_OU7IH8MSLwZpucSoGEYeEfyWMi-1aaMTyjRINmQxF9zVZAg19PD-_M5P54IxfLhGX_b78aFn-ndv0-JaDHIdO3CY4U8gQIytwVz_XnQTOPCDiB4Nspm-RlwQv7A3_vpS0_1ZOH91XQIkiVY09dmaeBTCzWx-nIiqgiHHTtZu7w1ufPSImjHKkEslutpGDztXAr0mT6ehCSzS5pEjQgTMQ-VH_AxefB2w0tKoAyGfABW7AtW2gwyicNMDTjaPPP5kyjuw',
            'User-Agent': 'NewsApp/qdnews/6.10.10 (iPhone; iOS 16.6; Scale/3.00)',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

    def userInfo(self):
        headers = {
            'Host': 'mid.huaruntong.cn',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': 'https://cloud.huaruntong.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 hrtbrowser/5.4.6 grayscale/0',
            'Referer': 'https://cloud.huaruntong.cn/'
        }
        json_data = {
            'auth': {
                'appid': 'API_AUTH_H5',
                'nonce': '9e8bab25-3c2c-4355-acb2-8af49c69dfb9',
                'timestamp': 1716540549369,
                'signature': '4a970bf123f6498b5d76eb844e741b81',
            },
            'channelId': 'APP', # 定值
            'sysId': 'T0000001', # 定值
            'transactionUuid': '230fc8a4-cb49-493a-8bf9-cb72a006da1f',
            'pointsType': '100000', # 定值
            'token': '364d7d64b3299b1d27b6061c404097992',
        }
        response = requests.post('https://mid.huaruntong.cn/api/points/querySummary', headers=headers, json=json_data).json()
        print(response)
        if response['code'] == "S0A00000":
            print("----------------------------")
            print(f'🧑‍✈️金币：{response["data"]["data"]["cPoints"]["points"]}')
            print("----------------------------")


    def sign(self):
        headers = {
            'Host': 'mid.huaruntong.cn',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': 'https://cloud.huaruntong.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x1800312e) NetType/WIFI Language/zh_CN miniProgram/wx66c62601b987e69d',
            'Referer': 'https://cloud.huaruntong.cn/',
            'X-Hrt-Mid-Appid': 'API_AUTH_WEB',
            'Sec-Fetch-Dest': 'empty',
            'Connection': 'keep-alive',
        }

        json_data = {
            'key': 'PU1WkZzN5JrEw/OZi5ugumYkkf8MMa/GYf7skV8l5VZkcX7Nw9+tBXTlGb6B/YAaf/u4Uaxxto+alHU0+8mQcz5B/L6gw3LzcmVoC77BIg3Q5snnN/4278wzbzLp+IMYL0+t2sTQEgzlTAtHyrKYku0ESQcrzv9YhVdu5OxVkRQ=',
            'data': 'MUMdugya7Y2xB0QG/SUc5V0KniL3AMLM3LHhhRPlYDODesY2OP927nMD24uPj6ElyN4TOf04tPGNF5YKw2eGo0gonrkkh/5eJfazWnwqzaZugFtEnHvPxsS5v1Kg1kQQ2RMR64SxZ/Ha9V5/u9YAmLoyPp3s828fSt+Q9xAabLEnet4hzKm/N+VgzHAlEQDM6hcJu58EB8hXdUOKTMB0b4sb+UOt8I7FqK4yghXWadguC8W1JfgKNSmH81iAhl6xz5NwRuZ/gOsXL3QTOjWI2giQR1Ff4r+aDPxwrG1vzLEc3M4VS1VBjGYXp/B6/vLJzLHDeqyEpEn/fjIwh0Qe3/HjBQSFpQZ2dO9Pp1mm2yvO2Iu1g3b1GjmSMr97N288EnTcenjkLe44HJN7OnmR5L9FWMUexhFZ8r2o0CMXqoyCpLp+vscg4SMtS5YW7BF1Nj+ldm6Fi7DG5VVFOhrPxgLclaat0L8P2TXzfXBh4P0GAf1wyf1VI/tkMeRDjc3R',
        }

        url = 'https://mid.huaruntong.cn/api/points/saveQuestionSignin'
        response = requests.post(url, headers=headers, json=json_data).json()
        if response['code'] == "S0A00000":
            print('签到成功')
        elif response['code'] == "E1B00101":
            print('重复签到')
        else:
            print('签到失败, ', response)

    def main(self):
        self.userInfo()
        self.sign()


if __name__ == '__main__':
    # env_name = 'SHCN_TOKEN'
    # tokenStr = os.getenv(env_name)
    # if not tokenStr:
    #     print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
    #     exit(0)

    HYT('').main()