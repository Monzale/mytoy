# encoding=utf-8
import matplotlib.pyplot as plt
from datetime import time
from pylab import *                                 #支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei'] 
import re  
import requests  
import sys
import urllib.request
import importlib
importlib.reload(sys)
import tkinter  
#建立一个对话框  
import tkinter.simpledialog as dl  
#建立一个信息展示框  
import tkinter.messagebox as mb 
from tkinter import *

def catchPoint(url):
    type = sys.getfilesystemencoding()  
    r = urllib.request.urlopen(url) 
    a = r.read().decode('utf-8')
    res_tr = r'<b class="full-court-one">(.*?)</b> <b class="vs">VS</b> <b class="full-court-tow">(.*?)</b>'
    m_tr =  re.findall(res_tr,a,re.S|re.M)
    return m_tr

x = [0]
originpoint = []
y = [0]
y1 = [0]
plt.grid(True)
plt.xlabel(u"time") #X轴标签
plt.ylabel(u"Point") #Y轴标签
plt.ion()
plt.margins(0)

def photos(a,b):
    x.append(x[-1]+1)
    y.append(a)
    y1.append(b)
    plt.plot(x, y,color='green')
    plt.plot(x, y1,color='red')
    plt.legend()  # 让图例生效 

def makeLive(url):
    originpoint = catchPoint(url) 
    y = [int(originpoint[0][0])]
    y1 = [int(originpoint[0][1])]
    lastpoint = [('0', '0')]
    while(1):
        point = catchPoint(url)
        time.sleep(2)
        if lastpoint != point:
            print(point)
            photos(int(point[0][0]),int(point[0][1]))
            plt.pause(1)
            lastpoint = point

def getGameList():
    ret = []
    url = "https://live.leisu.com/lanqiu"
    type = sys.getfilesystemencoding()   
    r = urllib.request.urlopen(url) 
    #将网页以utf-8格式解析然后转换为系统默认格式  
    a = r.read().decode('utf-8')
    res_tr = r'<a class="iconfont alt icon-live-animation on" href="(.*?)" target="_blank"="">'
    m_tr =  re.findall(res_tr,a,re.S|re.M)
	
    res_trLive = r'<a class="iconfont alt icon-liveanimation on" href="(.*?)" target="_blank"="">'
    m_trLive =  re.findall(res_trLive,a,re.S|re.M)
	
    for live in m_trLive:
        m_tr.append(live)
	
    neturl = "https://live.leisu.com"
    for item in m_tr:
        sonurl = "".join([neturl,item])
        gamelive = urllib.request.urlopen(sonurl) 
        b = gamelive.read().decode('utf-8')
        res_tr1 = r'<div class="tip"><span class="name">(.*?)</span> <span class="ranking">'
        m_tr1 =  re.findall(res_tr1,b,re.S|re.M)
        gametuple = (sonurl,m_tr1[0],m_tr1[1])
        ret.append(gametuple)
    print(ret)
    return ret

root = Tk()
listbox = Listbox(root)

gamelist = getGameList()
for item in gamelist:
	listbox.insert(END,"".join([item[1],"VS",item[2]]))
def getSelectGameURL(event):
    current = listbox.get(listbox.curselection())
    for i in gamelist:
        if "".join([i[1],"VS",i[2]]) == current:
            url = i[0]
    makeLive(url)
listbox.bind('<Double-Button-1>', getSelectGameURL)
	
listbox.pack()
root.mainloop()



