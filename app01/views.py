from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
# Create your views here.
from app01 import models
import json

def index(request):
        return render(request, 'index.html')

def get_imgs(request):
        nid = request.GET.get('nid')
        img_list = models.Img.objects.filter(id__gt=nid).values('id', 'src', 'title')
        img_list = list(img_list)
        ret = {
            'status': True,
            'data': img_list
        }
        return JsonResponse(ret)


def login(request):
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    print(user)
    if request.method=="GET":
        return render(request,"login.html")
    elif request.method=="POST":
        user_list = models.User.objects.filter(username=user)
        if user_list and user_list[0].pwd==pwd:
            return render(request,"blog.html")
        else:
            error = "用户名或密码错误"
            return render(request,"login.html",locals())


    return render(request,'login.html')
def register(request):

    if request.method=="GET":
        return render(request,'register.html')
    elif request.method=="POST":
        user = request.POST.get("user")
        pwd = request.POST.get("user")
        email = request.POST.get("email")
        headimg = request.POST.get("headimg")
        user_try = models.User.objects.filter(username=user)
        email_try = models.User.objects.filter(email=email)
        if not user_try and not email_try:
            models.User.objects.create(username=user,pwd=pwd,email=email,img=headimg)
            return render(request,"blog.html")
        else:
            error = "用户名或邮箱已存在"
            return render(request,"register.html",locals())

class blog():
    def __init__(self,sss):
        self.sss=sss
        pass
    def yy(self):
        return render(self, "blog.html")
    def home(self):
        return render(self, "blog_home.html")
    def good(self):
        return render(self, "blog_good.html")
    def new(self):
        return render(self, "blog_new.html")
