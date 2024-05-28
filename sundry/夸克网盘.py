"""
夸克网盘签到
定时设置：
cron: 43 7 * * *
const $ = new Env("夸克网盘");
"""
import logging
import json
import os
import re
import requests
from sendNotify import send


# PushPlus推送
def pushPlusNotify(**kwargs):
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
            "data": json.dumps({
                'token': token,
                'title': title,
                'content': content,
            }),
            "headers": {"Content-Type": "application/json"}
        }
        res = requests.post(meta['url'], data=meta['data'], headers=meta['headers'])
        if res and not res.json().get('errcode'):
            return True
        else:
            return False


# 夸克签到
def kk_sign():
    msg = ""
    logging.info("----------------夸克签到任务开始----------------")
    env_name = 'KK_COOKIE'
    token = os.getenv(env_name)
    token = '_UP_A4A_11_=wb96217167c246428c415e6cfe91882f; _UP_D_=pc; _UP_F7E_8D_=0z44HdIBxZZ%2BcDshYwkP7rClYOQkRQ1Wta2DY6yUrM%2BctZa7SKqcWBLdUtkAVl5Xw7HVs6f66k5LHpvA%2Fhicy1HUTu2LBlCPom4qTWeMFqCgN55FQx3lIyu%2B1OsWIKjG1w4pOGWcZjvuo4m2jHof9eRj66wpeTPO4r7NBD%2F4wEE0IpjIBHWretgcndtvmRjOGR1EaoCa5E2gZsHOrMm3YOHZ47Hvtvq2wLtchZ7GH2KZHru1xRmXkslz1%2FDvaW%2BhIvX3kcWZgFdVoMDN0Rc4966oeF1eZCXXLeEOyzEKqUvdldBvB7trVMH3IhYSoUw2AYTF7eNiF%2BU9DgASvb4Vfvosp%2BEFl7vny0TNscSZMOl8DcfixlwkYTpwSCY4564fHGA9cyxKste3pBRULSTR8JY7n3P6zUYaG%2BofGCzsMul3NGY6wl6lBISYJ2cSDS100Hjqhb3FcWuLwSSSdvGDxA%3D%3D; _UP_30C_6A_=st9656201981y0dvap77jkakmd529xci; _UP_TS_=sg17f2b2f6d6e9379b4611c12f67408579b; _UP_E37_B7_=sg17f2b2f6d6e9379b4611c12f67408579b; _UP_TG_=st9656201981y0dvap77jkakmd529xci; _UP_335_2B_=1; __pus=6a43efc597d327ef8820114f4c94da6dAATtluQccyYXZtb95w5Zo6Y1I8GrhZaothJ87mFB/mQy0OI23J9R09chpQ2ELwuzFDPJt08n6GH1gbBNmupSvcf0; __kp=174a5e10-07a6-11ef-83af-3b5ee77bbc2f; __kps=AAR3xdR6DIGWIGVVjbX/TkZE; __ktd=iD2Jbc1omzRiPpW6Ht1wZg==; __uid=AAR3xdR6DIGWIGVVjbX/TkZE; tfstk=fcjSgrsMtbcWrgWXtUe2cQ3942KQQ_ZaFv9dI9nrp3K-v66HgLuzrePCl6C2wgzkasOCQ9meaT-8d61ONe5CK8vp96CBTaz4bTXkxHFNOlrNEl0OnlCWJBEYpp9I9pjHyoWkxHF4ZG5BzTf6Lvg8VHeXDp9nJHnd9IBvipvKwpn8htdDpHHJyHLvMLJi22hzXS90PQB7Tvj1kbo_eTOjvcMMQUedF2osfi9WcTXJGUT5cLTW6E8mzYjRg9IPqE4muHXV56_d6SuywN91GF771011ZpCX4Ge3rEYdAM9coWgB1wBPSwLbeuBXVQTXFUMSJ3_dZMTlPv2GH3CcSCY8oSvf4G8BsEGYwtWXwF_CaSmpaN6AGFSqgc-OSssBWhIydcRsH90IhFmphCybh20elZlhgrCXSdTJnKj4h-gFtUpDhCybh20HyKvc0-wj86f..; __puus=9b5dfde513be3fed4307799b9639cae6AAQehENnqJBcFLNTVG+jo2xzDgpMe5uABLic1n5tw0lzSQWorkK5G4TsGLa8IVf+LdOy4tqFAil0xmmGFli+AgsbnGrQx52n6TbkIrQGtPXHlYRuwJEDfze36O6sTuSxSfliiF+2eHKbIr8enQ0a9HIYheKFVH363Jo+94+Cbdjmj7+Ws6kiek9vByFUlfOCkXOyQpb3aTm8S8WBN1WZE5T/'
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    cookies = re.split(r'[@\n]', token)
    print(f"夸克网盘共获取到{len(cookies)}个账号")
    for i, cookie in enumerate(cookies, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        # 如果变量的名字是 "KK_COOKIE"，那么就继续执行
        if not [cookie]:
            msg = "未检测到CK"
            return msg
        meta = {
            "method": "GET",
            "url": "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info?pr=ucpro&fr=pc&uc_param_str=",
            "headers": {
                "Cookie": cookie,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
        }
        res = requests.get(meta['url'], headers=meta['headers'])
        res_dict = res.json()
        if res_dict['status'] == 200:
            is_sign = res_dict["data"]["cap_sign"]["sign_daily"]
            if is_sign:
                number = res_dict["data"]["cap_sign"]["sign_daily_reward"] / (1024 * 1024)
                msg = f"✅今天已经签到过了,签到奖励容量 {int(number)} MB"
            else:
                sign_url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign?pr=ucpro&fr=pc&uc_param_str="
                payload = json.dumps({"sign_cyclic": "True"})
                meta.update({
                    "method": "POST",
                    "url": sign_url,
                    "data": payload
                })
                res = requests.post(meta['url'], data=meta['data'], headers=meta['headers'])
                res_dict = res.json()
                reward = res_dict["data"]["sign_daily_reward"] / (1024 * 1024)
                msg = f"✅签到成功，今日签到奖励 {int(reward)} MB"
        else:
            msg =  f"❌账号异常，签到失败，token 已失效."
    # PushPlus通知
    logging.info(msg)
    send("夸克网盘签到", msg)
    logging.info("夸克签到任务结束")

# if __name__ == '__main__':
#     kk_sign()
