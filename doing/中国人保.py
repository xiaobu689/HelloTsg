import requests


def sign():
    headers = {
        'Host': 'mp.picclife.cn',
        #'Cookie': 'app-token=7b22757365724964223a226130346563663832633733363466313361393963396464656562373530353063222c2273657373696f6e4964223a2236336133353833302d313534322d346262612d386564352d356633393861616632313935222c2263726561746554696d65223a313731373630343433353930317d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218fe4a853c9212-0bdb20a88f46958-75070f20-329160-18fe4a853cadf0%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fzgrb.epicc.com.cn%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmZTRhODUzYzkyMTItMGJkYjIwYTg4ZjQ2OTU4LTc1MDcwZjIwLTMyOTE2MC0xOGZlNGE4NTNjYWRmMCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218fe4a853c9212-0bdb20a88f46958-75070f20-329160-18fe4a853cadf0%22%7D; es_cookie_vid=fe14d44fa42418f4c26f345ba0518889; s_fid=4860AF87E88D08E1-21183F4BA90651A6; s_getNewRepeat=1717528223233-New; s_vnum=1749064188265%26vn%3D1',
        'x-app-auth-type': 'APP',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 PBrowser/3.16.0 PiccApp/6.22.4 &&webViewInfo=3.16.0&&appInfo=piccApp&&appVersion=6.22.4',
        'Referer': 'https://mp.picclife.cn/dop/scoremall/mall/',
        #'x-app-auth-token': '7b22757365724964223a226130346563663832633733363466313361393963396464656562373530353063222c2273657373696f6e4964223a2236336133353833302d313534322d346262612d386564352d356633393861616632313935222c2263726561746554696d65223a313731373630343433353930317d',
        'x-app-score-channel': 'picc-app001',
        'Origin': 'https://mp.picclife.cn',
        'x-app-auth-url': 'https://mp.picclife.cn/dop/scoremall/mall/#/dailyAttendance?apply=app',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Site': 'same-origin',
        'X-Tingyun': 'c=B|tV_cscse5A0;x=597952d0af8647f5',
        'x-app-score-platform': 'picc-app',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Sec-Fetch-Mode': 'cors',
    }

    json_data = {}

    response = requests.post(
        'https://mp.picclife.cn/dop/scoremall/coupon/ut/signIn/get',
        headers=headers,
        json=json_data,
    )
    print(response.text)

def task_list():
    import requests
    headers = {
        'Host': 'mp.picclife.cn',
        'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22b7617974424ef68e693237b27fd2e244%22%2C%22first_id%22%3A%2218fe4a853c9212-0bdb20a88f46958-75070f20-329160-18fe4a853cadf0%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmZTRhODUzYzkyMTItMGJkYjIwYTg4ZjQ2OTU4LTc1MDcwZjIwLTMyOTE2MC0xOGZlNGE4NTNjYWRmMCIsIiRpZGVudGl0eV9sb2dpbl9pZCI6ImI3NjE3OTc0NDI0ZWY2OGU2OTMyMzdiMjdmZDJlMjQ0In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22b7617974424ef68e693237b27fd2e244%22%7D%2C%22%24device_id%22%3A%2218fe4a853c9212-0bdb20a88f46958-75070f20-329160-18fe4a853cadf0%22%7D; app-token=7b22757365724964223a226130346563663832633733363466313361393963396464656562373530353063222c2273657373696f6e4964223a2264386535323564302d643532322d346362322d623530382d663033333635373438323532222c2263726561746554696d65223a313731373734353532353833367d; es_cookie_vid=fe14d44fa42418f4c26f345ba0518889; s_fid=4860AF87E88D08E1-21183F4BA90651A6; s_getNewRepeat=1717604747786-Repeat; s_vnum=1749064188265%26vn%3D2',
        'x-app-auth-type': 'APP',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 PBrowser/3.16.0 PiccApp/6.22.4 &&webViewInfo=3.16.0&&appInfo=piccApp&&appVersion=6.22.4',
        'Referer': 'https://mp.picclife.cn/dop/scoremall/mall/',
        'x-app-auth-token': '7b22757365724964223a226130346563663832633733363466313361393963396464656562373530353063222c2273657373696f6e4964223a2264386535323564302d643532322d346362322d623530382d663033333635373438323532222c2263726561746554696d65223a313731373734353532353833367d',
        'x-app-score-channel': 'picc-app001',
        'Origin': 'https://mp.picclife.cn',
        'x-app-auth-url': 'https://mp.picclife.cn/dop/scoremall/mall/#/dailyAttendance?apply=app',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Site': 'same-origin',
        'X-Tingyun': 'c=B|tV_cscse5A0;x=e63f6ce8e46a4117',
        'x-app-score-platform': 'picc-app',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Sec-Fetch-Mode': 'cors',
    }

    json_data = {
        'type': 1,
        #'ver': 'AZzqU5arEd+1YXgLSgr0wyGpIm9skwPB6eiUvGy/Zr3hIdPaVurjPj7RIWkj/pajI55+k4Tl4DD3FXynTceGXJl38rlK4ZPkDSUXaHlQjcwuOlJAdJ0hubpv0NYfkbDa93UQj1uTftP2GMaRydkmca/TuZXKMJVoVcPzZj8uUnCS/EN2BpTSWJ/YvZ9zgSOz6C1GWZO6MwF8kcEE2aR50RlH9230JqqIUIWrAFO9VQ1UBUmBSZOzDyDxUaBlHVAkUPeOM0YaT7wd/kXk/JmCgduy2k3fy974XyNObW+xDBssgpZa72k6DOHot/gCoZZnAfF4OgFEesMRz80TcfsgPQ==',
        'localizedModel': '',
        'platform': '',
    }

    response = requests.post(
        'https://mp.picclife.cn/dop/scoremall/coupon/ut/task/list',
        headers=headers,
        json=json_data,
    )
    print(response.text)


if __name__ == '__main__':
    sign()
    task_list()
