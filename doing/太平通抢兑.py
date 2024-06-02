import os
import asyncio
import aiohttp


async def exchange_jd(token, jd_id):
    url = "https://ecustomer.cntaiping.com/campaignsms/coin/exchange/receive"
    headers = {
        'Host': 'ecustomer.cntaiping.com',
        'x-ac-channel-id': 'KHT',
        'Sec-Fetch-Site': 'cross-site',
        'x-ac-token-ticket': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOltdLCJzdWIiOiIxNzE1NDE0MjQyODQ0RG5XQ20xdGxSMnl1WFVyS051NkNxQyIsInVzZXJfbmFtZSI6IjEzMDA0MTU5OTUyMzE0NzM2NjQiLCJsb2dpY19pZCI6ODk5Mjc4MywiaXNzIjoia2h0LnRhaXBpbmciLCJzY29wZSI6W10sImdyYW50X3R5cGUiOiJwYXNzd29yZCIsImp0aSI6IjE3MTU0MTQyNjM3NzJDbDFRV0ttVzNjU3hENHhRcVNyakNWIiwiYWRkaXRpb25hbEluZm8iOnt9LCJpYXQiOjE3MTU0MTQyNjMsImV4cCI6MTc4MDIxNDI2MywiYXV0aG9yaXRpZXMiOltdLCJjbGllbnRfaWQiOiJUUFRfQVBQIn0.Og7djzpD_7QygeWYN65ziySu5kaxBtvgaV4A-q59_o-Op-Y0QJAb2vV6w8cohn78i43TZ7lYUskM9i42VJh87oVzWqTkft1uAgCwx3boaEFrtTd3434-dGpSYu33O-5UJnozaFBd6e08MLk_uZzfaGNh_S2uHtoeegCUnZloge4',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Accept': 'application/json;charset=UTF-8',
        'Origin': 'https://ecustomercdn.itaiping.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS',
        'Referer': 'https://ecustomercdn.itaiping.com/',
        'x-ac-mc-type': 'gateway.user',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
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
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOltdLCJzdWIiOiIxNzE1NDE0MjQyODQ0RG5XQ20xdGxSMnl1WFVyS051NkNxQyIsInVzZXJfbmFtZSI6IjEzMDA0MTU5OTUyMzE0NzM2NjQiLCJsb2dpY19pZCI6ODk5Mjc4MywiaXNzIjoia2h0LnRhaXBpbmciLCJzY29wZSI6W10sImdyYW50X3R5cGUiOiJwYXNzd29yZCIsImp0aSI6IjE3MTU0MTQyNjM3NzJDbDFRV0ttVzNjU3hENHhRcVNyakNWIiwiYWRkaXRpb25hbEluZm8iOnt9LCJpYXQiOjE3MTU0MTQyNjMsImV4cCI6MTc4MDIxNDI2MywiYXV0aG9yaXRpZXMiOltdLCJjbGllbnRfaWQiOiJUUFRfQVBQIn0.Og7djzpD_7QygeWYN65ziySu5kaxBtvgaV4A-q59_o-Op-Y0QJAb2vV6w8cohn78i43TZ7lYUskM9i42VJh87oVzWqTkft1uAgCwx3boaEFrtTd3434-dGpSYu33O-5UJnozaFBd6e08MLk_uZzfaGNh_S2uHtoeegCUnZloge4'
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        return

    tasks = [exchange_jd(token, jd_id) for _ in range(1)]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print(f"\n======== ▷ 开始抢兑 ◁ ========")
    asyncio.run(main())
