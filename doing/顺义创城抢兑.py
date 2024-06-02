"""
顺义创城抢兑

抓任意包请求头 x_applet_token
变量名: SY_token

cron: 0 8,12,20 * * *
const $ = new Env("顺义创城抢兑");
"""

import asyncio
import os
import aiohttp
import requests

async def cashout(x_applet_token):
    headers = {
        'Host': 'admin.shunyi.wenming.city',
        'Connection': 'keep-alive',
        'X-Applet-Token': x_applet_token,
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x1800312c) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx0a035430a2e3a465/154/page-frame.html'
    }
    url = 'https://admin.shunyi.wenming.city/jeecg-boot/applet/award/exchangeAward'
    body = '{"awardIds":["1788826595521810434"],"phone":"17854279565"}'
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.post(url, data=body) as response:
                response.raise_for_status()
                data = await response.json()
                if data.get('success'):
                    print(f"✅提现成功， {data['message']}")
                else:
                    print(f"❌提现失败， {data['message']}")
        except Exception as e:
            print(f"请求异常：{e}")

async def main():
    SY_token = os.getenv('SY_token')
    if not SY_token:
        print(f'⛔️未获取到ck变量：请检查变量 {SY_token} 是否填写')
        return

    tasks = [cashout(SY_token) for _ in range(15)]

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
