#coding=utf-8
from django.http import HttpResponse

def home(request):
    if request.method == 'GET':
        echostr = request.GET.get('echostr', 'None')
        return HttpResponse(echostr)
