from django.shortcuts import render, HttpResponse

# Create your views here.
from io import BytesIO
from utils import check_code
from VerifyCode import models


def login(request):
    if request.method == "GET":
        msg = ("", "")
        return render(request, "index.html", {msg: ""})
    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        code_submit = request.POST.get("checkcode", "")
        code_session = request.session["CheckCode"]
        print("code_submit:", code_submit)
        print("code_session:", code_session)
        if code_submit.upper() == code_session.upper():
            print("验证码正确")
            user = models.Loginer.objects.filter(username=username).first()
            print(type(user))
            if username == user.username and password == user.password:
                print("登陆成功")
                return render(request, "homepage.html", {"user": user})
            else:
                print("用户名或密码错误")
                msg = ("用户名或密码错误", "")
                return render(request, "index.html", {"msg": msg})
        else:
            print("验证码错误")

            msg = ("", "验证码错误")
            return render(request, "index.html", {"msg": msg})


def get_check_code(request):
    stream = BytesIO()
    img, code = check_code.create_calidate_code()
    request.session["CheckCode"] = code
    img.save(stream, "PNG")
    return HttpResponse(stream.getvalue())


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        models.Loginer.objects.create(username=username, password=password)
    return render(request, "index.html")

