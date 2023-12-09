from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from master.models import *
from .models import *
import hashlib
from django.db.models import F


def get_hashlib(value):
    m = hashlib.md5()  # 指定算法

    m.update(value.encode())  # 输入计算的值

    output = m.hexdigest()  # 获得哈希值
    return output


# Create your views here.
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':

        # 创建用户
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = UserInformation.objects.filter(username=username, is_active=True)

        if user.exists() and user[0].password == get_hashlib(password):
            request.session['user_id'] = user[0].id
            return HttpResponseRedirect(reverse('master:index'))
        else:
            comment = '用户名或密码错误'
            return render(request, 'login.html', locals())


def register_view(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == 'POST':
        # 获取表单数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        phonenum = request.POST.get('phonenum')

        print('success get form data')

        username, password, repassword, phonenum = [
            v if v != '' else 'no' for v in [username, password, repassword, phonenum]
        ]
        print(username, password, repassword, phonenum)

        # 检查是否有字段是默认值
        if 'no' in [username, password, repassword, phonenum]:
            return render(request, 'register.html', locals())
        if len(username) > 11:
            comment = '用户名过长，不可超过11字'
            return render(request, 'register.html', locals())
        if UserInformation.objects.filter(username=username, is_active=True).exists():
            comment = '用户名已存在'
            return render(request, 'register.html', locals())
        if repassword != password:
            comment = '两次密码输入不一致'
            return render(request, 'register.html', locals())
        if len(phonenum) != 11 or not phonenum.isdigit():
            comment = '手机号格式不正确'
            return render(request, 'register.html', locals())

        user = UserInformation.objects.create(username=username, password=get_hashlib(password), phonenum=phonenum)
        request.session['user_id'] = user.id
        return HttpResponseRedirect(reverse('master:index'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('master:index'))

def personal_view(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return HttpResponseRedirect(reverse('user:login'))
    wpoints = WrongQuestion.objects.filter(user_id=user_id, is_active=True).order_by('level_mastery', 'edited_time')

    return render(request, 'personal_center.html', locals())

