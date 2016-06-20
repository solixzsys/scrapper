# -*- coding: utf-8 -*-
import os,sys
from bs4 import  BeautifulSoup as bs
import re,hashlib
import requests
from sys import stdout

class YahooNewsScrapper:
    SITE_URL='http://www.yahoo.com'
    POST_URL=''
    POST_HEADING=''
    POST_SUMMARY=''
    POST_IMG_SRC=''
    POSTS={}
    key=0
    soup=''
    def __init__(self,file=None):
        
        print('file: ',file)
        if file == None:
            try:
                html=requests.get(self.SITE_URL)
                print('Request Response: ',html)
                self.soup = bs(html.content)


            except Exception as e:
                print("Error from Requests Module\n")
                print(e,'\n')
                input('ENTER to exit')
                sys.exit()
        else:
            try:
                with open(file,'r',encoding='utf-8') as fp:
                    file_content=fp.read()
                    self.soup=bs(file_content)
            except Exception as e :
                print("Error from Reading File\n")
                print(e,'\n')
                input('ENTER to exit')    
        
        level1_postlist=self.soup.find_all(class_='js-stream-content')
        level2_postlist=[]
        if len(level1_postlist) != 0:
            for post in level1_postlist:
                if 'js-stream-cluster' not in post.attrs.get('class'):
                    level2_postlist.append(post)
        else:
            print('Passing Error.......................')
            Input('Enter to EXIT ............')
            sys.exit()
       
        if len(level2_postlist) != 0:
            for post in level2_postlist:

                strm_left=post.find('div',attrs={'class','strm-left'})
                strm_right=post.find('div',attrs={'class','strm-right'})
                
                if (strm_left is not None):
                    #print(strm_left)
                    self.POST_URL=strm_left.findChild('a').attrs.get('href')
                    self.POST_IMG_SRC=strm_left.findChild('img').attrs.get('src')
                    if self.POST_IMG_SRC.find('http')<0:
                        self.POST_IMG_SRC=self.SITE_URL+self.POST_IMG_SRC.strip('.')
                    

                
                    self.POST_HEADING=strm_right.findChild('span').text
                    print('*********: ',str(self.POST_HEADING))
                    self.POST_SUMMARY=strm_right.findChild('p').text
                    self.POSTS[self.key]={'heading':self.POST_HEADING,'link':self.POST_URL,'img':self.POST_IMG_SRC,'summary':self.POST_SUMMARY}
                self.key=self.key+1
                #print(self.key)=
    def get_Post(self):
        return self.POSTS

class UPIScrapper:
    SITE_URL='http://www.UPI.com'
    POST_URL=''
    POST_HEADING=''
    POST_SUMMARY=''
    POST_IMG_SRC=''
    POSTS={}
    key=0
    def __init__(self,file=None):
        soup=None
        print('file: ',file)
        if file == None:
            try:
                html=requests.get(self.SITE_URL)
                soup=bs(html.content)


            except Exception as e:
                print("Error from Requests Module\n")
                print(e,'\n')
                input('ENTER to exit')
                sys.exit()
        else:
            try:
                with open(file,'r',encoding='utf-8') as fp:
                    file_content=fp.read()
                    soup=bs(file_content)
            except Exception as e :
                print("Error from Reading File\n")
                print(e,'\n')
                input('ENTER to exit')
        
        level1_postlist=soup.find('div',attrs={'class','stories'})  
        level2_postlist=level1_postlist.find_all('div',attrs={'class','upi_item'})     
        if len(level2_postlist)>0:
            for post in level2_postlist:
                self.POST_URL=post.findChild('a').attrs.get('href')
                self.POST_IMG_SRC=post.findChild('img').attrs.get('src')
                self.POST_HEADING=post.findChild('span').text

                try:
                    html=requests.get(self.POST_URL)
                    soup2=bs(html.content)

                except Exception as e:
                    print("Error from Requests Module\n")
                    print(e,'\n')
                    #input('ENTER to exit')
                    #sys.exit()
                    pass
                #level3_postlist=soup2.find('div',attrs={'id','c_story'}) 
                level3_postlist=soup2.find('div',attrs={'id':'c_story'}) 
                paralist=level3_postlist.findChildren('p')
                if len(paralist)>0:
                    self.POST_SUMMARY=paralist[0].text +'\n'+paralist[1].text

                self.POSTS[self.key]={'heading':self.POST_HEADING,'link':self.POST_URL,'img':self.POST_IMG_SRC,'summary':self.POST_SUMMARY}
                self.key=self.key+1
                print(self.key)
    def get_Post(self):
        return self.POSTS                           

