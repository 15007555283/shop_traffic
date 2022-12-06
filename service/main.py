#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Created by main.py
# @Author: Snyder
# @Date: 2022/11/30
# @Time: 16:01
# @Email: snyder.xiang@gmail.com
import json
import os
import ssl
from copy import copy
import re
import random
from faker import Faker

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import urllib.request
import sys
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from create_proxy_auth_extension import create_proxy_auth_extension


class getSiteList:

    def __init__(self):
        self.__url = None
        self.invalidLink = ['#', 'None', 'javascript:void(0)']
        self.siteList = []
        self.hrefList = []
        self.activeList = []
        self.loop_max = 2
        self.loop_num = 0
        self.response_page = None
        self.html_parser = []
        self.config_path = f"{os.path.abspath('..')}/config"
        self.urlPath = f"{self.config_path}/url.json"
        self.proxy_list = []
        self.fake = Faker()

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

    def get_proxy(self):
        proxy_url = 'https://api.smartproxy.cn/web_v1/ip/get-ip?app_key=21824639440f11a4e83a6b1cd3ea79e8&pt=9&num=100&cc=US&protocol=1&format=json&nr=%5Cr%5Cn'
        response = requests.get(url=proxy_url)
        if response.status_code != 200:
            return
        response = json.loads(response.text)
        if response['code'] == 200:
            self.proxy_list = response['data']['list']

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
        # 禁止加载图片
        chrome_options = webdriver.ChromeOptions()
        # prefs = {'profile.managed_default_content_settings': {'images': 2, 'javascript': 2}, 'permissions.default.stylesheet': 2}
        prefs = {'profile.managed_default_content_settings.images': 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option('prefs', prefs)
        # 关闭图形界面，提高效率
        # chrome_options.add_argument('--headless')
        for i in range(20):
            num = 0
            for item in self.activeList:
                num += 1
                if len(self.proxy_list) <= 10:
                    self.get_proxy()
                if num == 1:
                    proxyHost = "proxy.smartproxycn.com"
                    proxyPort = "1000"
                    # 代理隧道验证信息（账号+密码）
                    proxyUser = "mallus_area-US"
                    proxyPass = "linemall888"
                    chrome_options.add_extension(create_proxy_auth_extension(proxyHost, proxyPort, proxyUser, proxyPass))
                try:
                    wd = Chrome(options=chrome_options)
                    if num == 1:
                        wd.get(item)
                    else:
                        js = "window.open('{}','_blank');"
                        wd.execute_script(js.format(item))
                    if num == 10:
                        wd.quit()
                        num = 0
                    # self.request_data(item)
                except Exception as e:
                    print(e)

    def request_data(self, url):
        if len(self.proxy_list) <= 10:
            self.get_proxy()
        try:
            headerData = {"User-Agent": Faker('en_US').user_agent()}
            proxy_num = random.randint(0, len(self.proxy_list))
            proxy_obj = self.proxy_list[proxy_num - 1]
            del self.proxy_list[proxy_num]
            proxyMeta = f"http://{proxy_obj['ip']}:{proxy_obj['port']}"
            proxies = {"http": proxyMeta, "https": proxyMeta}
            res = requests.get(url, headers=headerData, proxies=proxies, timeout=10)
            print(res.status_code)
        except Exception as e:
            print(e)

    def access_main(self):
        global urlObj
        with open(self.urlPath) as urls:
            urlObj = json.loads(urls.read())
            urls.close()
        for url in urlObj['urls']:
            self.web_access(url)


my_site = getSiteList()
aList = my_site.access_main()
# aList = my_site.web_access()
# aList = my_site.is_image('https://shop.snyder.cc/image/cache/catalog/demo/banners/MacBookAir-1140x380.jpg')
