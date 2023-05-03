import numpy as np
import pandas as pd
from cmdb import jiaoyi




#计算EMA
def calculateEMA(period, closeArray, emaArray=[]):
	length = len(closeArray)
	nanCounter = np.count_nonzero(np.isnan(closeArray))
	if not emaArray:
		emaArray.extend(np.tile([np.nan],(nanCounter + period - 1)))
		firstema = np.mean(closeArray[nanCounter:nanCounter + period - 1])    
		emaArray.append(firstema)    
		for i in range(nanCounter+period,length):
			ema=(2*closeArray[i]+(period-1)*emaArray[-1])/(period+1)
			emaArray.append(ema)        
	return np.array(emaArray)

 #计算MACD的值   
def 计算MACD(closeArray,shortPeriod = 12 ,longPeriod = 26 ,signalPeriod =9):
	ema12 = calculateEMA(shortPeriod ,closeArray,[])
	ema26 = calculateEMA(longPeriod ,closeArray,[])
	diff = ema12-ema26
	dea= calculateEMA(signalPeriod ,diff,[])
	macd = 2*(diff-dea)
	diff=np.round(diff,3)
	dea=np.round(dea,3)
	macd=np.round(macd,3)
	return macd,diff,dea 

#计算收益率，规则：diff大于dea买进，diff小于dea卖出
def MACD交易策略(code,close,diff,dea,参数=(12,26,9)):
	交易=jiaoyi.交易(code, "macd交易策略 参数:"+str(参数))
	i,flag=参数[1],0            #i=26（macd以12天为参数)，i记录股票交易日，s记录交易次数（一次买卖的过程），flag标志持股状态

	while( i< len(close)-1):
		if(diff[i]> dea[i]  and flag==0):
			交易.买入股票(close.index[i],close[i])
			i=i+1
			flag=1
		else:
			i=i+1
		while(flag and i< len(close)-1):
			if(diff[i]< dea[i] ):
				交易.卖出股票(close.index[i],close[i])
				i=i+1
				flag=0
			else:
				i=i+1

	return 交易

def 计算最优参数(股票代码,收盘价):
    a=0.0
    参数=(6,14,3)
    for i in range(3,20):
            macd,diff,dea=计算MACD(收盘价,shortPeriod = i+3 ,longPeriod = (i+3)*2+2 ,signalPeriod =i)
            交易记录=MACD交易策略(股票代码,收盘价,diff,dea,参数=(i+3,(i+3)*2+2 ,i))
            交易记录.计算收益()
            if(交易记录.总收益率> a) : 
                a = 交易记录.总收益率
                参数=(i+3,(i+3)*2+2 ,i)

    return 参数
#low,high,close=getdata(code,dayss,dayend)
#macd,diff,dea=calculateMACD(close,shortPeriod = 12 ,longPeriod = 26 ,signalPeriod =9)
#sr=rateMACD(code,close,diff,dea)
#print(sr)
