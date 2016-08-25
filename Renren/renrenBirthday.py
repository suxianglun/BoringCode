# -*- coding: utf-8 -*-

#
# 这是啥
#   人人好友生日爬虫
#

# 需要
#
# python2 
#    https://www.python.org/downloads/
# BeautifulSoup 
#    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
#

#
# 配置 使用
# rrb = rrBrower("useremail","password")
#    这里更换为你的 用户名 密码 即可
#

import urllib2
import urllib
import re
import thread
from bs4 import BeautifulSoup

from renrenBrower import *

rrb = rrBrower("useremail","password")


host="http://gift.renren.com/show/birth/monthly?month="
browerLock = thread.allocate_lock()
printLock = thread.allocate_lock()
    
def saveImage(filename,addr):
    with open(filename, 'wb') as f:
        f.write(urllib.urlopen(addr).read())

def getBirthByMonth(monthvalue):
    url = host+monthvalue
    browerLock.acquire()
    data = rrb.brower(url)
    browerLock.release()
    soup = BeautifulSoup(data,'lxml')#soup = BeautifulSoup(data)
    birthdayUL = soup.find("ul",class_="brith-wrap")
    birthdayLi = birthdayUL.find_all('li')
    for eachli in birthdayLi:
        imgurl = eachli.find(class_='user-box').find('img')['src']
        infop = eachli.find(class_='msg-b').find("p",recursive=False)
        namea = infop.find("a")
        birtha = re.findall(".(.*).",namea.find_next_sibling("a").get_text())[0];
        birthAndName = birtha + " "+namea.get_text();
        saveImage(birthAndName+".jpg",imgurl)
        printLock.acquire()
        #print imgurl
        print birthAndName
        printLock.release()

def getBirth():
    for i in range(1,13):
        thread.start_new_thread(getBirthByMonth,(str(i),))

if __name__ == '__main__':
    getBirth();
