#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Created by main_v7.py
# @Author: Snyder
# @Date: 2022/12/7
# @Time: 09:44
# @Email: snyder.xiang@gmail.com
import json
import random
from selenium.webdriver import Chrome
import fire
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from service.pageLink import main as link_main
import requests


def get_proxy(type='smartproxy'):
    print('获取代理IP')
    proxy_list = []
    if type == 'smartproxy':
        proxy_url = 'https://api.smartproxy.cn/web_v1/ip/get-ip?app_key=21824639440f11a4e83a6b1cd3ea79e8&pt=9&num=1000&cc=US&protocol=1&format=json&nr=%5Cr%5Cn'
        response = requests.get(url=proxy_url)
        if response.status_code != 200:
            return
        response = json.loads(response.text)
        if response['code'] == 200:
            proxy_list = response['data']['list']
            return proxy_list
    if type == 'ipipgo':
        proxy_url = 'http://api.ipipgo.com/ip?cty=US&c=500&pt=1&ft=json&pat=\n&rep=1&key=aa7acddc&ts=3'
        response = requests.get(url=proxy_url)
        if response.status_code != 200:
            return
        response = json.loads(response.text)
        if response['code'] == 200:
            proxy_list = []
            for ip in response['data']:
                proxy_list.append(f"{ip['ip']}:{ip['port']}")
            return proxy_list
    return proxy_list


class Access:

    def __init__(self, url=None):
        if url is None:
            url = "https://www.btwearables.com"
        self.page_link = link_main(url)

    def web_access(self):
        chrome_options = Options()
        prefs = {'profile.managed_default_content_settings.images': 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option('prefs', prefs)
        # chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-extensions")
        proxy_list = get_proxy(type='ipipgo')
        if len(proxy_list) <= 0:
            print('没有获取到代理IP')
            return
        if len(self.page_link) <= 0:
            print('没有获取到该网站的页面地址')
            return
        for i in range(1000):
            i += 1
            if i % 100 == 0:
                proxy_list = get_proxy()
            choice_proxy = random.choice(proxy_list)
            choice_list = choice_proxy.split(':')
            try:
                chrome_options.add_argument(f"--proxy-server=http://{choice_list[0]}:{choice_list[1]}")
                diver = Chrome(options=chrome_options)
                diver.set_page_load_timeout(10)
                diver.set_page_load_timeout(10)
                diver.get(f'{random.choice(self.page_link)}')
                # diver.get('https://shop.snyder.cc')
                # print(diver.page_source)
            except TimeoutException:
                print('页面加载超时')
            except Exception as e:
                print(e)
            diver.quit()
            print(f'LOOP---->>>>{i}')


def main():
    my_access = Access()
    my_access.web_access()


if __name__ == '__main__':
    # print(link_main("https://www.btwearables.com"))
    # fire.Fire({
    #     'main': main,
    # })
    main()
