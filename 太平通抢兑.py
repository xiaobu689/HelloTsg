import os
import asyncio
import aiohttp


async def exchange_jd(token, jd_id):
    url = "https://ecustomer.cntaiping.com/campaignsms/coin/exchange/receive"
    headers = {
        "Accept": "application/json;charset=UTF-8",
        "x-ac-black-box": "",
        "x-ac-token-ticket": token,
        "Sec-Fetch-Site": "cross-site",
        "x-ac-channel-id": "KHT",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "content-type": "application/json",
        "Origin": "https://ecustomercdn.itaiping.com",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS",
        "Referer": "https://ecustomercdn.itaiping.com/",
        "x-ac-mc-type": "gateway.user",
        "Content-Length": "2",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
    }
    json_data = {"id": jd_id, "appVersion": "4.0.2"}
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.post(url, json=json_data, verify_ssl=False) as response:
                response.raise_for_status()
                data = await response.json()
                if data.get('success'):
                    print(f"✅兑换成功， {data}")
                else:
                    print(f"❌兑换失败， {data}")
        except aiohttp.ClientError as e:
            return e


async def main():
    # jd_ids: 66|1元 169|2元 120|5元 121|10元
    jd_id = 121
    env_name = 'tptCookie'
    token = os.getenv(env_name)
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        return

    tasks = [exchange_jd(token, jd_id) for _ in range(1)]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print(f"\n======== ▷ 开始抢兑 ◁ ========")
    asyncio.run(main())
