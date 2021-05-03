# encoding: utf-8
# !/usr/bin/env python


import configparser
import time
import os
from http import cookiejar
import requests
import datetime

import wechat2
import json
from time import sleep
import getpass

class LeagueEngine:
    def __init__(self):
        self.USERID = 'zt007'
        self.PASSWORD = 'wsx123'
        self.URL = "47.111.231.208:8200"
        self._path = 'tmp/config.ini'
        self.headers = {
            "Host": self.URL,
            "Referer": "http://" + self.URL + "/bet/login",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        self.token = ''
        self._get_access_token()

        self.itemPath = 'C:/Users/' + getpass.getuser() + '/Documents/GitHub/zuqiu/tmp/item_config.ini'
        self.itemConfig = configparser.ConfigParser()
        self.itemConfig.read(self.itemPath)

    def getItemName(self, name):
        h = self.itemConfig['name'].get(name)
        if not h:
            # print('未找到对应的xjw队名')
            return name  #None
        else:
            return h

    def _get_access_token(self):
        self.session = requests.session()
        self.session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            pass  # print("还没有cookie信息")
        self.login()
        # self.cf = configparser.ConfigParser()  # configparser类来读取config文件

    def login(self):
        login_url = 'http://' + self.URL + '/api_v1/coolstorm/login'
        data = {
            'username': self.USERID,
            'password': self.PASSWORD
        }
        response = self.session.post(login_url, data=data, headers=self.headers)
        login_code = response.json()
        self.token = str(login_code['code'])

    def find_betid(self, betid, data):
        for item in data['bets']:
            if item['id'] == betid:
                return item

    # 'sort_by:percent
    def request_data(self, sort_by='percent'):
        url = 'http://' + self.URL + '/bet/api/v1/arbs/pro_search?access_token=' + self.token + '&locale=cn'
        data = {
            'sort_by': sort_by,
            'koef_format': 'decimal',
        }
        r = self.session.post(url, data=data, headers=self.headers)
        r_data = json.loads(r.text)
        # r_data = r.json()
        rets = self.update_data(r_data)
        return rets

    def request_data2(self):
        while True:
            ret = self.request_data()
            if len(ret) == 0:
                sleep(30)
                continue
            return ret

    # 得到球队名称
    def get_bet_name(self, arb):
        if arb['bet1_id'] == arb['hgw']['id']:
            arb['hgw']['bet_name'] = arb['hgw']['home']
            arb['xjw']['bet_name'] = self.getItemName(arb['hgw']['away'])
        else:
            arb['hgw']['bet_name'] = arb['hgw']['away']
            arb['xjw']['bet_name'] = self.getItemName(arb['hgw']['home'])
        return arb


    # 更新数据 剔除系数>1的球队和让球大小以外的盘口，连接arb,brb数据
    def update_data(self, data, xjw_v=5000):
        ret = []
        if data == []:
            return data
        for arb in data['arbs']:
            arb['bet1_v'] = self.find_betid(arb['bet1_id'], data)
            arb['bet2_v'] = self.find_betid(arb['bet2_id'], data)
            arb = self.update_val(arb, xjw_v)
            if arb['sort'] < 1:
                if arb['arb_type'] in ('7:2', '7:3'):
                    tv1 = arb['hgw']['market_and_bet_type']
                    tv2 = arb['xjw']['market_and_bet_type']
                    b1 = tv1 in (17, 18, 19, 20)
                    b2 = tv2 in (17, 18, 19, 20)
                    if b1 and b2:
                        arb['hgw']['bet_type_name'] = self.getConfig('market_and_bet_type', tv1)
                        arb['xjw']['bet_type_name'] = self.getConfig('market_and_bet_type', tv2)
                        arb = self.get_bet_name(arb)

                        hname = self.getItemName(arb['hgw']['home'])
                        aname = self.getItemName(arb['hgw']['away'])
                        if not hname or not aname:  # item_config.ini有名字 才返回数据
                            continue
                        arb['xjw']['home'] = hname
                        arb['xjw']['away'] = aname
                        arb['hgw']['started_at'] = self.updateTime(arb['hgw']['started_at'] )

                        ret.append(arb)
            else:
                break
        ret.sort(key=self.take_started, reverse=True)
        return ret

    def take_started(self, e):
        return e['started_at']

    def koef_isok(self, k1, k2):
        v = (1.0 / float(k1)) + (1.0 / float(k2))
        print(v)
        return v <= 2

    def get_value(self,k1,k2,v2):
        k1 = float(k1)
        k2 = float(k2)
        v = (1 / k1) / (1 / k2) * v2
        return v

    def update_val(self, arb, xjw_v):
        koef_1 = arb['bet1_v']['koef']
        koef_2 = arb['bet2_v']['koef']
        if arb['bet1_v']['bookmaker_id'] == 12:
            hgw_v = (1 / koef_2) / (1 / koef_1) * xjw_v
            arb['hgw'] = arb['bet2_v']
            arb['hgw']['val'] = hgw_v
            arb['xjw'] = arb['bet1_v']
            arb['xjw']['val'] = xjw_v
        else:
            hgw_v = (1 / koef_1) / (1 / koef_2) * xjw_v
            arb['hgw'] = arb['bet1_v']
            arb['hgw']['val'] = hgw_v
            arb['xjw'] = arb['bet2_v']
            arb['xjw']['val'] = xjw_v
        # 越小越挣钱，可以按这个排序
        sort = (1 / koef_1) + (1 / koef_2)
        arb['sort'] = sort
        av = arb['hgw']['val'] * (arb['hgw']['koef'])
        bv = arb['xjw']['val'] * (arb['xjw']['koef'])
        yl_a = av - arb['hgw']['val'] * 2
        yl_b = bv - arb['xjw']['val'] * 2
        yl = yl_a + yl_b
        profit_margin = yl / (arb['hgw']['val'] + arb['xjw']['val'])
        arb['profit'] = profit_margin
        return arb

    def getConfig(self, t, k):
        return k
        # k = str(k)
        # base_dir = str(os.path.dirname(os.path.dirname(__file__)))
        # base_dir = base_dir.replace('\\', '/')
        # file_path = base_dir + "./tmp/names.ini"
        # self.cf.read(file_path)
        # RYST = self.cf.get(t, k)
        # return RYST

    def findOne(self, ret):
        r = ret[0]
        v = ['', '', '', '', '', '', '', '']
        v[0] = 1
        start_time = time.localtime(r['xjw']['started_at'])
        v[1] = time.strftime('%Y年%m月%d日 %H:%M', start_time)
        v[2] = r['team1_name']
        v[3] = r['team2_name']
        v[4] = r['xjw']['bet_type_name']
        v[5] = str(r['xjw']['market_and_bet_type_param'])
        v[6] = str(r['xjw']['val'])
        v[7] = str(r['profit']) + ' ' + r['name'] + str(r['sort']) + '|' + str(r['country_id']) + r['league']
        return '\n'.join(str(x) for x in v)

    def filter_update(self, x):
        now = datetime.datetime.now()

        update = x['updated_at']
        update = datetime.datetime.fromtimestamp(update)
        miao = (now - update).seconds

        update = x['hgw']['updated_at']
        update = datetime.datetime.fromtimestamp(update)
        hgw_m = (now - update).seconds / 60

        update = x['xjw']['updated_at']
        update = datetime.datetime.fromtimestamp(update)
        xjw_m = (now - update).seconds / 60
        return miao < 20  # 收留更新时间5分钟内的

    # 最全显示的数据
    def get_manual_data(self):
        ret = self.request_data()
        ff = filter(self.filter_update, ret)
        ret = list(ff)
        print(len(ret))
        if len(ret) == 0: return []
        ary = []
        for r in ret:
            x = ['']
            # print(r)

            recorded_at = time.localtime(r['created_at'])
            recorded_at = time.strftime('%d日 %H:%M', recorded_at)
            x.append('创建时间' + recorded_at)

            updated_at = time.localtime(r['updated_at'])
            updated_at = time.strftime('%d日 %H:%M', updated_at)
            x.append('更新时间' + updated_at)

            # koef_last_modified_at = time.localtime(r['hgw']['koef_last_modified_at'])
            # koef_last_modified_at = time.strftime('%m月%d日 %H:%M',koef_last_modified_at)
            # x.append('koef_last_m_hgw'+koef_last_modified_at)

            updated_at = time.localtime(r['hgw']['updated_at'])
            updated_at = time.strftime('%d日 %H:%M', updated_at)
            x.append('hgw更新' + updated_at)
            # recorded_at = time.localtime(r['hgw']['recorded_at'])
            # recorded_at = time.strftime('%d日 %H:%M',recorded_at)
            # x.append('hgw_入账时间'+recorded_at)

            # koef_last_modified_at = time.localtime(r['xjw']['koef_last_modified_at'])
            # koef_last_modified_at = time.strftime('%m月%d日 %H:%M',koef_last_modified_at)
            # x.append('koef_last_m_xjw:'+koef_last_modified_at)

            updated_at = time.localtime(r['xjw']['updated_at'])
            updated_at = time.strftime('%d日 %H:%M', updated_at)
            x.append('xjw更新' + updated_at)
            # recorded_at = time.localtime(r['xjw']['recorded_at'])
            # recorded_at = time.strftime('%d日 %H:%M',recorded_at)
            # x.append('xjw_入账时间'+recorded_at)

            stime = time.localtime(r['hgw']['started_at'])
            stime = time.strftime('%d日 %H:%M', stime)
            x.append('开踢时间' + stime)
            # x.append('rate:' + str(r['profit']*1000)[:4] + '‰')
            x.append('\n')
            x.append(r['hgw']['bookmaker_league_name'])  # 意大利甲组联赛
            x.append(r['hgw']['bookmaker_event_name'])  # 斯佩齐亚-AC米兰
            # xishu = (1/r['hgw']['koef']) / (1/r['xjw']['koef']) #比例系数乘xlw_val，188成本
            # xishu = str(format(xishu,'.4f'))
            x.append('\nhgw:')
            pank = r['hgw']['bet_type_name']
            pankv = r['hgw']['market_and_bet_type_param']
            pankv = ' ' + str(pankv)
            x.append(r['hgw']['bet_name'] + pank + pankv)
            x.append(str(r['hgw']['koef']))
            x.append(str(r['hgw']['val']))
            x.append('\nxjw:')
            pank = r['xjw']['bet_type_name']
            pankv = r['xjw']['market_and_bet_type_param']
            pankv = ' ' + str(pankv)
            x.append(r['xjw']['bet_name'] + pank + pankv)
            x.append(str(r['xjw']['koef']))
            x.append(str(r['xjw']['val']))
            v = '\n'.join(str(xx) for xx in x)
            ary.append(v)
            # -------------------------
        return '\n\n———————————'.join(str(xx) for xx in ary)

    def test_data(self):
        while True:
            ret = self.request_data()
            if len(ret) == 0:
                sleep(3)
                continue
            return ret[0]

    def updateTime(self, t):
        interval = datetime.timedelta(hours=-12)
        d = datetime.datetime.fromtimestamp(t)
        d = d + interval
        return d.timestamp()

    def saveData(self):

        def time_format(t):
            interval = datetime.timedelta(hours=-12)
            d = datetime.datetime.fromtimestamp(t)
            # r = d.strftime('%Y-%m-%d %H:%M:%S')
            r = d.strftime('%H:%M')
            return r

        config = configparser.ConfigParser()
        config.read(self._path)


        sort_by='percent'
        url = 'http://' + self.URL + '/bet/api/v1/arbs/pro_search?access_token=' + self.token + '&locale=cn'
        data = {
            'sort_by': sort_by,
            'koef_format': 'decimal',
        }
        r = self.session.post(url, data=data, headers=self.headers)
        r_data = json.loads(r.text)
        print(r_data)
        bets = r_data['bets']
        for d in bets:
            if d['bookmaker_id'] == 5:  # hgw
                time = time_format(d['started_at'])
                if time not in config:
                    config.add_section(time)
                v = 'hgw' + d['bookmaker_event_name']
                if v not in config[time]:
                    config.set(time, v, '2')
            config.write(open(self._path, 'w'))



if __name__ == '__main__':
    wx = wechat2.WeChat()
    wx.TOUSER = 'ZhouJian'
    le = LeagueEngine()
    le.saveData()