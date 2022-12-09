#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Created by main_v7.py
# @Author: Snyder
# @Date: 2022/12/7
# @Time: 09:44
# @Email: snyder.xiang@gmail.com
import json
import os
import random
import threading
import time

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import fire
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from service.pageLink import main as link_main
import requests
from create_proxy_auth_extension import create_proxy_auth_extension


def get_proxy(type='smartproxy'):
    print('获取代理IP')
    proxy_list = []
    if type == 'smartproxy':
        proxy_url = 'https://api.smartproxy.cn/web_v1/ip/get-ip?app_key=21824639440f11a4e83a6b1cd3ea79e8&pt=9&num=500&cc=US&protocol=1&format=json&nr=%5Cr%5Cn'
        response = requests.get(url=proxy_url)
        if response.status_code != 200:
            return
        response = json.loads(response.text)
        if response['code'] == 200:
            proxy_list = response['data']['list']
            return proxy_list
    if type == 'ipipgo':
        proxy_url = 'http://api.ipipgo.com/ip?cty=US&c=500&pt=1&ft=json&pat=\n&rep=1&key=aa7acddc&ts=30'
        response = requests.get(url=proxy_url)
        if response.status_code != 200:
            return
        response = json.loads(response.text)
        if response['code'] == 200:
            proxy_list = []
            for ip in response['data']:
                proxy_list.append(f"{ip['ip']}:{ip['port']}")
            return proxy_list
    if type == 'smartdaili':
        proxy_list.append(f"us.smartproxy.com:10000")
        return proxy_list
    return proxy_list


def get_proxy_user(type='smartproxy'):
    if type == 'smartproxy':
        proxyHost = "proxy.smartproxycn.com"
        proxyPort = "1000"
        # 代理隧道验证信息（账号+密码）
        proxyUser = "mallus_area-US"
        proxyPass = "linemall888"
        return proxyHost, proxyPort, proxyUser, proxyPass


class Access:

    def __init__(self, url=None, proxy_type="smartproxy", proxy_way="ip"):
        if url is None:
            url = "https://www.btwearables.com"
            # url = "https://shop.snyder.cc"
        self.page_link = link_main(url)
        self.proxy_type = proxy_type
        self.proxy_way = proxy_way

    def web_access(self):
        global choice_list, diver
        chrome_options = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option('prefs', prefs)
        proxy_list = []
        if self.proxy_way == "ip":
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            # chrome_options.add_argument("--disable-extensions")
            while len(proxy_list) <= 0:
                proxy_list = get_proxy(type=self.proxy_type)
            if len(proxy_list) <= 0:
                print('没有获取到代理IP')
                return
        if len(self.page_link) <= 0:
            print('没有获取到该网站的页面地址')
            return
        for i in range(1000):
            i += 1
            if i % 50 == 0 and self.proxy_way == "ip":
                proxy_list = get_proxy(self.proxy_type)
            choice_proxy = random.choice(proxy_list)
            choice_list = choice_proxy.split(':')
            try:
                if self.proxy_way == "ip":
                    chrome_options.add_argument(f"--proxy-server=http://{choice_list[0]}:{choice_list[1]}")
                if self.proxy_way == "user":
                    proxy_obj = get_proxy_user(self.proxy_type)
                    chrome_options.add_extension(create_proxy_auth_extension(proxy_obj[0], proxy_obj[1], proxy_obj[2], proxy_obj[3], self.proxy_type))
                diver = webdriver.Chrome(options=chrome_options)
                diver.set_page_load_timeout(40)
                diver.set_page_load_timeout(40)
                diver.get(f'{random.choice(self.page_link)}')
                # diver.get('https://shop.snyder.cc')
                # print(diver.page_source)
                print(f'LOOP---->>>>Success>>>>>>{i}')
            except TimeoutException:
                print(f'LOOP---->>>>Error>>>>>>页面加载超时{i}')
            except Exception as e:
                print(f'LOOP---->>>>Error>>>>>>未知错误{e}')
            time.sleep(random.randint(5, 20))
            diver.quit()


def main(url, proxy_type, proxy_way):
    my_access = Access(url, proxy_type, proxy_way)
    my_access.web_access()


if __name__ == '__main__':
    # print(link_main("https://www.btwearables.com"))
    # fire.Fire({
    #     'main': main,
    # })
    with open(f"{os.path.abspath('..')}/config/url.json") as urls:
        uList = json.loads(urls.read())['urls']
    uList = ["https://shop.snyder.cc"]
    if len(uList) > 0:
        for item in uList:
            task = threading.Thread(target=main, args=(item, "smartproxy", "ip"))
            task.start()
    else:
        print('没有需要执行的任务')
