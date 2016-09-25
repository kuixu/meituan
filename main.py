#!/usr/local/bin/python
__author__ = 'Kui Xu'
# -*- coding:utf-8 -*-
 
import urllib
import urllib2
import re
import json
#import HTMLParser  
from sgmllib import SGMLParser  


#class MyParser(HTMLParser.HTMLParser):  
class MyParser(SGMLParser):  
    def __init__(self): 
        SGMLParser.__init__(self)
        self.siteURL = 'http://sz.meituan.com/deal/feedbacklist/0/7336/all/0/default/30'
        self.is_p=""
        self.is_span=""
        #self.name = []
        self.data = []
        self.pagesize=10
        self.cur = 0

    def handle_data(self, data):
      data=data.replace('\r\n','').replace(' ','').strip('\n').strip().strip('\n')
      if self.is_span == 1:       
            self.data[self.cur][0]=data.decode('unicode-escape').encode('utf8')
      if self.is_p == 1 and len(data) > 50:       
            self.data[self.cur][1]=data
            if self.data[self.cur][0] == "":
               self.data[self.cur][0] = "--"
            if self.data[self.cur][2] == "":
               self.data[self.cur][2] = "0"
    
    def start_li(self, attrs): 
        for k, v in attrs: 
            if k=='class' and v == 'J-ratelist-item rate-list__item cf':
               self.is_li=1
    
    def end_li(self): 
        if self.is_li == 1:
          self.cur = self.cur + 1
          self.is_li=""

    def start_p(self, attrs): 
        for k, v in attrs: 
            if k=='class' and v == 'content':
               self.is_p=1
    
    def end_p(self): 
        self.is_p=""

    def start_span(self, attrs): 
        for k, v in attrs: 
            if k=='class' and v.startswith('name'):
               self.is_span=1
            if k=='style' and v.startswith('width:'):
               score=v[6:len(v)-1]
               self.data[self.cur][3]=score
    
    def end_span(self): 
        self.is_span=""

    def start_ul(self, attrs): 
        for k, v in attrs: 
            if k=='class' and v == 'pic-thumbnail-list':
              self.data[self.cur][2]=1
  
    def printCom(self,i):
        print str(i)+"\t"+spider.data[i][0]+"\t\""+spider.data[i][1].decode('unicode-escape').encode('utf8').replace("\n","")+"\"\t"+str(spider.data[i][2])+"\t"+str(spider.data[i][3])

    def getPage(self,offset):
#        offset=pageIndex*self.pagesize;
        url = self.siteURL + "?showpoititle=0&offset=" + str(offset)+"&limit="+str(self.pagesize);
#        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = response.read().decode('utf-8')
        jsonObj = json.loads(data)
        return jsonObj
 
    def getContents(self,pageIndex):
        jsondata = self.getPage(pageIndex)
        #page= jsondata['data']['ratelistHtml']
        page= jsondata['data']
        if len(self.data) == 0:
            self.total = int(jsondata['data']['total'])
#            print "len of data:"+str(len(self.data))
            self.data =[[""]*4 for i in range(self.total)] 
#            print "len of data:"+str(len(self.data))
        return page
        #print html
        #pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        #items = re.findall(pattern,page)
        #for item in items:
        #    print item[0],item[1],item[2],item[3],item[4]
 
spider = MyParser()
a=spider.getContents(0)
spider.feed(str(a))
for j in range(10,30,10):
    a=spider.getContents(j)
    spider.feed(str(a))

for i in range(30):
    spider.printCom(i)
#i=0

#for item in spider.name:
#    i=i+1
#    print str(i) +"===="+item.decode('unicode-escape').encode('utf8').strip('\n').strip().strip('\n')


