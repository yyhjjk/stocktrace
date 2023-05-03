from django.http import HttpResponse
from django.shortcuts import render
import json
from cmdb import stock,jiaoyi,追涨杀跌,均线策略,RSI交易策略,均线穿越策略,布林线策略,kdj策略,macd策略

# 表单
def getsearch(request):
    return render(request, 'cmdb/getsearch.html')
 
# 接收请求数据
def search(request):  
    request.encoding='utf-8'
    message=""


    if 'code' in request.GET and request.GET['code']:
        message = message+'股票代码为: ' + request.GET['code']
        message = message+' 天数为: ' + request.GET['days']
        message =message+' 截至日期：' + request.GET['date']
        message =message+' 交易策略：' + request.GET['tactics']

        股票数据=stock.读取csv数据(str(request.GET['code']),int(request.GET['days']),str(request.GET['date']))
        if(request.GET['tactics']=="追涨杀跌"):
            参数=追涨杀跌.计算最优参数(request.GET['code'],股票数据.最低价,股票数据.最高价,股票数据.收盘价)
            交易=追涨杀跌.追涨杀跌交易策略(request.GET['code'],股票数据.最低价,股票数据.最高价,股票数据.收盘价,参数[0],参数[1])
            mydata=json.dumps(交易.outdict()).encode('utf-8').decode('unicode_escape')
        elif(request.GET['tactics']=="均线策略"):
            参数=均线策略.计算最优参数(request.GET['code'],股票数据.收盘价)
            均线=均线策略.ma(股票数据.收盘价,参数)
            交易=均线策略.均线交易策略(request.GET['code'],股票数据.收盘价,均线,参数)
            mydata=json.dumps(交易.outdict()).encode('utf-8').decode('unicode_escape')
        elif(request.GET['tactics']=="均线穿越策略"):
            参数=均线穿越策略.计算最优参数(request.GET['code'],股票数据.收盘价)
            ma0=均线穿越策略.均线计算(股票数据.收盘价,参数[0])
            ma1=均线穿越策略.均线计算(股票数据.收盘价,参数[1])
            交易=均线穿越策略.均线穿越交易策略(request.GET['code'],股票数据.收盘价,ma0,ma1,参数)
            mydata=json.dumps(交易.outdict()).encode('utf-8').decode('unicode_escape')           
        elif(request.GET['tactics']=="RSI策略"):
            参数=RSI交易策略.计算最优参数(request.GET['code'],股票数据.收盘价) #(5,10,20) 
            交易=RSI交易策略.RSI交易策略(request.GET['code'],股票数据.收盘价,参数)
            mydata=json.dumps(交易.outdict()).encode('utf-8').decode('unicode_escape') 
        elif(request.GET['tactics']=="布林线策略"):
            参数=布林线策略.计算最优参数(request.GET['code'],股票数据.收盘价)
            ma20=布林线策略.ma(股票数据.收盘价,参数)
            up_bb, low_bb=布林线策略.bull(股票数据.收盘价,ma20,参数)
            交易=布林线策略.布林线交易策略(request.GET['code'],股票数据.收盘价,ma20,参数,up_bb,low_bb)
            mydata=json.dumps(交易.outdict()).encode('utf-8').decode('unicode_escape')        

        elif(request.GET['tactics']=="KDJ策略"):
            参数=kdj策略.计算最优参数(request.GET['code'],股票数据.收盘价,股票数据.最低价,股票数据.最高价)
            k,d,j=kdj策略.KDJ(股票数据.收盘价,股票数据.最低价,股票数据.最高价,参数)
            交易=kdj策略.kdj交易策略(request.GET['code'],股票数据.收盘价,k,d,参数)
            mydata=json.dumps(交易.outdict()).encode('utf-8').decode('unicode_escape')      

        elif(request.GET['tactics']=="MACD策略"):
            参数=macd策略.计算最优参数(request.GET['code'],股票数据.收盘价)
            macd,diff,dea=macd策略.计算MACD(股票数据.收盘价,参数[0] ,参数[1],参数[2])
            交易=macd策略.MACD交易策略(request.GET['code'],股票数据.收盘价,diff,dea,参数)
            mydata=json.dumps(交易.outdict()).encode('utf-8').decode('unicode_escape')                  
    else:
        message = '你提交了空表单'
    return HttpResponse(mydata)