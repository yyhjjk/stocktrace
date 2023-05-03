import pandas as pd
import datetime

class 交易:
    "记录模拟股票交易的数据类"
    
    def __init__(self,股票代码,交易策略):
        self.列名=["买入时间","买入价格","卖出时间","卖出价格","收益率","交易周期","盈亏"]
        self.股票代码=股票代码
        self.交易策略=交易策略
        self.买入时间=[]
        self.买入价格=[]
        self.卖出时间=[]
        self.卖出价格=[]
        self.收益率=[]
        self.总收益率=0.0
        self.盈亏=[]
        self.盈亏比=0.0
        self.交易周期=[]
        self.交易次数=0


            
    def datedel(self,dat1,dat2):
        "计算日期相隔多少天,dat1,dat2格式为 %Y-%m-%d %H:%M:%S"
        dat1=datetime.datetime.strptime(dat1,"%Y-%m-%d")
        dat2=datetime.datetime.strptime(dat2,"%Y-%m-%d")
        return (dat1-dat2).days

    def 买入股票(self,买入时间,买入价格):
        买入时间=str(买入时间)[0:10]
        self.买入时间.append(买入时间)
        self.买入价格.append(买入价格)

    
    def 卖出股票(self,卖出时间,卖出价格):
        卖出时间=str(卖出时间)[0:10]
        self.卖出时间.append(卖出时间)
        self.卖出价格.append(卖出价格)
        self.交易次数+=1

    def 计算收益(self):
        if(len(self.卖出价格)>0):
            for i in range(len(self.卖出时间)):
                收益=(self.卖出价格[i]-self.买入价格[i])/self.买入价格[i]
                收益=round(收益,3)
                self.收益率.append(收益)
                if(收益>0):self.盈亏.append(1)
                else:self.盈亏.append(0)
                self.交易周期.append(self.datedel(self.卖出时间[i],self.买入时间[i]))
        
            self.交易次数=len(self.卖出时间)
            self.总收益率=round(sum(self.收益率),4)
            self.盈亏比=round(sum(self.盈亏)/self.交易次数,2)


    def 显示交易(self):
        self.计算收益()
        print(self.股票代码,self.交易策略,"交易次数:"+str(self.交易次数),"总收益率："+str(self.总收益率),"盈亏比率："+str(self.盈亏比))
        print(self.列名)
        if(len(self.卖出价格)>0):
            for i in range(len(self.卖出价格)):
                print(self.买入时间[i],"    %.2f" %(self.买入价格[i]),"    "+self.卖出时间[i],"    %.2f" %(self.卖出价格[i]),
                "    %.3f" %(self.收益率[i]),"          %d" %(self.交易周期[i]),"    %d" %(self.盈亏[i]))
    

    def __str__(self):
        self.计算收益()
        ttstr=""
        mystr=self.股票代码+" "+self.交易策略+"  交易次数:"+str(self.交易次数)+"  总收益率："+str(self.总收益率)+"  盈亏比率："+str(self.盈亏比)+"\n"
        mystr+=str(self.列名)+"\n"
        if(len(self.卖出价格)>0):
            for i in range(len(self.卖出价格)):
                ttstr=ttstr+self.买入时间[i]+"    {:.2f}     ".format(self.买入价格[i])+self.卖出时间[i]+"    {:.2f}  ".format(self.卖出价格[i])+ "     {:.3f}".format(self.收益率[i])+"          {:d}".format(self.交易周期[i])+"      {:d}\n" .format(self.盈亏[i])
        return mystr+ttstr
        

    def outdict(self):
        self.计算收益()
        ttstr=""
        strtitle={"标题":self.股票代码+" "+self.交易策略+"  交易次数:"+str(self.交易次数)+"  总收益率："+str(self.总收益率)+"  盈亏比率："+str(self.盈亏比)}
        strlist={"列名":str(self.列名)}
        if(len(self.卖出价格)>0):
           for i in range(len(self.卖出价格)):
                ttstr=ttstr+self.买入时间[i]+"    {:.2f}     ".format(self.买入价格[i])+self.卖出时间[i]+"    {:.2f}  ".format(self.卖出价格[i])+ "     {:.3f}".format(self.收益率[i])+"          {:d}".format(self.交易周期[i])+"      {:d}    \\n" .format(self.盈亏[i])
        ttstr={"数据":ttstr}
        a=dict(strtitle,**strlist)
        b=dict(a,**ttstr)




        return b



        


if __name__ == '__main__':

    我的交易=交易("600352","kdj策略")
    我的交易.买入股票("2021-10-12", 11.3)
    我的交易.卖出股票("2021-12-24", 13.25)
    我的交易.买入股票("2022-01-12", 13.35)
    我的交易.卖出股票("2022-02-24", 11.25)
    #我的交易.计算收益()
    #我的交易.显示交易()
    print(我的交易.outdict())


    

