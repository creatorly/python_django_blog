from django.shortcuts import render
from .models import UserInfo

# Create your views here.
userlist = []


def test(request):
    # 1.return data
    # return HttpResponse("Hello World!")
    
    # 2.retutn enter date
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     print(username,password)
    #     tempuser = {'user':username, 'pwd':password}
    #     userlist.append(tempuser)

    # return render(request,'test.html', {'data':userlist})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 将数据保存到数据库
        UserInfo.objects.create(user=username, pwd=password)
        
    # 将数据库中的所有数据读取出来
    userlist = UserInfo.objects.all()
    return render(request, 'test.html', {'data': userlist})

    