from getBookInfo import getBookById 
from getBookInfo import saveImage 
from getBookInfo import resultfile 


"""
a = [];
JSON.stringify(a.sort(function(v1,v2){
if(v1['author'].localeCompare(v2['author'])!=0)
return v1['author'].localeCompare(v2['author']);
else return v1['title'].localeCompare(v2['title'])
}));

"""

import threading
import sys
import os
import json
import time

bookdataLock = threading.Lock()

def appendBookInfo(data):
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
    print("√-",data[1])
    f = open(resultfile,"w")
    json.dump(booksdata, f , ensure_ascii=False)
    f.close()
    bookdataLock.release() 

def appendById(bookid):
    getBookDataFromAPI = getBookById(bookid)
    appendBookInfo(getBookDataFromAPI)
    
def init():
    global booksdata
    if os.path.isfile(resultfile):
        f = open(resultfile,"r")
        booksdata = json.load(f)
        f.close()
    else:
        booksdata = []

if __name__ == '__main__':
    toAppendlist = sys.argv[1:]
    init()
    for i in toAppendlist:
        threading.Thread(target=appendById,args=(i,)).start()
        time.sleep(1)


