import requests
import time
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import qianwen_messages, make_request
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
timestamp = str(int(time.time() * 1000))
def lottery():
    headers = {
        'Host': 'koplus.icoke.cn',
        'Connection': 'keep-alive',
        'x-sg-timestamp': timestamp,
        'content-type': 'application/json',
        'Authorization': 'MP c5ce060c32d04e4cb410fb1fc9c1e3af',
        'SV': '5',
        'x-sg-signature': '5dd59fe87917ac8bf15a044f577e06292b9bf7d096fc4b553d9cd7ff0faed1d3',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003132) NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxa5811e0426a94686/388/page-frame.html',
    }

    json_data = {
        'pincode': 'http://i.icoke.cn/G/4ASRJGJ655OVYZ2P',
        'isAuthLbs': True,
        'latitude': 31.184159071180556,
        'longitude': 121.55051920572917,
        'accuracy': 35,
        'altitude': 9.169983863830566,
        'speed': -1,
    }
    url = 'https://koplus.icoke.cn/cre-bff/wechat/user/lotteries/G/scan-draw'
    response = make_request(url, json_data=json_data, method='post', headers=headers)
    print(response)



if __name__ == '__main__':
    lottery()
