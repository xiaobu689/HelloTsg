# -*- coding: utf-8 -*-
import asyncio
from httpx import AsyncClient
from loguru import logger


# 请求函数
async def req(**kwargs):
    url = kwargs.get("url", "")
    if not url:
        return None
    headers = kwargs.get("headers", {"User-Agent": "okhttp/3.12.1;jdmall;android;version/10.3.4;build/92451;"})
    proxy = None
    proxies = kwargs.get("proxies", {"all://": proxy} if proxy else {})
    try:
        async with asyncio.Semaphore(100):
            async with AsyncClient(http2=kwargs.get("http2", False), proxies=proxies, headers=headers,
                                   cookies=kwargs.get("cookies", {}), verify=False,
                                   trust_env=False,
                                   follow_redirects=True, timeout=20) as client:
                rs = await client.request(method=kwargs.get("method", "GET"), url=url, params=kwargs.get("params", {}),
                                          data=kwargs.get("data", {}), json=kwargs.get("json", {}),
                                          files=kwargs.get("files", {}),
                                          headers=headers)
                return rs
    except Exception as e:
        logger.error(f'req {url} {e}')
        retry = kwargs.get("retry", 0)
        retry += 1
        if retry > 2:
            return None
        return await req(**kwargs | {"retry": retry})
