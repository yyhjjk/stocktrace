#!/usr/bin/env python
# -*-coding:utf-8 -*-
import datetime
import sqlite3
import pymysql
from sqlalchemy import create_engine
import pandas as pd

code="000001"                #股票代码
dayss=1000                 #截止日期之前天数
dayend="20230101"             #截止日期
dbfile="D:\\炒股软件项目\\股票数据采集\\csvtodb20220312.db"                #sqlite数据库存放位置
path="D:\\炒股软件项目\\股票数据采集\\日线数据20230219\\"                    #csv文件目录
myini={"用户名":"root","密码":"rootlizigushi","域名ip":"127.0.0.1","端口号":23306,"数据库名":"stockx"}   #mysql数据库配置文件

def 读取csv数据(code,dayss,dayend):
    date_end_str=dayend[0:4]+'-'+dayend[4:6]+'-'+dayend[6:8]
    date_end = datetime.datetime.strptime(date_end_str, "%Y-%m-%d")
    date_start = (date_end + datetime.timedelta(days=-dayss)).strftime("%Y-%m-%d")
    date_end = date_end.strftime("%Y-%m-%d")
    #stock_X=pd.read_csv(path+code+".csv",usecols=["date","open","high","close","low","volume"],index_col='date',encoding='gbk')
    stock_X=pd.read_csv(path+code+".csv",usecols=["日期","开盘价","最高价","最低价","收盘价","成交量"],index_col='日期',encoding='gbk')
    stock_X=stock_X.loc[(stock_X.index >= date_start) & (stock_X.index <= date_end )]
    stock_X=stock_X.sort_index()
    return stock_X

    	


def 读取mysql数据(code,dayss,dayend):
    date_end_str=dayend[0:4]+'-'+dayend[4:6]+'-'+dayend[6:8]	  
    date_end = datetime.datetime.strptime(date_end_str, "%Y-%m-%d")
    date_start = (date_end + datetime.timedelta(days=-dayss)).strftime("%Y-%m-%d")
    date_end = date_end.strftime("%Y-%m-%d")
    pymysql.install_as_MySQLdb()
    dbstring="mysql+mysqldb://%(用户名)s:%(密码)s@%(域名ip)s:%(端口号)d/%(数据库名)s?charset=utf8" %(myini)
    engine=create_engine(dbstring)
    sql="select 日期,开盘价,收盘价,最高价,最低价,成交量 from eb_%s where 日期 >= '%s' and 日期 <= '%s'" %(code,date_start,date_end)
    stock_X=pd.read_sql(sql,engine,index_col='日期')
    stock_X=stock_X.sort_index()
    return stock_X
    	


def 读取sqlite数据(code,dayss,dayend):

	date_end_str=dayend[0:4]+'-'+dayend[4:6]+'-'+dayend[6:8]	  
	date_end = datetime.datetime.strptime(date_end_str, "%Y-%m-%d")
	date_start = (date_end + datetime.timedelta(days=-dayss)).strftime("%Y-%m-%d")
	date_end = date_end.strftime("%Y-%m-%d")
	conn=sqlite3.connect(dbfile)
	sql="select 日期,开盘价,收盘价,最高价,最低价,成交量 from eb_%s where 日期 >= '%s' and 日期 <= '%s'" %(code,date_start,date_end)
	stock_X=pd.read_sql(sql,conn,index_col='日期')
	stock_X=stock_X.sort_index()
	conn.close()
	return stock_X




#stock=读取sqlite数据(code,dayss,dayend)
#print(stock)

#stock=读取csv数据(code,dayss,dayend)
#print(stock)
