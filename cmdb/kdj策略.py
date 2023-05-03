from cmdb import jiaoyi
import pandas as pd


#计算kdj值列表
def KDJ(收盘价,最低价,最高价,参数):
    low_min=最低价.rolling(参数, min_periods=参数).min()
    high_max=最高价.rolling(参数,min_periods=参数).max()
    rsv=(收盘价-low_min)/(high_max-low_min)*100
    K=pd.DataFrame(rsv).ewm(com=2).mean()
    D=K.ewm(com=2).mean()
    J=3*K-2*D
    K=round(K,2)
    D=round(D,2)
    J=round(J,2)
    return K,D,J



#根据交易策略设计模拟交易函数
def kdj交易策略(股票代码,收盘价,k,d,参数):
	i,flag=参数,0                               #i记录股票交易日起始，s记录交易次数（一次买卖的过程），flag标志持股状态
	交易=jiaoyi.交易(股票代码, "kdj策略 参数:"+str(参数))
	while( i< len(收盘价)-1):
		if(k[0][i]> d[0][i] and flag==0):
			交易.买入股票(收盘价.index[i],收盘价[i])
			i=i+1
			flag=1
		else:
			i=i+1
		while(flag and i< len(收盘价)-1):
			if(k[0][i] < d[0][i]):
				交易.卖出股票(收盘价.index[i],收盘价[i])
				i=i+1
				flag=0
			else:
				i=i+1
	return 交易

def 计算最优参数(股票代码,收盘价,最低价,最高价):
    a=0.0
    参数=1
    for i in range(3,20):
            K,D,J=KDJ(收盘价,最低价,最高价,i)
            交易记录=kdj交易策略(股票代码,收盘价,K,D,i)
            交易记录.计算收益()
            if(交易记录.总收益率> a) : 
                a = 交易记录.总收益率
                参数=i

    return 参数