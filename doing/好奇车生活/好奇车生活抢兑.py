import requests
import time

accountId = 'wx8c6e8a965158ad6c'

def main():
    global accountId
    print(f'用户：{accountId}开始兑换')

    queryPointsMallCardList = common_get('/pointsmall/queryPointsMallCardList?isGroup=false')
    print("----------------1111111111111111111wx8c6e8a965158ad6c=", queryPointsMallCardList)
    for item in queryPointsMallCardList['result']['全部']:
        print(f"兑换商品：{item['cardName']} id: {item['id']} 兑换所需积分：{item['exchangePointsValue']} 兑换所需金额：{item['exchangeMoneyValue']}")

    # pointsMallCardId = Cheryfs_GIFTID
    # queryByPointsMallCardId = common_get(f"/pointsmall/queryByPointsMallCardId?pointsMallCardId={pointsMallCardId}")
    # print(f"开始兑换{queryByPointsMallCardId['result']['cardName']}")
    #
    # exchangeCount = 1
    # exchangeType = queryByPointsMallCardId['result']['exchangeType']
    # exchangeNeedPoints = queryByPointsMallCardId['result']['exchangePointsValue']
    # exchangeNeedMoney = queryByPointsMallCardId['result']['exchangeMoneyValue']
    #
    # for i in range(20):
    #     for j in range(2):
    #         exchange = common_get(f"/pointsmall/exchangeCard?pointsMallCardId={pointsMallCardId}&exchangeCount={exchangeCount}&mallOrderInputVoStr=%7B%22person%22:%22%22,%22phone%22:%22%22,%22province%22:%22%22,%22city%22:%22%22,%22area%22:%22%22,%22address%22:%22%22,%22remark%22:%22%22%7D&channel=1&exchangeType={exchangeType}&exchangeNeedPoints={exchangeNeedPoints}&exchangeNeedMoney={exchangeNeedMoney}&cardGoodsItemIds=")
    #     time.sleep(0.1)
    #
    # time.sleep(60)


def common_get(url):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Referer': 'https://servicewechat.com/wx8c6e8a965158ad6c/31/page-frame.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
        'appid': 'wx8c6e8a965158ad6c',
        'tenantid': '619669306447261696',
        'wxappid': 'wx8c6e8a965158ad6c',
        'xweb_xhr': '1',
    }
    url = f"https://channel.cheryfs.cn/archer/activity-api{url}"
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)  # Print response data for debugging
    return data

if __name__ == "__main__":
    main()
