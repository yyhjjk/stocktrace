# Python股票量化分析平台说明如下：

# 1.python量化分析平台程序架构
## 该平台使用Django框架做服务端，用手机APP，本地java程序作为客户端访问。

# 2.cmdb目录文件介绍

         cmdb目录下放置python程序，用来响应请求。
         cmdb/jiaoyi为交易类，根据交易策略模拟交易，输出交易结果，主要以json形式输出，也有字符串形式输出。

# 3. 数据源连接程序
    stock.py文件为数据源连接文件，可根据需要设置。支持mysql,sqlite,csv文件等。

# 4.web响应get请求文件
   getsearch.py文件响应网络请求。

# 5.交易策略文件

     kdj策略.py，macd策略.py，RSI交易策略.py，布林线策略.py，均线策略.py，均线穿越策略.py，追涨杀跌.py为交易策略执行文件

#  6.手机端app程序
     djingo-hellowrold.rar为android 手机端源码。


# 7.重要提示
     代码中大量使用中文命名函数名，变量名，类名，如有不适，请绕开。。。
     
     
# 详细说明网站 python量化分析
    https://author.baidu.com/home?from=bjh_article&app_id=1724269905542206
