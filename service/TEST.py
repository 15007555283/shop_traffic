#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Created by TEST.py
# @Author: Snyder
# @Date: 2022/12/7
# @Time: 21:21
# @Email: snyder.xiang@gmail.com

import requests

url = 'http://ip.smartproxy.com/json'
username = 'mall'
password = 'mall.2022'

proxy = f'http://user-{username}:{password}@us.smartproxy.com:10000'

response = requests.get(url, proxies={'http': proxy, 'https': proxy})

print(response.text)