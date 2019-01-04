from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.forms import ValidationError
from .models import Users
from datetime import datetime
from .apis import Page, APIValueError, APIResourceNotFoundError
import json, hashlib
import demjson

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


def main(request):
    return render(request, 'main.html')


def login(request):

    if request.method == 'POST':
        json_result = json.loads(request.body)
        password = json_result["password"]
        email = json_result["email"]

        if password == '' or email == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        # 根据其他条件进行查找
        user = Users.objects.filter(email=email)

        if user:
            print(user)
            # check passwd:
            sha1 = hashlib.sha1()
            print(sha1)
            sha1.update(user.id.encode('utf-8'))
            sha1.update(b':')
            sha1.update(password.encode('utf-8'))
            if user.passwd != sha1.hexdigest():
                return JsonResponse({'status': 10022, 'message': 'Invalid password'})

        else:
            return JsonResponse({'status': 10022, 'message': 'Email not exist'})

        # authenticate ok, set cookie:
        # response = web.Response()
        # response.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
        # user.passwd = '******'
        # response.content_type = 'application/json'
        # response.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
        # JsonResponse({'status': 200, 'message': 'add event success'})
        #
        # return response

    return render(request, 'login.html')


def register(request):

    if request.method == 'POST':

        json_result = json.loads(request.body)
        name = json_result["name"]
        password = json_result["password"]
        email = json_result["email"]
        add_date = datetime.now()
        print("name:%s,email:%s,password:%s" % (name, email, password))
        if name == '' or password == '' or email == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        # 判断发布会名称重复
        result = Users.objects.filter(email=email)
        if result:
            return JsonResponse({'status': 10023, 'message': 'email already exists'})

        try:
            # 将数据保存到数据库
            Users.objects.create(name=name, password=password, email=email, add_date=add_date)
        except ValidationError as e:
            error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS'
            return JsonResponse({'status': 10024, 'message': error})

        return JsonResponse({'status': 200, 'message': 'add event success'})

    # 根据primary key查找
    try:
        user = Users.objects.get(pk=1)
        print(user)
    except Exception as e:
        print(e)

    # 根据其他条件进行查找
    user = Users.objects.filter(name="SIM")
    print(user)
    # 根据其他条件进行查找
    user = Users.objects.all()
    print(user)

    user = Users.objects.count()
    print(user)
    # 删除
    # user = Users.objects.get(pk=1)
    # user.delete()

    # 修改
    # user = Users.objects.get(name="SIM")
    # user.admin = False
    # user.save()

    return render(request, 'register.html')


class TestInfo(object):
    def __init__(self, title, content):
        self.title = title  # 判断模块是否检测完成，0-未完成，1-完成
        self.content = content    # 测试次数


testdata = TestInfo("test", "test")


def blogs(request):
    # if request.method == "POST":
    #     print("POST")
    #     print(json.loads(request.body))
    # elif request.method == "GET":
    #     print("GET")
    #     return JsonResponse({'status': 10023, 'message': 'email already exists', 'page_index': 3})
    return render(request, 'manage_blogs.html', {'data': testdata})


def create(request):
    if request.method == 'POST':

        json_result = json.loads(request.body)
        print("json_result:%s" % json_result)
        title = json_result["name"]
        content = json_result["content"]

        print("title:%s,content:%s" % (title, content))
        testdata.title = title
        testdata.content = content
        if title == '' or content == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        return JsonResponse({'status': 200, 'message': 'add event success'})

    return render(request, 'manage_blog_create.html')


def users(request):
    if request.method == 'GET':
        page = request.GET.get('page')

        if page:
            # 获取用户总数
            page_index = get_page_index(page)
            num = Users.objects.count()

            p = Page(num, page_index)
            if num == 0:
                return dict(page=p, users=())

            response = {"status": 200, "page": 0, "users": []}
            response["page"] = p
            response["page"] = eval(str(p))

            print("offset:", p.offset)
            print("limit:", p.limit)
            # 通过时间排序，获取从offset到limit的记录数据
            users = Users.objects.all()[p.offset:p.limit]
            print(users)
            # 将密码置成*了再穿给浏览器，不然用户就看到密码了
            for u in users:
                u.password = '******'
                response["users"].append(eval(str(u)))

            response_json = json.dumps(response)
            print(response_json)
            return HttpResponse(response_json)
            # return dict(status_code='200', page=p, users=users)
        else:
            page_index = get_page_index("1")
            p = Page(0, page_index)
            return render(request, 'manage_users.html', {'page': p})

    else:
        return render(request, 'manage_users.html')


def comments(request):
    return render(request, 'manage_comments.html')


# 写博客上传图片
def blog_img_upload(request):
    if request.method == "POST":
        data = request.FILES['editormd-image-file']
        img = Image.open(data)
        width = img.width
        height = img.height
        rate = 1.0  # 压缩率

        # 根据图像大小设置压缩率
        if width >= 2000 or height >= 2000:
            rate = 0.3
        elif width >= 1000 or height >= 1000:
            rate = 0.5
        elif width >= 500 or height >= 500:
            rate = 0.9

        width = int(width * rate)  # 新的宽
        height = int(height * rate)  # 新的高

        img.thumbnail((width, height), Image.ANTIALIAS)  # 生成缩略图

        url = 'blogimg/' + data.name
        name = settings.MEDIA_ROOT + '/' + url
        while os.path.exists(name):
            file, ext = os.path.splitext(data.name)
            file = file + str(random.randint(1, 1000))
            data.name = file + ext
            url = 'blogimg/' + data.name
            name = settings.MEDIA_ROOT + '/' + url
        try:
            img.save(name)
            url = '/static'+name.split('static')[-1]
            return JsonResponse({'success': 1, 'message': '成功', 'url': url})
        except Exception as e:
            return JsonResponse({'success': 0, 'message': '上传失败'})
