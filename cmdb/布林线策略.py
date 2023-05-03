import pandas as pd
from cmdb import jiaoyi


def ma(收盘价, 参数): 
    均线 = 收盘价.rolling(参数).mean() 
    均线=round(均线,3)
    return 均线

def bull(收盘价, 均线, 参数):
    std = 收盘价.rolling(参数).std()
    up_bb = 均线 + std * 2 
    low_bb = 均线 - std * 2 
    up_bb,low_bb=round(up_bb,3),round(low_bb,3)
    return up_bb, low_bb 



def 布林线交易策略(code,close,ma20,num,up_bb,low_bb):
	i,s,flag=num,0,0                               #i记录股票交易日起始，s记录交易次数（一次买卖的过程），flag标志持股状态
	交易=jiaoyi.交易(code, str(num)+"日布林线策略")
	while( i< len(close)-3):
		if(close[i]< low_bb[i] and close[i+1] > low_bb[i+1] and flag==0):
			交易.买入股票(close.index[i],close[i])
			i=i+1
			flag=1
		else:
			i=i+1
		while(flag and i< len(close)-3):
			if(close[i] > up_bb[i] and close[i+1] < up_bb[i+1]):
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
        均线=ma(close, i)
        up_bb, low_bb=bull(close, 均线,  i)
        交易记录=布林线交易策略(code,close,均线,i,up_bb,low_bb)
        交易记录.计算收益()
        if (交易记录.总收益率 > 收益率):
                收益率=交易记录.总收益率
                最佳参数=i
    return 最佳参数	 
"""

股票代码='002191'
天数=500
截止日期='20220312'

股票数据=stock.读取csv数据(股票代码,天数,截止日期)


参数=20
ma20=ma(股票数据.收盘价,参数)
up_bb, low_bb=bull(股票数据.收盘价,ma20,参数)

交易记录=布林线交易策略(股票代码,股票数据.收盘价,ma20,参数,up_bb,low_bb)
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


#添加布林线指标到K线图中
添加bull= [画K线.mpf.make_addplot(up_bb, type='line',panel=0),画K线.mpf.make_addplot(low_bb, type='line',panel=0)]   #panel=1设置kdj指标放在图中间
添加买卖点 += 添加bull

画K线.绘图参数 = dict(
	type='candle', 
	mav=参数, 
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