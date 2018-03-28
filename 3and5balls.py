# -*- coding: utf-8 -*-  
import urllib2  
import re  
import requests  
import sys
from pymongo import MongoClient  
import urllib
#设置编码  
reload(sys)  
sys.setdefaultencoding('utf-8')  
#获得系统编码格式  

conn = MongoClient('172.16.1.22', 27017)
db = conn.mydb  #连接mydb数据库，没有则自动创建
ticket = db.ticket

def getPage(url):
    type = sys.getfilesystemencoding()  
    r = urllib.urlopen(url)  
    #将网页以utf-8格式解析然后转换为系统默认格式  
    a = r.read().decode('utf-8').encode(type)
    dealdata(a)  

def dealdata(a):
    res_tr = r'<td>(.*?)</td>(.*?)<td>(.*?)</td>(.*?)<td>(.*?)<ul class=\'ballbox middle\'>(.*?)</td>(.*?)<td>(.*?)</td>(.*?)<td>(.*?)</td>(.*?)<td>(.*?)</td>'
    m_tr =  re.findall(res_tr,a,re.S|re.M)   
    for _str in m_tr:
        res_tr1 = r'<li class=\'ball wred-24\'>(.*?)</li>'
        result = re.findall(res_tr1,_str[5],re.S|re.M)
        num = result[0]+result[1]+result[2]+result[3]+result[4]
        # print result
        res_tr2 = r'(.*?)注<i>'   
        reward = re.findall(res_tr2,_str[9],re.S|re.M)
        # print reward

        res_tr3 = r'(.*?)</td>(.*?)'   
        date = re.findall(res_tr3,_str[4],re.S|re.M)
        time = ""
        # print reward
        if len(date)>0:
            time = date[0][0]
        
        total = _str[7]
        if "元。" in total:
            total = total.strip('元。')
        ticket.insert({"No":_str[0],"data":_str[2],"total":total,"result":num,"reward":reward[0]})
        # if gain<0:
        #     print "期数:"+_str[2]+" 日期："+time+" 赔钱："+str(gain)
def getAlldataintoMongo():
    for i in range(2004,2019):
        pageuri = "http://kjh.55128.cn/p5-history-"+str(i)+".htm"
        getPage(pageuri)
def num5():
    allNum = [0 for x in range(0, 100000)]
    for ele in ticket.find():
        allNum[int(ele["result"])] = allNum[int(ele["result"])]+1

    results = [[] for x in range(0, 10)]

    for i, element in enumerate(allNum):
        results[element].append(i)


    with open('/home/bdyun/Desktop/data', 'w') as f:
        f.write(str(results))

    print "从未开出过的号码",len(results[0])
    print "开出过一次的号码",len(results[1]),results[1]
    print "开出过两次的号码",len(results[2]),results[2]
    print "开出过三次的号码",len(results[3]),results[3]
def num3():
    allNum = [0 for x in range(0, 1000)]
    for ele in ticket.find():
        number = 0 if len(ele["result"])<3 else int(ele["result"][0:-2])
        allNum[number] = allNum[number]+1
        # if "199" in str(number):
        #     print ele

    results = [[] for x in range(0, 13)]

    maxNum = 0 
    maxRes = 0

    for i, element in enumerate(allNum):
        results[element].append(i)
        if maxNum < element:
            maxNum = element 
            maxRes = i

    # for i in range(0,len(results)):
    #     print i,results[i]
    
    numcount = [[0 for i in range(0,10)] for x in range(0, 5)]


    for tickect in ticket.find():
        result = tickect["result"]
        if len(result) == 5:
            pass
        if len(result) == 4:
            result = "0"+result
        if len(result) == 3:
            result = "00"+result
        if len(result) == 2:
            result = "000"+result
        if len(result) == 1:
            result = "0000"+result
        if len(result) == 0:
            result = "00000"
        for k in range(0,5):
            numcount[k][int(result[k])] += 1
        
    print numcount

    for i in numcount:
        print i.index(max(i)),i.index(min(i))


    

    with open('/home/bdyun/Desktop/data', 'w') as f:
        f.write(str(results))

num3()