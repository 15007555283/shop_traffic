#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Created by main_v4.py
# @Author: Snyder
# @Date: 2022/12/5
# @Time: 15:20
# @Email: snyder.xiang@gmail.com
import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from create_proxy_auth_extension import create_proxy_auth_extension


chrome_options = Options()
prefs = {'profile.managed_default_content_settings.images': 2, 'permissions.default.stylesheet': 2}
chrome_options.add_experimental_option('prefs', prefs)
# proxyHost = "proxy.smartproxycn.com"
# proxyPort = "1000"
# # 代理隧道验证信息（账号+密码）
# proxyUser = "mallus_area-US"
# proxyPass = "linemall888"
proxyHost = "na.ipidea.io"
proxyPort = "2333"
# 代理隧道验证信息（账号+密码）
proxyUser = "snyder_xiang-zone-custom-region-us"
proxyPass = "jubao5xihuan"

for i in range(10000):
    chrome_options.add_extension(create_proxy_auth_extension(proxyHost, proxyPort, proxyUser, proxyPass))
    diver = Chrome(options=chrome_options)
    diver.get('https://shop.snyder.cc/index.php?route=product/product&product_id=40')
    diver.quit()