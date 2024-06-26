import requests
def goods_list():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'KUMI-TOKEN': 'WX_MP:o2Pmw5bD-of8g_EOb1zPoLl9cd4g',
        'PLATFORM': 'KUMI_KINDER',
        'PROJECT-ID': 'KINDER_36780507',
        'Referer': 'https://servicewechat.com/wxc412b42328595540/124/page-frame.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
        'xweb_xhr': '1',
    }

    json_data = {
        'desc': False,
        'page': 1,
        'pageSize': 10,
        'thresholdIn': [],
        'putBottom': True,
        'spuIdIn': [
            '240522MdRTeyD1gf',
            '240522YJM48fJs7r',
            '240522w7x51rWzxw',
            '240522GJDtVWzyQT',
            '240522a49wxb7arf',
            '240522xdnNp8zRFf',
            '240522uCwppsJMYs',
            '2405229uFe8JGRWs',
            '240605aAaQJMv2pM',
            '240527XuU7Hxpqc1',
        ],
    }
    url = 'https://mole.ferrero.com.cn/boss/boss/pointsmall/spu/list'
    response = requests.post(url, headers=headers, json=json_data)
    if not response or response.status_code != 200:
        print("获取商品信息异常")
        return
    response_json = response.json()
    if response_json['code'] == '1':
        list = response_json["data"]["items"]
        print(list)
        for good in list:
            name = good["name"]
            inventory = good["inventory"]
            maxPoint = good["maxPoint"]
            print(f'🐷{name} | 积分:{maxPoint} | 库存:{inventory}')


if __name__ == '__main__':
    goods_list()
