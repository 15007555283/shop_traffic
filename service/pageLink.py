#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Created by main_v7.py
# @Author: Snyder
# @Date: 2022/12/7
# @Time: 09:44
# @Email: snyder.xiang@gmail.com
import fire
import json
import os
import random
import re
import ssl
import urllib.request

from bs4 import BeautifulSoup
from faker import Faker


class Browser:
    def __init__(self):
        pass

    def headerData(self):
        headers = {
            "User-Agent": Faker('en_US').user_agent(),
            'content-type': "application/json"
        }
        return headers

    def getPageData(self, url):
        context = ssl._create_unverified_context()
        request = urllib.request.Request(url, None, self.headerData(), 'None')
        response = urllib.request.urlopen(request, context=context)
        content = response.read()
        htmlObj = BeautifulSoup(content, "html.parser")
        return htmlObj

    def getHeader(self, pageData, url=None):
        print('开始获取分类链接')
        hrefUrl = []
        header = pageData.find(name=['header'])
        liObj = header.find_all(name='a')
        for li in liObj:
            href = li['href']
            if 'product/category' in href and href not in hrefUrl:
                if url not in href:
                    href = f"{url}/{href}"
                    print(f'简短Url>>>>>>>>>>>,拼接后{url}')
                hrefUrl.append(href)
        return hrefUrl

    def getPagination(self, pageData, url):
        """
        获取最大页面数
        :param url:
        :param pageData:
        :return:
        """
        print('开始获取分页链接', url)
        paginationList = []
        paginationNo = 1
        pagination = pageData.find(name='ul', attrs={"class": "pagination"})
        if not pagination:
            print('没有分页数据')
        else:
            paginationItem = pagination.find_all(name='li')
            for item in paginationItem:
                itemObj = item.find(name='a')
                if itemObj is None or itemObj == 'None':
                    continue
                itemNum = itemObj.text
                if itemNum.isdigit():
                    if paginationNo < int(itemNum):
                        paginationNo = int(itemNum)
        for row in range(paginationNo):
            if row + 1 <= 1:
                paginationList.append(url)
            else:
                paginationList.append(f"{url}&page={row + 1}")
        print(f"当前链接{url}；当前页面最大分页量：{paginationNo}")
        return paginationList

    def getGoods(self, pageData):
        """
        获取商品链接
        :param pageData:
        :return:
        """
        print('开始获取商品链接')
        goodsList = []
        goods = pageData.find(name='div', attrs={"class": "custom-category"})
        goodsItem = goods.find_all(name='a')
        for item in goodsItem:
            itemHref = item['href']
            if 'product/product' in itemHref:
                if itemHref not in goodsList:
                    goodsList.append(itemHref)
        print(f"总共获取到商品链接数量：{len(goodsList)}")
        return goodsList


def main(url, is_force=None):
    print(f"开始解析Url地址:{url}")
    config_path = f"{os.path.abspath('..')}/config"
    listUrls = f"{config_path}/{url.replace('https://', '')}.json"
    print(f'存放Urls的Json文件{listUrls}')
    pageList = []
    if os.path.exists(listUrls) is True and is_force is True:
        print('本次需要强制更新')
        os.remove(listUrls)
    if os.path.exists(listUrls) is False:
        print('Urls文件不存在，需要通过爬虫获取')
        my_browser = Browser()
        headerList = my_browser.getHeader(Browser().getPageData(url), url)
        pageList = pageList + headerList
        print(f"获取到的分类地址数量:{len(headerList)}")
        for item in headerList:
            paginationList = my_browser.getPagination(Browser().getPageData(item), item)
            pageList = pageList + paginationList
            for pagination in paginationList:
                goodsList = my_browser.getGoods(Browser().getPageData(pagination))
                pageList = pageList + goodsList
        print(f"当前url地址获取到的需要爬虫的Url数量为：{len(pageList)}，准备保存文件")
        with open(listUrls, 'w+') as obj:
            tempData = {'urls': pageList}
            obj.write(json.dumps(tempData))
            obj.close()
    else:
        print(f'当前url地址的urls文件已经存在，如果需要更新则需要删除该文件{config_path}')
        with open(listUrls, 'r') as obj:
            links = json.loads(obj.read())
            pageList = links['urls']
    return pageList


if __name__ == '__main__':
    fire.Fire({
        'main': main,
    })
    # print(main("https://www.btwearables.com"))
