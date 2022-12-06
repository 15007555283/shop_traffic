#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Created by main_v4.py
# @Author: Snyder
# @Date: 2022/12/5
# @Time: 15:20
# @Email: snyder.xiang@gmail.com
import json
import os
import random
import re
import ssl
import time
import urllib.request
from copy import copy

import requests
from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

def get_proxy():
    proxy_url = 'https://api.smartproxy.cn/web_v1/ip/get-ip?app_key=21824639440f11a4e83a6b1cd3ea79e8&pt=9&num=1000&cc=US&protocol=1&format=json&nr=%5Cr%5Cn'
    response = requests.get(url=proxy_url)
    if response.status_code != 200:
        return
    response = json.loads(response.text)
    if response['code'] == 200:
        proxy_list = response['data']['list']
        return proxy_list

class AccessMall:

    def __init__(self):
        self.config_path = f"{os.path.abspath('..')}/config"
        self.urlPath = f"{self.config_path}/url.json"
        self.invalidLink = ['#', 'None', 'javascript:void(0)']
        self.loop_max = 2
        self.loop_num = 0


    def get_page(self, url=None):
        if url is None:
            url = self.__url
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) "
                          "AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            'content-type': "application/json"
        }
        try:
            context = ssl._create_unverified_context()
            request = urllib.request.Request(url, None, headers, 'None')
            response = urllib.request.urlopen(request, context=context)
            content = response.read()
            return BeautifulSoup(content, "html.parser")
        except Exception as e:
            return None

    def is_image(self, url):
        """
        判断是否是一个图片的URL地址
        :param url:
        :return:
        """
        if url:
            img = re.compile('/png|jpg|jpeg|gif|bmp/')
            if len(img.findall(url)) > 0:
                return True
        return None

    def get_page_href(self, html_obj):
        all_href = html_obj.find_all('a')
        for h in all_href:
            h_url = h.get('href')
            if h_url not in self.invalidLink:
                if self.is_image(h_url):
                    continue
                if h_url is None or len(str(h_url)) < len(self.__url) or h_url[:len(self.__url)] != self.__url:
                    continue
                if h_url not in self.hrefList:
                    self.hrefList.append(h_url)
                if h_url not in self.activeList:
                    self.activeList.append(h_url)


    def get_all_href(self):
        while self.loop_num <= self.loop_max:
            if len(self.hrefList) <= 0:
                pageHtml = self.get_page(self.__url)
                if pageHtml:
                    self.get_page_href(pageHtml)
            hrefList = copy(self.hrefList)
            self.hrefList = []
            for href in hrefList:
                pageHtml = self.get_page(href)
                if pageHtml:
                    self.get_page_href(pageHtml)
            self.loop_num += 1
        print(f"总共获取到的链接地址数量：{len(self.activeList)}，{self.loop_num}")

    def web_access(self, url):
        self.__url = url
        activeUrls = f"{self.config_path}/{url}.json"
        listUrls = f"{self.config_path}/{url.replace('https://', '')}.json"
        if os.path.exists(listUrls) is False:
            self.get_all_href()
            with open(listUrls, 'w+') as file:
                tempData = {'urls': self.activeList}
                file.write(json.dumps(tempData))
                file.close()
        else:
            with open(listUrls) as oList:
                self.activeList = json.loads(oList.read())['urls']
                oList.close()

        proxy_list = get_proxy()
        chrome_options = Options()
        prefs = {'profile.managed_default_content_settings.images': 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option('prefs', prefs)
        diver = Chrome(options=chrome_options)
        chrome_options.add_experimental_option("detach", True)

        for i in range(10000):
            choice_proxy = random.choice(proxy_list)
            choice_list = choice_proxy.split(':')
            try:
                chrome_options.add_argument(f"--proxy-server=http://{choice_list[0]}:{choice_list[1]}")
                diver = Chrome(options=chrome_options)
                diver.set_page_load_timeout(10)
                diver.set_page_load_timeout(10)
                diver.get(f'{random.choice(self.activeList)}')
                # diver.get('https://shop.snyder.cc')
                # print(diver.page_source)
            except TimeoutException:
                print('页面加载超时')
            except Exception as e:
                print(e)
            diver.quit()


def main():
    AccessMall().web_access('https://www.btwearables.com')

if __name__ == '__main__':
    main()