class YahooRssScrapper:
    SITE_URL='http://news.yahoo.com/rss/'
    POST_URL=''
    POST_HEADING=''
    POST_SUMMARY=''
    POST_IMG_SRC=''
    POSTS={}
    key=0
    soup=''
    def __init__(self,file=None):
        
        print('file: ',file)
        if file == None:
            try:
                html=requests.get(self.SITE_URL)
                print('Request Response: ',html)
                temp=html.text
                self.soup = bs(temp.replace('&lt;','<').replace('&gt','>'))


            except Exception as e:
                print("Error from Requests Module\n")
                print(e,'\n')
                input('ENTER to exit')
                sys.exit()
        else:
            try:
                with open(file,'r',encoding='utf-8') as fp:
                    file_content=fp.read()
                    self.soup=bs(file_content.replace('&lt;','<').replace('&gt','>'),'xml')
            except Exception as e :
                print("Error from Reading File\n")
                print(e,'\n')
                input('ENTER to exit')    
        items=self.soup.find_all('item')
        #print(str(items[0]))
        t=items[0].description.findChild('a').attrs.get('href')
        if len(items) >0:
            print('len: ',len(items))
            for item in items:
                #self.POST_URL=item.description.findChild('a').attrs.get('href')

                self.POST_URL=item.link.text
                try:
                    self.POST_IMG_SRC=item.description.findChild('img').attrs.get('src')
                except:
                    pass
                try:
                    self.POST_SUMMARY=item.description.findChild('p').text.strip(';')
                except:
                    self.POST_SUMMARY=item.description.text

                self.POST_HEADING=item.title.text
                self.POSTS[self.key]={'heading':self.POST_HEADING,'link':self.POST_URL,'img':self.POST_IMG_SRC,'summary':self.POST_SUMMARY}
                self.key=self.key+1
                
                print(self.key)
                print(((self.POST_HEADING).encode('cp850', errors='ignore')).decode('cp850'))

class AlMonitorScrapper:
    SITE_URL='http://www.al-monitor.com'
    SITE_NAME='Al-Monitor'
    POST_DATE=''
    POST_ID=''
    POST_URL=''
    POST_HEADING=''
    POST_SUMMARY=''
    POST_FULLSTORY=''
    POST_IMG_SRC=''
    POSTS={}
    key=0
    def __init__(self,file=None):
        soup=None
        print('file: ',file)
        if file == None:
            try:
                html=requests.get(self.SITE_URL)
                soup=bs(html.content)


            except Exception as e:
                print("Error from Requests Module\n")
                print(e,'\n')
                input('ENTER to exit')
                sys.exit()
        else:
            try:
                with open(file,'r',encoding='utf-8') as fp:
                    file_content=fp.read()
                    soup=bs(file_content)
            except Exception as e :
                print("Error from Reading File\n")
                print(e,'\n')
                input('ENTER to exit')
        
        level1_postlist=soup.find('div',attrs={"class":"carousel-inner span9"}) 
        level2_postlist=level1_postlist.find_all("a")   
        if len(level2_postlist)>0:
            for post in level2_postlist:
                self.POST_URL=self.SITE_URL + post.attrs.get('href')
                self.POST_IMG_SRC= self.SITE_URL + post.img.attrs.get('src')
                self.POST_HEADING=post.h2.text
                self.POST_SUMMARY=post.attrs.get('title')
                

                self.POSTS[self.key]={'heading':self.POST_HEADING,'link':self.POST_URL,'img':self.POST_IMG_SRC,'summary':self.POST_SUMMARY}
                self.key=self.key+1
        # Grabing Breaking News 
        breakingnews=soup.find('div',attrs={"class":"span3 contentRow special"})
        table=breakingnews.table
        tlist=table.find_all('tr')
        for news in tlist:
            try:
                self.POST_URL=self.SITE_URL + news.a.attrs.get('href','')
                self.POST_IMG_SRC= ''
                self.POST_HEADING=news.a.h5.text.replace('\xa0','')
                self.POST_SUMMARY=''

                try:
                    html=requests.get(self.POST_URL)
                    soup2=bs(html.content,)

                except Exception as e:
                    print("Error from Requests Module\n")
                    print(e,'\n')
                    #input('ENTER to exit')
                    #sys.exit()
                    pass
                #level3_postlist=soup2.find('div',attrs={'id','c_story'}) 
                items=soup2.find('div',attrs={'class':'span8','id':'leftcolumn'})
                self.POST_IMG_SRC=self.SITE_URL + items.img.attrs.get('src')
                self.POST_HEADING=items.div.h2.text
                
                para=""
                for item in items.find_all('p'):
                    if (len(item.attrs) ==0):
                        para=para+"\n"+item.text

                self.POST_SUMMARY=para



                self.POSTS[self.key]={'heading':self.POST_HEADING,'link':self.POST_URL,'img':self.POST_IMG_SRC,'summary':self.POST_SUMMARY}
                self.key=self.key+1
                print(self.key)
            except:
                pass

       
                

    def get_Post(self):
        return self.POSTS  
