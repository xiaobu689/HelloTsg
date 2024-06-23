import importlib
import logging
import os
import random
import traceback
import requests
import time

# 定义需要运行的脚本类名称列表
jobs_skip = []  # 如果有跳过的脚本，可以在这里配置


def discover_jobs(directory):
    jobs_all = []
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py' and filename.startswith('jd_'):
            job_name = os.path.splitext(filename)[0]
            jobs_all.append(job_name)

    return jobs_all


def main(cookies):
    jobs = []
    for job_name in discover_jobs('./'):  # 指定脚本文件存放目录
        print(f"正在加载任务 {job_name}")
        if job_name not in jobs_skip:
            try:
                module = importlib.import_module(f'{job_name}')
                print(f"正在加载任务 {module}")
                job_class = getattr(module, job_name.capitalize())  # 假设脚本类名首字母大写
                print("---------job_class=", job_class)
                jobs.append(job_class)
                print(f"任务 {jobs} 加载成功")
            except ModuleNotFoundError as e:
                logging.error(f"未找到模块 {job_name}: {repr(e)}")
            except AttributeError as e:
                logging.error(f"未找到类 {job_name.capitalize()} 在模块 {job_name} 中: {repr(e)}")

    # 输出加载的任务类
    print("jobs=", jobs)

    jobs_failed = []

    for job_class in jobs:
        print(f"正在运行任务 {job_class}")
        try:
            headers = {'cookie': cookies}  # 构造请求头，示例中假设 cookie 是必要的头信息
            job = job_class(cookies)  # 实例化任务类对象，传入 headers
            job.run()  # 假设任务类有一个 run 方法用于执行任务
            time.sleep(random.randint(15, 30))  # 任务执行完成后随机等待一段时间
        except Exception as e:
            logging.error(f"任务 {job_class.__name__} 运行出错: {repr(e)}")
            traceback.print_exc()
            jobs_failed.append(job_class.__name__)

    # 输出任务汇总信息
    print('=================================')
    print(f'= 任务数: {len(jobs)}; 失败数: {len(jobs_failed)}')

    if jobs_failed:
        print(f'= 失败的任务: {jobs_failed}')
    else:
        print('= 全部成功 ~')

    print('=================================')


if __name__ == '__main__':
    env_name = 'JD_COOKIE'
    cookies = os.getenv(env_name)
    cookies = 'pt_key=AAJmdOT2ADBJ0yBmpOtDAxi2Gr6S_sYeZG29Cd3qH0O7DqSm1p6eaMILhZvlpMRIZ1NidC-dUGc;pt_pin=jd_561ef4e64818a;'
    if not cookies:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    main(cookies)
