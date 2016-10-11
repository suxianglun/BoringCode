# -*- coding: utf-8 -*-
# Dependence:
#   pip3 install beautifulsoup4 

import urllib.request
import urllib.parse
#import chardet
import json
import threading
import time
import gzip
import re
import os

from booklist import bookName

from bs4 import BeautifulSoup

resultfile = "booksdata.json"

booksdata = []
booknum = 0
bookdataLock = threading.Lock()

reqErrBook = []

fightWithDoubanCrawlerBlockArr = []

def saveImage(filename,addr):
    pathprefix = "imgs/"
    with open(pathprefix + filename, 'wb') as f:
        f.write(urllib.request.urlopen(addr).read())

def getBookById(bookid):
    doubanAPIurl = "https://api.douban.com/v2/book/" + bookid
    rawdata = urllib.request.urlopen(doubanAPIurl).read();
    try:  
        getData = gzip.decompress(rawdata).decode('utf-8')
    except:
        getData = rawdata.decode('utf-8')
    jsondata = json.loads(getData)
    
    return [jsondata["image"],jsondata["title"],jsondata["author"][0],jsondata["isbn13"]]

def saveBookInfo(data):
    global booknum,booksdata,bookdataLock,resultfile
    ##save image
    threading.Thread(target=saveImage,args=(data[1]+".jpg",data[0],)).start()

    localimgprefix = "data/books/"
    bookdataLock.acquire() 
    booksdata.append({
        "title" : data[1],
        "author" : data[2],
        "ISBN": data[3],
        "cover" : localimgprefix + data[1] + ".jpg"
        })
    booknum = booknum - 1
    print("√-",data[1])
    f = open(resultfile,"w")
    json.dump(booksdata, f , ensure_ascii=False)
    f.close()
    if booknum == 0 :
        print("finish.",reqErrBook)
    bookdataLock.release() 


def getBookInfo(bname):
    global booknum
    try : 
        #visit https://book.douban.com/subject_search?search_text=
        browser_url = "https://book.douban.com/subject_search?search_text="+ urllib.parse.quote(bname)
        browser_headers = {
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch, br',
                    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Cookie':'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyooooooooooooooooooooouuuuuuuuuuuuuuuuuurrrrrrrrrrrrrrr cccccccccccccoooooooooookie here',
                    'Host':'book.douban.com',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
                    }

        #get fisrt url and get infoPageUrl
        req = urllib.request.Request(browser_url,headers = browser_headers) 
        searchRes = urllib.request.urlopen(req).read()
        try:  
            html = gzip.decompress(searchRes)
        except:
            html = searchRes
        soup = BeautifulSoup(html,'lxml')
        bookListUL = soup.find_all("ul",class_="subject-list")[0]
        bookListLi0 = bookListUL.find_all("li")[0]
        bookListLi0ahref = bookListLi0.find_all("a")[0]["href"]
        doubanID = re.findall(".*/(\d*)\/$",bookListLi0ahref)[0]

        ##############################  use api  ####################################

        getBookDataFromAPI = getBookById(doubanID)
        saveBookInfo(getBookDataFromAPI)
        
        #V_image = getBookDataFromAPI[0]
        ##V_title = jsondata["title"] 
        #V_title = bname 
        #V_author = getBookDataFromAPI[2]
        #V_ISBN = getBookDataFromAPI[3]
    
        #############################  Deprecated  START ##################################
        #visit resolve data and save
        #req = urllib.request.Request(bookListLi0ahref,headers = browser_headers) 
        #pageInfo = urllib.request.urlopen(req).read()
        #soup = BeautifulSoup(pageInfo,'lxml')
        #bookInfodiv = soup.find_all('div',class_="subjectwrap")[0]
        #bookInfodivsubject = bookInfodiv.find_all('div',class_="subject")[0]
        #V_image = bookInfodivsubject.find_all('img')[0]["src"]
        #infotxtarr = bookInfodivsubject.find_all("div",id='info')[0].get_text().split()
        
        #infodict = {}
        #for i in range(len(infotxtarr)//2):
        #    infodict[infotxtarr[i*2]] = infotxtarr[i*2+1]
        #    #print(infotxtarr[i*2],"=>",infotxtarr[i*2+1])
        #V_ISBN = infodict["ISBN:"]
        #V_author = infodict["作者:"]
        #V_title = bname
        #############################  Deprecated  END ##################################
        
        #saveBookInfo([V_image,V_title,V_author,V_ISBN])

    except Exception as err:
        bookdataLock.acquire() 
        print(bname,"===>",err)
        reqErrBook.append(bname)
        booknum = booknum - 1
        bookdataLock.release() 

def getBooksInfo(data):
    for eachBook in data:
        threading.Thread(target=getBookInfo,args=(eachBook,)).start()
        #getBookInfo(eachBook)
        time.sleep(1)

def fightWithDoubanCrawlerBlock():
    global resultfile,booknum,booksdata,rawBooklist
    fightWithDoubanCrawlerBlockArr = []
    if os.path.isfile(resultfile):
        f = open(resultfile,"r")
        booksdata = json.load(f)
        f.close()
    else:
        booksdata = []

    for bookrecord in booksdata:
        try:
            rawBooklist.remove(bookrecord["title"])
            booknum -= 1
        except:
            pass
    #print(booksdata)
    print(rawBooklist)

if __name__ == '__main__':
    global rawBooklist
    rawBooklist = []
    booknum = len(bookName)
    rawBooklist = bookName
    fightWithDoubanCrawlerBlock()
    getBooksInfo(rawBooklist)


