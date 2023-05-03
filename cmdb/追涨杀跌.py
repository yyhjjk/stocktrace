from cmdb import jiaoyi
#import stock






def 追涨杀跌交易策略(code,low,high,close,number,number1):
	number=number/100
	number1=number1/100
	i,s,flag=0,0,0                               #i记录股票交易日，s记录交易次数（一次买卖的过程），flag标志持股状态
	q=low[0]						#q记录每一交易区间的最低价格
	t=high[0]						#t主录每一交易区间最高价格
	交易=jiaoyi.交易(code, "上涨"+str(number)+",下跌"+str(number1)+"交易策略")

	while( i< len(low)-1):
		if((close[i]-q)/q >=number and flag==0):
			交易.买入股票(close.index[i],close[i])
			t=high[i]
			i=i+1
			if(high[i]>t): t=high[i]
			flag=1
		else:
			i=i+1	
			if(low[i]<q):q=low[i]
		while(flag and i< len(low)-1):
			if((t-close[i])/t >=number1 ):
				交易.卖出股票(close.index[i],close[i])
				q=low[i]
				i=i+1
				if(low[i]<q):q=low[i]
				s=s+1
				flag=0
			else:
				i=i+1
				if(high[i]>t): t=high[i]

	return 交易


def 计算最优参数(code,low,high,close):
    收益率=0.0
    最佳参数=(0,0)
    for 参数 in range(1,11):
        for 参数1 in range(1,11):
            交易记录=追涨杀跌交易策略(code,low,high,close,参数,参数1)
            交易记录.计算收益()
            #print("参数1：%d ,参数2：%d 总收益率：%.2f 盈亏比： %.2f" %(参数,参数1,交易记录.总收益率,交易记录.盈亏比))
            if (交易记录.总收益率 > 收益率):
                收益率=交易记录.总收益率
                最佳参数=(参数,参数1)
    return 最佳参数


if __name__ == '__main__':
    股票代码='300114'
    天数=100
    截止日期='20230215'
    股票数据=stock.读取csv数据(股票代码, 天数, 截止日期)
    #print(股票数据.index)
    参数=计算最优参数(股票代码,股票数据.最低价,股票数据.最高价,股票数据.收盘价)
    print(参数)
    交易=追涨杀跌交易策略(股票代码,股票数据.最低价,股票数据.最高价,股票数据.收盘价,参数[0],参数[1])
    print(交易)