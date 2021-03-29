from bs4 import BeautifulSoup
import requests
import hashlib
import re
import urllib
import random
import ssl
import os
import time
import json
import requests
import socket
import time
from datetime import datetime



class snkrsUK:

    def __init__(self, db):
        self.timeout = 30
        socket.setdefaulttimeout(self.timeout)
        self.db = db
        self.cursor = self.db.cursor()
        # 模拟请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "nike-api-caller-id": "nike:snkrs:web:1.0",
            "origin": "https://www.nike.com",
            "referer": "https://www.nike.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }
        self.url1 = "https://api.nike.com/product_feed/threads/v2/?anchor=0&count=20&filter=marketplace%28GB%29&filter=language%28en-GB%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.subType%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title";
        self.url2 = "https://api.nike.com/product_feed/threads/v2/?anchor=9&count=20&filter=marketplace%28GB%29&filter=language%28en-GB%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.subType%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title";
        self.buildData_url1 = "https://api.nike.com/product_feed/threads/v2/?anchor=0&count=50&filter=marketplace%28GB%29&filter=language%28en-GB%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.subType%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title";
        self.buildData_url2 = "https://api.nike.com/product_feed/threads/v2/?anchor=9&count=50&filter=marketplace%28GB%29&filter=language%28en-GB%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.subType%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title";
        # self.url3 = "https://api.nike.com/snkrs/content/v1/?anchor=0&language=en-GB&marketplace=GB&includeContentThreads=true&format=v4&exclusiveAccess=true%2Cfalse"

        self.proxy_list = self.read_from_txt('ipPool.txt')

    def read_from_txt(self, path):
        '''
        (None) -> list of str
        Loads up all sites from the sitelist.txt file in the root directory.
        Returns the sites as a list
        '''
        # Initialize variables
        raw_lines = []
        lines = []

        # Load data from the txt file
        try:
            f = open(path, "r")
            raw_lines = f.readlines()
            f.close()

        # Raise an error if the file couldn't be found
        except:
            print('e', "Couldn't locate <" + path + ">.")

        if(len(raw_lines) == 0):
            pass
        # Parse the data
        for line in raw_lines:
            lines.append(line.strip("\n"))

        # Return the data
        return lines

    def get_proxy(self, proxy_list):
        '''
        (list) -> dict
        Given a proxy list <proxy_list>, a proxy is selected and returned.
        '''
        # Choose a random proxy
        proxy = random.choice(proxy_list)

        # Set up the proxy to be used
        proxies = {
            "http": str(proxy)
            #"https": str(proxy)
        }

        # Return the proxy
        return proxies

    def go(self, channel):
        self.db.ping(reconnect=True)
        self.db.rollback()
        self.db.commit()
        rtdic = []
        objects = []
        for url in [self.url1, self.url2]:
            try:
                # print('go')
                proxies = self.get_proxy(self.proxy_list)
                httpproxy_handler = urllib.request.ProxyHandler(proxies)
                opener = urllib.request.build_opener(httpproxy_handler)
                request = urllib.request.Request(url, headers=self.headers)
                response = opener.open(request).read().decode('utf-8')
                objects = json.loads(response)['objects']
                # print('success connect')
            except:
                print("fail connect " + str(proxies), flush=True)


            for obj in objects:
                name = ""
                price = ""
                method = ""
                styleColor = ""
                availableSkus = ""
                buy_time = None
                restricted = 0
                gmt_modified = None
                Pass = 0
                link = ""
                image = ""
                visibility_time = None
                dc = {}
                rs=()

                if 'productInfo' in obj:
                    for Info in obj['productInfo']:
                        try:
                            name = Info['productContent']['fullTitle'] + \
                                   Info['productContent']['colorDescription']
                        except:
                            # print("error_name: ", str(obj))
                            pass
                        try:
                            styleColor = Info['merchProduct']['styleColor']
                        except:
                            # print("error_name: ", str(obj))
                            pass
                        try:
                            price = str(Info['merchPrice']['currentPrice']) + Info['merchPrice']['currency']
                        except:
                            pass
                            # print("error_price: ", str(obj))
                        try:
                            image = Info['imageUrls']['productImageUrl']
                        except:
                            pass
                            # print("error_img: ", str(obj))
                        try:
                            entry_time = Info['launchView']['startEntryDate']
                            entry_time = entry_time.replace('T', ' ')
                            entry_time = entry_time.replace('.000Z', '')
                            # buy_time = time.strftime("%Y-%m-%d %H:%M:%S", entry_time)
                            buy_time = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S")
                        except:
                            pass
                            # print("error_buy_time: ", str(obj))
                        try:
                            visibility_time = Info['launchView']['delayConsumerVisibilityUntil']
                            visibility_time = visibility_time.replace('T', ' ')
                            visibility_time = visibility_time.replace('.000Z', '')
                            # buy_time = time.strftime("%Y-%m-%d %H:%M:%S", entry_time)
                            visibility_time = datetime.strptime(visibility_time, "%Y-%m-%d %H:%M:%S")
                        except:
                            pass
                            # print("error_visibility_time: ", str(obj))
                        try:
                            link = ""
                        except:
                            pass
                            # print("error_link: ", str(obj))
                        try:
                            method = Info['launchView']['method']
                        except:
                            pass
                            # print("error_method: ", str(obj))
                        try:
                            restricted = obj['publishedContent']['properties']['custom']['restricted']
                            if (restricted == False or restricted == 0):
                                restricted = 0
                            else:
                                restricted = 1
                        except:
                            pass
                            # print("error_restricted: ", str(obj))
                        try:
                            for NUM in range(len(Info['skus'])):
                                availableSkus = availableSkus + 'size: ' + Info['skus'][NUM]['nikeSize'] + '   ' 'level: ' + \
                                               Info['availableSkus'][NUM]['level'] + '\n'
                        except:
                            pass
                            # print("error_availbleSkus: ", str(obj))
                        Pass = 0

                        gmt_modified = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

                        if(styleColor!="" and buy_time!=None):
                            sql_findShoe = "select * from shoe_database where styleColor='%s' && buy_time='%s' && type='shoe';" %(self.db.escape_string(styleColor), buy_time)
                        elif(styleColor!="" and buy_time==None):
                            sql_findShoe = "select * from shoe_database where styleColor='%s' && type='shoe';" % (self.db.escape_string(styleColor))
                        self.cursor.execute(sql_findShoe)
                        rs = self.cursor.fetchall()
                        if not rs:
                            dc['name'] = name
                            dc['styleColor'] = "none" if styleColor=="" else styleColor
                            dc['buy_time'] = "none" if buy_time==None else buy_time
                            dc['image'] = "none" if image=="" else image
                            dc['availableSkus'] = "none" if availableSkus==None else availableSkus
                            dc['price'] = "none" if price=="" else price
                            dc['link'] = "none" if link=="" else link
                            dc['method'] = "none" if method=="" else method
                            dc['restricted'] = 'true' if restricted==1 else 'false'
                            dc['visibility_time'] = "none" if visibility_time==None or visibility_time=="" else visibility_time
                            dc['pass'] = 'true' if Pass==1 else 'false'
                            dc['type'] = 'shoe'
                            if (name != "" and buy_time != None):
                                if (visibility_time == None):
                                    sql = "INSERT INTO shoe_database(type, name, styleColor, price, method, availableSkus, buy_time, restricted, gmt_modified, pass, link, image) \
                                                           VALUES ('%s', '%s', '%s' ,'%s', '%s',  '%s',  '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                          (self.db.escape_string("shoe"), self.db.escape_string(name), self.db.escape_string(styleColor), self.db.escape_string(price),
                                           self.db.escape_string(method), self.db.escape_string(availableSkus), buy_time,
                                           restricted, gmt_modified, Pass, self.db.escape_string(link),
                                           self.db.escape_string(image))
                                else:
                                    sql = "INSERT INTO shoe_database(type, name, styleColor, price, method, availableSkus, buy_time, restricted, gmt_modified, pass, link, image, visibility_time) \
                                                                                   VALUES ('%s', '%s', '%s','%s', '%s',  '%s',  '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                          (self.db.escape_string("shoe"),self.db.escape_string(name), self.db.escape_string(styleColor), self.db.escape_string(price),
                                           self.db.escape_string(method),
                                           self.db.escape_string(availableSkus), buy_time, restricted, gmt_modified, Pass,
                                           self.db.escape_string(link), self.db.escape_string(image), visibility_time)
                                print(sql, flush=True)
                                self.db.ping(reconnect=True)
                                self.cursor.execute(sql)
                                # self.db.commit()
                            elif (name != "" and buy_time == None):
                                if (visibility_time == None):
                                    sql = "INSERT INTO shoe_database(type, name, styleColor,price, method, availableSkus, restricted, gmt_modified, pass, link, image) \
                                                                               VALUES ('%s', '%s', '%s','%s', '%s',  '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                          (self.db.escape_string("shoe"),self.db.escape_string(name), self.db.escape_string(styleColor), self.db.escape_string(price),
                                           self.db.escape_string(method),
                                           self.db.escape_string(availableSkus), restricted, gmt_modified, Pass,
                                           self.db.escape_string(link), self.db.escape_string(image))
                                else:
                                    sql = "INSERT INTO shoe_database(type, name, styleColor, price, method, availableSkus, restricted, gmt_modified, pass, link, image, visibility_time) \
                                                                                                       VALUES ('%s','%s', '%s', '%s',  '%s',  '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                          (self.db.escape_string("shoe"),self.db.escape_string(name), self.db.escape_string(styleColor), self.db.escape_string(price),
                                           self.db.escape_string(method),
                                           self.db.escape_string(availableSkus), restricted, gmt_modified, Pass,
                                           self.db.escape_string(link), self.db.escape_string(image), visibility_time)
                                print(sql, flush=True)
                                self.db.ping(reconnect=True)
                                self.cursor.execute(sql)
                                # self.db.commit()
                            rtdic.append(dc)
                elif 'publishedContent' in obj:
                    tags = ""
                    publishedContent = obj['publishedContent']
                    try:
                        name = publishedContent['properties']['seo']['title']
                    except:
                        pass
                    if name == "":
                        try:
                            name = publishedContent['properties']['title'] + publishedContent['properties']['subtitle']
                        except:
                            pass
                    try:
                        tags = publishedContent['properties']['custom']['tags'][0]
                    except:
                        pass
                    name = name + tags
                    try:
                        image = publishedContent['properties']['coverCard']['properties']['squarishURL']
                    except:
                        pass
                    gmt_modified = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                    if(name!=""):
                        sql_findShoe = "select * from shoe_database where name='%s' && type='card'" % (
                            self.db.escape_string(name))
                    self.cursor.execute(sql_findShoe)
                    rs = self.cursor.fetchall()
                    if not rs:
                        dc['name'] = name
                        dc['image'] = image
                        dc['type'] = 'card'
                        sql = "INSERT INTO shoe_database(type, name, image, gmt_modified) \
                                                             VALUES ('%s','%s', '%s', '%s')" % \
                              (self.db.escape_string("card"),self.db.escape_string(name), self.db.escape_string(image), gmt_modified)
                        print(sql, flush=True)
                        self.db.ping(reconnect=True)
                        self.cursor.execute(sql)
                        # self.db.commit()
                        rtdic.append(dc)
        return rtdic

    def buildData(self):
        self.db.ping(reconnect=True)
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()

        print("Database version : %s " % data)

        sql_update = "DELETE from shoe_database;"
        self.cursor.execute(sql_update)
        self.db.commit()
        for buildData_url in [self.buildData_url1, self.buildData_url2]:
            try:
                # print('go')
                proxies = self.get_proxy(self.proxy_list)
                httpproxy_handler = urllib.request.ProxyHandler(proxies)
                opener = urllib.request.build_opener(httpproxy_handler)
                request = urllib.request.Request(buildData_url, headers=self.headers)
                response = opener.open(request).read().decode('utf-8')
                objects = json.loads(response)['objects']
                # print('success connect')
            except:
                print("fail connect", flush=True)
            for obj in objects:
                name = ""
                price = ""
                method = ""
                availableSkus = ""
                buy_time = None
                restricted = 0
                gmt_modified = None
                Pass = 0
                styleColor=""
                link = ""
                image = ""
                visibility_time = None

                if 'productInfo' in obj:
                    for Info in obj['productInfo']:
                        try:
                            name = Info['productContent']['fullTitle'] + \
                                   Info['productContent']['colorDescription']
                        except:
                            # print("error_name: ", str(obj))
                            pass
                        try:
                            styleColor = Info['merchProduct']['styleColor']
                        except:
                            # print("error_name: ", str(obj))
                            pass
                        try:
                            price = str(Info['merchPrice']['currentPrice']) + Info['merchPrice']['currency']
                        except:
                            pass
                            # print("error_price: ", str(obj))
                        try:
                            image = Info['imageUrls']['productImageUrl']
                        except:
                            pass
                            # print("error_img: ", str(obj))
                        try:
                            entry_time = Info['launchView']['startEntryDate']
                            entry_time = entry_time.replace('T', ' ')
                            entry_time = entry_time.replace('.000Z', '')
                            # buy_time = time.strftime("%Y-%m-%d %H:%M:%S", entry_time)
                            buy_time = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S")
                        except:
                            pass
                            # print("error_buy_time: ", str(obj))
                        try:
                            visibility_time = Info['launchView']['delayConsumerVisibilityUntil']
                            visibility_time = visibility_time.replace('T', ' ')
                            visibility_time = visibility_time.replace('.000Z', '')
                            # buy_time = time.strftime("%Y-%m-%d %H:%M:%S", entry_time)
                            visibility_time = datetime.strptime(visibility_time, "%Y-%m-%d %H:%M:%S")
                        except:
                            pass
                            # print("error_visibility_time: ", str(obj))
                        try:
                            link = ""
                        except:
                            pass
                            # print("error_link: ", str(obj))
                        try:
                            method = Info['launchView']['method']
                        except:
                            pass
                            # print("error_method: ", str(obj))
                        try:
                            restricted = obj['publishedContent']['properties']['custom']['restricted']
                            if (restricted == False or restricted == 0):
                                restricted = 0
                            else:
                                restricted = 1
                        except:
                            pass
                            # print("error_restricted: ", str(obj))
                        try:
                            for NUM in range(len(Info['skus'])):
                                availableSkus = availableSkus + 'size: ' + Info['skus'][NUM]['nikeSize'] + '   ' 'level: ' + \
                                                Info['availableSkus'][NUM]['level'] + '\n'
                        except:
                            pass
                            # print("error_availbleSkus: ", str(obj))
                        Pass = 0

                        gmt_modified = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                        if (styleColor != "" and buy_time != None):
                            sql_findShoe = "select * from shoe_database where styleColor='%s' && buy_time='%s' && type='shoe';" % (
                            self.db.escape_string(styleColor), buy_time)
                        elif (styleColor != "" and buy_time == None):
                            sql_findShoe = "select * from shoe_database where styleColor='%s' && buy_time is NULL && type='shoe';" % (
                                self.db.escape_string(styleColor))
                        self.cursor.execute(sql_findShoe)
                        rs = self.cursor.fetchall()
                        if not rs:
                            if(name!="" and buy_time!=None):
                                if(visibility_time==None):
                                    sql = "INSERT INTO shoe_database(type, name,styleColor, price, method, availableSkus, buy_time, restricted, gmt_modified, pass, link, image) \
                                           VALUES ('%s', '%s', '%s','%s', '%s',  '%s',  '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                          (self.db.escape_string("shoe"),self.db.escape_string(name), self.db.escape_string(styleColor), self.db.escape_string(price), self.db.escape_string(method), self.db.escape_string(availableSkus), buy_time, restricted, gmt_modified, Pass, self.db.escape_string(link), self.db.escape_string(image))
                                else:
                                    sql = "INSERT INTO shoe_database(type, name,styleColor, price, method, availableSkus, buy_time, restricted, gmt_modified, pass, link, image, visibility_time) \
                                                                   VALUES ('%s', '%s','%s', '%s', '%s',  '%s',  '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                          (self.db.escape_string("shoe"), self.db.escape_string(name), self.db.escape_string(styleColor),self.db.escape_string(price), self.db.escape_string(method),
                                           self.db.escape_string(availableSkus), buy_time, restricted, gmt_modified, Pass,
                                           self.db.escape_string(link), self.db.escape_string(image), visibility_time)
                                # print(sql)
                                self.db.ping(reconnect=True)
                                self.cursor.execute(sql)
                                self.db.commit()
                            elif(name!="" and buy_time==None):
                                if (visibility_time == None):
                                    sql = "INSERT INTO shoe_database(type, name,styleColor, price, method, availableSkus, restricted, gmt_modified, pass, link, image) \
                                                               VALUES ('%s','%s', '%s','%s', '%s',  '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                          (self.db.escape_string("shoe"),self.db.escape_string(name), self.db.escape_string(styleColor),self.db.escape_string(price), self.db.escape_string(method),
                                           self.db.escape_string(availableSkus), restricted, gmt_modified, Pass,
                                           self.db.escape_string(link), self.db.escape_string(image))
                                else:
                                    sql = "INSERT INTO shoe_database(type, name,styleColor, price, method, availableSkus, restricted, gmt_modified, pass, link, image, visibility_time) \
                                                                                       VALUES ('%s', '%s','%s', '%s',  '%s',  '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                          (self.db.escape_string("shoe"),self.db.escape_string(name), self.db.escape_string(styleColor),self.db.escape_string(price), self.db.escape_string(method),
                                           self.db.escape_string(availableSkus), restricted, gmt_modified, Pass,
                                           self.db.escape_string(link), self.db.escape_string(image), visibility_time)

                                # print(sql)
                                self.db.ping(reconnect=True)
                                self.cursor.execute(sql)
                                self.db.commit()
                elif 'publishedContent' in obj:
                    tags=""
                    publishedContent = obj['publishedContent']
                    try:
                        name = publishedContent['properties']['seo']['title']
                    except:
                        pass
                    if name == "":
                        try:
                            name = publishedContent['properties']['title'] + publishedContent['properties']['subtitle']
                        except:
                            pass
                    try:
                        tags = publishedContent['properties']['custom']['tags'][0]
                    except:
                        pass
                    name = name + tags
                    try:
                        image = publishedContent['properties']['coverCard']['properties']['squarishURL']
                    except:
                        pass
                    gmt_modified = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                    if (name != ""):
                        sql_findShoe = "select * from shoe_database where name='%s' && type='card'" % (
                            self.db.escape_string(name))
                    self.cursor.execute(sql_findShoe)
                    rs = self.cursor.fetchall()
                    if not rs:
                        if(name!=""):
                            sql = "INSERT INTO shoe_database(type, name, image, gmt_modified) \
                                                                                                       VALUES ('%s','%s', '%s', '%s')" % \
                                  (self.db.escape_string("card"),self.db.escape_string(name), self.db.escape_string(image), gmt_modified)
                            # print(sql)
                            self.db.ping(reconnect=True)
                            self.cursor.execute(sql)
                            self.db.commit()
        # self.db.close()
