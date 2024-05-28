"""
京东签到领京豆
定时设置：
cron: 35 8 * * *
const $ = new Env("京东");
"""
import logging
import os
import re
from json import dumps
from time import time
from loguru import logger
from task_request import req


# PushPlus推送
async def pushPlusAlert(**kwargs):
    title = kwargs.get("title", "")
    content = kwargs.get("msg", "")
    name = 'PUSH_PLUS_TOKEN'
    token = os.getenv(name)
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {name} 是否填写')
        exit(0)
    if token:
        meta = {
            "method": "POST",
            "url": "http://www.pushplus.plus/send",
            "data": dumps({
                'token': token,
                'title': title,
                'content': content,
            }),
            "headers": {"Content-Type": "application/json"}
        }
        res = await req(**meta)
        if res and not res.json().get('errcode'):
            return True
        else:
            return False


# 京豆签到
async def jd_app_sign_bean():
    jd_results = {
        "title": "京东签到领京豆",
        "results": []
    }
    logging.info("--------------任务开始--------------")
    env_name = 'JD_COOKIE'
    tokens = os.getenv(env_name)
    if not tokens:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    cookies = re.split(r'[@\n]', tokens)
    print(f"京东共获取到{len(cookies)}个账号")
    for i, token in enumerate(cookies, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        # 如果变量的名字是 "JD_cookie"，那么就继续执行
        pt_key, pt_pin = get_jd_cookie(token)
        result = {
            "code": 400,
            "msg": f'请输入pt_key及pt_pin',
            "time": int(time())
        }
        if not all([pt_pin, pt_key]):
            return result
        meta = {
            "method": "POST",
            "url": "https://api.m.jd.com/client.action",
            "params": {
                "functionId": "signBeanAct",
                # "body": '{"fp":"-1","shshshfp":"-1","shshshfpa":"-1","referUrl":"-1","userAgent":"-1","jda":"-1","rnVersion":"3.9"}',
                "appid": "ld",
                "client": "apple",
                # "clientVersion": "10.0.4",
                # "networkType": "wifi",
                # "osVersion": "14.8.1",
                # "uuid": "",
                # "openudid": "",
            },
            "cookies": {
                "pt_key": pt_key,
                "pt_pin": pt_pin
            }
        }
        res = await req(**meta)
        result.update({"msg": f'❌【账号{i}】{pt_pin} 的 cookie 已失效，请重新获取pt_key和pt_pin'})
        jd_results["results"].append(result)  # 将结果添加到jd_results中
        if res.status_code == 200:
            text = res.text
            # print(text)
            try:
                res = res.json()
                if res.get("errorMessage"):
                    print("出现错误， res=", res)
                    # cache.delete(pt_pin)
                else:
                    if res["data"]["status"] == '1':
                        result.update({
                            "code": 200,
                            "msg": f'✅【账号{i}】{pt_pin} {res["data"]["newUserAward"]["title"]}' if res[
                                "data"].get(
                                "newUserAward") else f"✅【账号{i}】{pt_pin} 今天已签到",
                        })
                        jd_results["results"].append(result)  # 将结果添加到jd_results中
                    else:
                        result.update({
                            "code": 200,
                            "msg": f"✅【账号{i}】{pt_pin} 今天已签到",
                        })
                        jd_results["results"].append(result)  # 将结果添加到jd_results中
            except Exception as e:
                logger.error(f'{text} {e}')
                result.update({"msg": f"❌【账号{i}】{pt_pin}京豆签到程序异常"})
                jd_results["results"].append(result)  # 将结果添加到jd_results中

    # PushPlus通知
    logger.info(jd_results["results"])

    await pushPlusAlert(**jd_results)
    logging.info("jd_app_sign_bean任务结束")

    return jd_results


def get_jd_cookie(cookie):
    # 只在第一个分号处分割 value
    pt_key, pt_pin = cookie.split(";", 1)
    # 去掉 pt_key 和 pt_pin 的前缀和后缀
    pt_key = pt_key.replace("pt_key=", "").strip()
    pt_pin = pt_pin.replace("pt_pin=", "").strip(";")

    return pt_key, pt_pin

