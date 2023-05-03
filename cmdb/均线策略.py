#!/usr/bin/env python
# -*-coding:utf-8 -*-
from cmdb import jiaoyi
import pandas as pd
#import 画K线


def ma(close,参数):
    ma3=close.rolling(参数).mean()
    return ma3

def 均线交易策略(code,close,ma,num):
	i,s,flag=num,0,0                               #i记录股票交易日起始，s记录交易次数（一次买卖的过程），flag标志持股状态
	交易=jiaoyi.交易(code, str(num)+"日均线策略")
	while( i< len(close)-1):
		if(close[i]> ma[i] and flag==0):
			交易.买入股票(close.index[i],close[i])
			i=i+1
			flag=1
		else:
			i=i+1
		while(flag and i< len(close)-1):
			if(close[i] < ma[i]):
				交易.卖出股票(close.index[i],close[i])
				i=i+1
				s=s+1
				flag=0
			else:
				i=i+1
				

	return 交易

def 计算最优参数(code,close):
    收益率=0.0
    最佳参数=3
    for i in range(3,100):
        均线=ma(close,i)
        交易记录=均线交易策略(code,close,均线,i)
        交易记录.计算收益()
        if (交易记录.总收益率 > 收益率):
                收益率=交易记录.总收益率
                最佳参数=i
    return 最佳参数	    
    

"""
股票代码='002191'
天数=500
截止日期='20210312'

股票数据=stock.读取csv数据(股票代码, 天数, 截止日期)

print(股票数据)

ma3,ma4,ma5,ma6,ma7,ma10,ma20=ma(股票数据.收盘价)

num=20
交易记录=均线交易策略(股票代码,股票数据.收盘价,ma20,num)
交易记录.显示交易()

#画K线图
k线数据=画K线.读取数据(股票代码, 天数, 截止日期)



#K线图上标记买入价格，卖出价格点
buypd=pd.DataFrame(data={'Date':交易记录.买入时间,'买入价格':交易记录.买入价格})
buypd.Date=pd.to_datetime(buypd.Date)
buypd.set_index('Date',drop=True,append=False, inplace=True)
sellpd=pd.DataFrame(data={'Date':交易记录.卖出时间,'卖出价格':交易记录.卖出价格})
sellpd.Date=pd.to_datetime(sellpd.Date)
sellpd.set_index('Date',drop=True,append=False, inplace=True)

买入交易 = pd.merge(k线数据.Close,buypd,on=['Date'],how='outer')
卖出交易 = pd.merge(k线数据.Close,sellpd,on=['Date'],how='outer')
#buyts=pd.merge(df,buypd,how='left')

添加买卖点 = [画K线.mpf.make_addplot(买入交易.买入价格, scatter=True, markersize=50, marker='s', color='r'),
        画K线.mpf.make_addplot(卖出交易.卖出价格, scatter=True, markersize=50, marker='v', color='b')
]




画K线.绘图参数 = dict(
	type='candle', 
	mav=(num), 
	addplot=添加买卖点, 
	volume=True, 
	datetime_format="%Y-%m-%d",
	title='\n股票代码 %s K线图' % (股票代码),    
	ylabel='股票蜡烛价格', 
	ylabel_lower='成交量', 
	warn_too_much_data=2000,  #设置最大显示数据记录条数
	figratio=(15, 10), 
	figscale=10)

画K线.mpf.plot(k线数据, 
	**画K线.绘图参数, 
	style=画K线.s, 
	show_nontrading=False
	)

画K线.mpf.show()


"""






