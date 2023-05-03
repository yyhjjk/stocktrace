# -*- coding: utf-8 -*-
 
from django.shortcuts import render
from django.views.decorators import csrf

import pandas as pd
from cmdb import stock




# 接收POST请求数据


def search_post(request):
    ctx ={}
    if request.POST:
        ctx['code'] = str(request.POST['code'])
        ctx['days']=int(request.POST['days'])
        ctx['date']=str(request.POST['date'])
        ctx['mydata']=stock.读取csv数据(ctx['code'],ctx['days'],ctx['date'])

       
    return render(request, "cmdb/post.html", ctx)
