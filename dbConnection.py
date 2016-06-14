import sqlite3
import time
import datetime


class myConnection:
    """description of class"""
    DBNAME='db/post_pro01.sqlite'
    TBNAME='post_tb_01'

    con=''
    cur=''


    def __init__(self):
    
        try:
            self.con=sqlite3.connect(self.DBNAME)
        except sqlite3.Error as e:
            print(e)
        self.cur=self.con.cursor()

       
    def db_create(self):
        query='CREATE  TABLE  IF NOT EXISTS "{0}" (\
	                "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE  DEFAULT CURRENT_TIMESTAMP,\
	                "post_id" VARCHAR  NOT NULL  UNIQUE  DEFAULT CURRENT_TIMESTAMP,\
	                "link" VARCHAR,\
	                "heading" TEXT,\
	                "summary" TEXT, \
	                "full_story" TEXT, \
	                "site" VARCHAR \
	            )'.format(self.TBNAME)
            
        self.cur.execute(query)
        return self.cur

    def db_insert(self,my_dict={}):
        lin=str(post_dict[i]['link'])
        h=str(post_dict[i]['heading'])
        s=str(post_dict[i]['summary'])
        cur.execute('insert into post values(?,?,?,?)',[i,lin,h,s])
                




        



