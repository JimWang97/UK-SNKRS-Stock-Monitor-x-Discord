import asyncio
import os
import sys
from datetime import datetime
import time
import discord
import pymysql
from snkrsUK import snkrsUK
from threading import Timer


class MyTimer(object):

    def __init__(self, start_time, interval, callback_proc, args=None, kwargs=None):
        self.__timer = None
        self.__start_time = start_time
        self.__interval = interval
        self.__callback_pro = callback_proc
        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}

    def exec_callback(self, args=None, kwargs=None):
        self.__callback_pro(*self.__args, **self.__kwargs)
        self.__timer = Timer(self.__interval, self.exec_callback)
        self.__timer.start()

    def start(self):
        interval = self.__interval - (datetime.now().timestamp() - self.__start_time.timestamp())
        self.__timer = Timer(interval, self.exec_callback)
        self.__timer.start()

    def cancel(self):
        self.__timer.cancel()
        self.__timer = None


def printRunning():
    print("running...:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), flush=True)


class discordBot(discord.Client):
    async def on_connect(self):
        # 下面两行初始化数据库用
        print("reconnect")

    async def on_ready(self):
        print('Logged on as', self.user)
        channel_uk = self.get_channel(784377996487426062)
        while 1:
            rtdic = monitor.go(channel_uk)
            for dc in rtdic:
                if dc:
                    embed = discord.Embed(title=dc['name'],color=0xeee657)
                    if dc['type']=='shoe':
                        embed.add_field(name="ReleaseDate: ", value=dc['buy_time'])
                        embed.add_field(name="StyleColor: ", value=dc['styleColor'])
                        embed.add_field(name="Method: ", value=dc['method'])
                        embed.add_field(name="Price: ", value=dc['price'])
                        embed.add_field(name="Restricted: ", value=dc['restricted'])
                        embed.add_field(name="Pass: ", value=dc['pass'])
                        embed.add_field(name="VisibilityTime: ", value=str(dc['visibility_time']))
                        embed.add_field(name="Link: ", value=dc['link'])
                        embed.add_field(name="AvailableSize: ", value=dc['availableSkus'], inline=False)
                    if(dc['image']!="none"):
                        embed.set_image(url=dc['image'])
                    print(str(embed.to_dict()))
                    await channel_uk.send(embed=embed)
            if(len(rtdic)>0):
                db.commit()
                time.sleep(3)
            time.sleep(2)


MYSQL_CONFIG = {
        'host': 'xxx.xxx.xxx.xxx',  # IP地址
        'port': 3306,  # 端口
        'user': 'root',  # 用户名
        'passwd': 'xxxx',  # 密码
        'db': 'snkrsuk',  # 数据库
        'charset': 'utf8',  # 编码，
        'autocommit': True
}
db = pymysql.connect(**MYSQL_CONFIG)
monitor = snkrsUK(db)
monitor.buildData()
print("finish build data", flush=True)
# 定时输出
tmr = MyTimer(datetime.now(), 60 * 60, printRunning)
tmr.start()
bot = discordBot()
bot.run('Nzg0MzgzMjI4MTIzNDE0NTY4.X8ofzg.xxxxxxxxxxxxxxx')