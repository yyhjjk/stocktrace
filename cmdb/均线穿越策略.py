#!/usr/bin/env python
# -*-coding:utf-8 -*-
from cmdb import jiaoyi

import pandas as pd



#计算均线参数
def 均线计算(收盘价,均线参数):
    ma=收盘价.rolling(均线参数).mean()
    return ma


#根据交易策略设计模拟交易函数
def 均线穿越交易策略(股票代码,收盘价,ma0,ma1,均线参数):
	i,flag=均线参数[1],0                               #i记录股票交易日起始，s记录交易次数（一次买卖的过程），flag标志持股状态
	交易=jiaoyi.交易(股票代码, str(均线参数[0])+"日穿越"+str(均线参数[1])+"日均线策略")
	while( i< len(收盘价)-1):
		if(ma0[i]> ma1[i] and flag==0):
			交易.买入股票(收盘价.index[i],收盘价[i])
			i=i+1
			flag=1
		else:
			i=i+1
		while(flag and i< len(收盘价)-1):
			if(ma0[i] < ma1[i]):
				交易.卖出股票(收盘价.index[i],收盘价[i])
				i=i+1
				flag=0
			else:
				i=i+1
	return 交易


def 计算最优参数(股票代码,收盘价):
    a=0.0
    a0=0
    a1=0
    for i in range(3,11):
        for j in range(11,30):
            均线参数=(i,j)
            ma0=均线计算(收盘价,均线参数[0])
            ma1=均线计算(收盘价,均线参数[1])
            交易记录=均线穿越交易策略(股票代码,收盘价,ma0,ma1,均线参数)
            交易记录.计算收益()
            #print("均线 %d日 穿越均线 %d日 ： 总收益率：%.3f" %(均线参数[0],均线参数[1],交易记录.总收益率))
            if(交易记录.总收益率> a) : 
                a = 交易记录.总收益率
                a0,a1=均线参数[0],均线参数[1]

    return a0,a1


"""

if __name__=='__main__':
    股票代码='600352'
    天数=1000
    截止日期='20230212'
    股票数据=stock.读取csv数据(股票代码, 天数, 截止日期)


    均线参数=计算最优参数(股票代码,股票数据.收盘价) #设置短周期参数为5日，长周期参数为20日
    ma0=均线计算(股票数据.收盘价,均线参数[0])
    ma1=均线计算(股票数据.收盘价,均线参数[1])
    交易记录=均线穿越交易策略(股票代码,股票数据.收盘价,ma0,ma1,均线参数)
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


添加买卖点 = [画K线.mpf.make_addplot(买入交易.买入价格, scatter=True, markersize=50, marker='s', color='r'),
        画K线.mpf.make_addplot(卖出交易.卖出价格, scatter=True, markersize=50, marker='v', color='b')
]


画K线.绘图参数 = dict(
	type='candle', 
	mav=均线参数, 
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