class PunchScrapper:
    SITE_URL='http://www.punchng.com'
    SITE_NAME='Punch'
    POST_DATE=''

    POST_ID=''
    POST_URL=''
    POST_HEADING=''
    POST_SUMMARY=''
    POST_FULLSTORY=''
    POST_IMG_SRC=''
    POSTS={}
    key=0
    def __init__(self,file=None):
        soup=None
        print('file: ',file)
        if file == None:
            try:
                html=requests.get(self.SITE_URL)
                soup=bs(html.content)


            except Exception as e:
                print("Error from Requests Module\n")
                print(e,'\n')
                input('ENTER to exit')
                sys.exit()
        else:
            try:
                with open(file,'r',encoding='utf-8') as fp:
                    file_content=fp.read()
                    soup=bs(file_content)
            except Exception as e :
                print("Error from Reading File\n")
                print(e,'\n')
                input('ENTER to exit')
        
        #level1_postlist=soup.find_all('div',attrs={'class':'td-module-thumb'})
        level1_postlist=soup.find_all('h3',attrs={'class':'entry-title td-module-title'})
        
        if len(level1_postlist)>0:
            for post in level1_postlist:
                
                self.POST_URL= post.a.attrs.get('href')
                try:
                    self.POST_IMG_SRC= post.img.attrs.get('src')
                except Exception as e:
                    pass
                self.POST_HEADING= post.a.attrs.get('title')
                self.POST_ID=hashlib.md5(self.POST_HEADING.encode()).hexdigest()
                try:
                    self.POST_DATE=post.parent.find('div',attrs={'class':'td-post-date'}).text
                except Exception as e:
                    pass
                self.POST_SUMMARY=''
                

                
                # follow the links
       
                try:
                    html=requests.get(self.POST_URL)
                    soup2=bs(html.content)

                except Exception as e:
                    print("Error from Requests Module\n")
                    print(e,'\n')
                    #input('ENTER to exit')
                    #sys.exit()
                    pass
                #level3_postlist=soup2.find('div',attrs={'id','c_story'}) 
                try:
                    items=soup2.find('div',attrs={'class':'td-post-content'})
                    self.POST_IMG_SRC=items.figure.a.attrs.get('href')
                    print('src1... ',self.POST_IMG_SRC)
                except Exception as e:          
                    try:
                        self.POST_IMG_SRC=items.a.attrs.get('href')
                        print('src2... ',self.POST_IMG_SRC)
                    except Exception as e:
                        pass

              
                
                para=""
                redline='Copyright PUNCH'
                try:
                    for item in items.find_all('p',recursive=False):
                        itemtxt=item.text
                        if itemtxt.find(redline)>=0:
                            break
                        para=para+"\n"+itemtxt
                    self.POST_FULLSTORY=para
                    self.POST_SUMMARY=para[:150]
                except Exception as e:
                    pass
                


                self.POSTS[self.key]={'real_date':self.POST_DATE,'post_id':self.POST_ID,'heading':self.POST_HEADING,'site_link':self.SITE_URL,'site_name':self.SITE_NAME,'post_link':self.POST_URL,'img':self.POST_IMG_SRC,'summary':self.POST_SUMMARY,'full_story':self.POST_FULLSTORY}
                self.key=self.key+1

                print(self.key)
                self.POST_DATE=''
                self.POST_ID=''
                self.POST_URL=''
                self.POST_HEADING=''
                self.POST_SUMMARY=''
                self.POST_FULLSTORY=''
                self.POST_IMG_SRC=''

       
                

    def get_Post(self):
        return self.POSTS  








import sys,codecs,sqlite3
from datetime import datetime
if __name__=='__main__':
   
    scrapper= PunchScrapper()
    post_dict=scrapper.POSTS

    l=len(post_dict)
    print(l)
    i=0
    con=sqlite3.connect("db/staging.sqlite")
    cur=con.cursor()
    post_count=cur.execute('SELECT COUNT(*) FROM post_tb_01').fetchone()[0]
    while(i<l):
        try:
            post_count=post_count+1
            print('insert ',i)
            id=post_count
            p_id=str(post_dict[i]['post_id'])
            s_linkn=str(post_dict[i]['site_link'])
            heading=str(post_dict[i]['heading'])
            summary=str(post_dict[i]['summary'])
            p_linkn=str(post_dict[i]['post_link'])
            p_date=str(post_dict[i]['real_date'])
            scrap_date=datetime.today()
            fullstory=str(post_dict[i]['full_story'])
            img=str(post_dict[i]['img'])
            s_name=str(post_dict[i]['site_name'])
            try:
                cur.execute('insert into post_tb_01 values(?,?,?,?,?,?,?,?,?,?,?)',[id,p_id,s_linkn,heading,summary,fullstory,s_name,p_date,img,p_linkn,scrap_date])
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
        finally: 
            con.commit()
            
            i=i+1