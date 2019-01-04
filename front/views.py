from django.shortcuts import HttpResponse
from django.shortcuts import redirect


def index(request):
    username = request.GET.get('username')
    if username:
        return HttpResponse("前台首页")
    else:
        return redirect('/login/')


def login(request):
    return HttpResponse("前台登录页面")


def login_user(request, username):
    search = request.GET.get('search')
    text = "你好：%s,搜索内容：%s" % (username, search)
    if search == "test":
        return redirect('/login/')
    else:
        return HttpResponse(text)


