# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib

#
# demo 在 __main__ 中
#

class rrBrower:
    username = ""
    pwd = ""
    opener = None
    def __init__(self,u,p):  
        self.username = u  
        self.pwd = p
        self.login()
    def renrenLogin(self,u,p):
        loginPage = "http://www.renren.com/PLogin.do"
        try:
            cj = cookielib.CookieJar()
            opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
            data = urllib.urlencode({"email":u,"password":p})
            opener.open(loginPage,data)
            return opener
        except Exception,e:
            print str(e)
    def login(self):
        if(self.opener == None):
            self.opener = self.renrenLogin(self.username,self.pwd)
    def brower(self,url):
        op = self.opener.open(url)
        data= op.read()
        return data

if __name__ == '__main__':
    demo = rrBrower("username","password")
    print demo.brower("http://www.renren.com/home")