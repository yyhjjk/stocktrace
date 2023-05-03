from django.shortcuts import render

context          = {}
context['hello'] = '这世界，我来啦！！!'
context['test']="天涯风云，这是我的世界"

context['ppp']="这也是策略实验！！"
 
def showlogin(request):
    return render(request, 'cmdb/login.html',context)

def index(request):
    return render(request, 'cmdb/index.html',context)



