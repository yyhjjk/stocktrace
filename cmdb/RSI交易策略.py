import pandas as pd
import numpy as np
from cmdb import jiaoyi
#import 画K线
import numpy as np

def RSI(array_list, periods=14):
    length = len(array_list)
    rsies = [np.nan] * length
    if length <= periods:
        return rsies
    up_avg = 0
    down_avg = 0

    first_t = array_list[:periods + 1]
    for i in range(1, len(first_t)):
        if first_t[i] >= first_t[i - 1]:
            up_avg += first_t[i] - first_t[i - 1]
        else:
            down_avg += first_t[i - 1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    #print("{}日,up_avg:{},down_avg:{}".format(array_list.index[periods],up_avg,down_avg))
    rs = up_avg / down_avg
    rsies[periods] = 100 - 100 / (1 + rs)

    for j in range(periods + 1, length):
        up = 0
        down = 0
        if array_list[j] >= array_list[j - 1]:
            up = array_list[j] - array_list[j - 1]
            down = 0
        else:
            up = 0
            down = array_list[j - 1] - array_list[j]
        up_avg = (up_avg * (periods - 1) + up) / periods
        down_avg = (down_avg * (periods - 1) + down) / periods
        #print("{}日,up:{},down:{}".format(array_list.index[j],up,down))
        #print("{}日,up_avg:{},down_avg:{}".format(array_list.index[j],up_avg,down_avg))
        rs = up_avg / down_avg
        rsies[j] = 100 - 100 / (1 + rs)
    
    rsies=np.round(rsies,3)
    rsies=pd.Series(rsies, index = array_list.index)
    #rsies=rsies.dropna()
    return rsies

def rsi0(price,period=6):

    clprcChange = price - price.shift(1)
    clprcChange[0] = 0
    indexprc = clprcChange.index
    
    upPrc = pd.Series(0, index = indexprc)
    upPrc[clprcChange > 0] = clprcChange[clprcChange > 0]
    downPrc = pd.Series(0, index = indexprc )
    downPrc[clprcChange < 0] = - clprcChange[clprcChange < 0]
    

    
    SMUP=upPrc.rolling(period).mean()
    SMDOWN=downPrc.rolling(period).mean()
    #rsi = [100 - 100/ (1 + SMUP[i]/SMDOWN[i]) for i in range(0,len(SMUP))]
    
    rsi = [100 * SMUP[i] / (SMUP[i] + SMDOWN[i]) for i in range(0,len(SMUP))]
    rsi = pd.Series(rsi, index = SMUP.index)
    #print(rsi)
    
    return rsi




def RSI交易策略(股票代码,收盘价,参数=(6,12,24)):
	rsi=(rsi0(收盘价,参数[0]),rsi0(收盘价,参数[1]),rsi0(收盘价,参数[2]))
	i,s,flag=参数[2],0,0                               #i记录股票交易日起始，s记录交易次数（一次买卖的过程），flag标志持股状态
	交易=jiaoyi.交易(股票代码, "RSI策略 参数："+str(参数))
	while( i< len(收盘价)-1):
		if(rsi[0][i]> rsi[1][i] and flag==0):
			交易.买入股票(收盘价.index[i],收盘价[i])
			i=i+1
			flag=1
		else:
			i=i+1
		while(flag and i< len(收盘价)-1):
			if(rsi[0][i]< rsi[1][i]  and flag==1):
				交易.卖出股票(收盘价.index[i],收盘价[i])
				i=i+1
				s=s+1
				flag=0
			else:
				i=i+1
				

	return 交易

def RSI1交易策略(股票代码,收盘价,参数=(6,12,24)):
	rsi=(RSI(收盘价,参数[0]),RSI(收盘价,参数[1]),RSI(收盘价,参数[2]))
	i,s,flag=参数[0],0,0                               #i记录股票交易日起始，s记录交易次数（一次买卖的过程），flag标志持股状态
	交易=jiaoyi.交易(股票代码, "RSI策略")
	while( i< len(收盘价)-1):
		if(rsi[0][i]> rsi[1][i] and flag==0):
			交易.买入股票(收盘价.index[i],收盘价[i])
			i=i+1
			flag=1
		else:
			i=i+1
		while(flag and i< len(收盘价)-1):
			if(rsi[0][i]< rsi[1][i]  and flag==1):
				交易.卖出股票(收盘价.index[i],收盘价[i])
				i=i+1
				s=s+1
				flag=0
			else:
				i=i+1
				

	return 交易


def 计算最优参数(股票代码,收盘价):
    a=0.0
    参数=(3,6,12)
    for i in range(3,20):
            交易记录=RSI交易策略(股票代码,收盘价,参数=(i,i*2,i*4))
            交易记录.计算收益()
            if(交易记录.总收益率> a) : 
                a = 交易记录.总收益率
                参数=(i,i*2,i*4)

    return 参数

"""
股票代码='002191'
天数=500
截止日期='20230225'
股票数据=stock.读取csv数据(股票代码, 天数, 截止日期)
收盘价=股票数据.收盘价

参数=(6,12,24)
rsi=(rsi0(收盘价,参数[0]),rsi0(收盘价,参数[1]),rsi0(收盘价,参数[2]))


交易记录=RSI交易策略(股票代码,收盘价,参数=(6,12,24))
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


#添加RSI指标到K线图中
添加rsi = [画K线.mpf.make_addplot(rsi[0], type='line',panel=1),画K线.mpf.make_addplot(rsi[1], type='line',panel=1)]   #panel=1设置kdj指标放在图中间
添加买卖点 += 添加rsi


画K线.绘图参数 = dict(
	type='candle', 
	mav=(5), 
	addplot=添加买卖点, 
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