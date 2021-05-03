# encoding: utf-8
# !/usr/bin/env python


import configparser
import time
import os
from http import cookiejar
# import requests
import datetime
from requests_html import HTMLSession
import wechat
import pandas as pd
import numpy as np
import operator
import json
from time import sleep
import getpass


class Announcement:
    def __init__(self):
        self.URL = "https://www.binancezh.co/zh-CN"
        self.headers = {
            "Host": self.URL,
            "Referer": "http://" + self.URL + "/support/announcement",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

        self.wx = wechat.WeChat()
        self.wx.TOUSER = 'ZhouJian'
        self.df_links = {}
        self.huobi_links = {}
        self.okex_links = {}
        # self.df_links = equity_curve = pd.read_pickle('df_links.pkl')
        self.session = HTMLSession()
        # self.updateData()

    def updateBinancezh(self):
        links = {}#a[1]
        r = self.session.get(
            'https://www.binancezh.co/zh-CN/support/announcement')  # https://www.binancezh.co/zh-CN/support/announcement/xxxx
        for i in range(2, 7):
            txt = r.html.xpath('//*[@id="__APP"]/div/div/main/div/div[3]/div[1]/div['+str(i)+']/div[2]/div/a[1]')
            text = txt[0].text
            href = 'https://www.binancezh.co' + txt[0].attrs['href']
            links[href] = text

        if operator.ne(self.df_links.keys(), links.keys()):
            self.df_links = links.copy()

            return links
        return {}

    def updateHuobi(self):
        links = {}  # a[1]
        r = self.session.get('https://www.huobi.li/support/zh-cn/list/360000039942')
        txt = r.html.xpath('//*[@id="__layout"]/section/div/div[1]/div/div[3]/div[2]/dl/dd[1]/div[2]/a')
        text = txt[0].text
        href = 'https://www.binancezh.co' + txt[0].attrs['href']
        print(text)
        print(href)
        links[href] = text
        if operator.ne(self.huobi_links.keys(), links.keys()):
            self.huobi_links = links.copy()
            return links
        return {}

    def updateOkex(self):
        links = {}  # a[1]
        r = self.session.get('https://www.okex.win/support/hc/zh-cn/sections/115000447632-%E6%96%B0%E5%B8%81%E4%B8%8A%E7%BA%BF')
        txt = r.html.xpath('/html/body/main/div[1]/div[1]/section/ul/li[1]/a')
        text = txt[0].text
        href = 'https://www.binancezh.co' + txt[0].attrs['href']
        links[href] = text
        if operator.ne(self.okex_links.keys(), links.keys()):
            self.okex_links = links.copy()
            return links
        return {}
#

    def updateData(self):
        # links = self.updateBinancezh()
        # str = ''
        # for k in links.keys():
        #     v = links[k]
        #     str = str + k + '\n' + v + '\n\n'
        # if str != '':
        #     print(str)
        #     self.wx.send_data(str)
        #
        # hbLinks = self.updateHuobi()
        # for k in hbLinks.keys():
        #     v = hbLinks[k]
        #     self.wx.send_data(k + '\n' + v)

        okLinks = self.updateOkex()
        print(okLinks)
        for k in okLinks.keys():
            v = okLinks[k]
            k = 'https://www.okex.win/support/hc/zh-cn/sections/115000447632-%E6%96%B0%E5%B8%81%E4%B8%8A%E7%BA%BF'
            self.wx.send_data(k + '\n' + v)


if __name__ == '__main__':
    autoEngine = Announcement()
    # autoEngine.updateData()
    while True:
        autoEngine.updateData()
        sleep(60)
        print(datetime.datetime.now())
