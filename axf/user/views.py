from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from user.models import UserModel, UserTicketModel
from utils.functions import get_ticket


def register(request):
    """
    注册
    :param request:
    :return: 注册成功返回登录页面,注册不成功返回注册页面
    """
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repwd = request.POST.get('repwd')
        icon = request.FILES.get('icon')
        # 需要验证参数都不为空
        if not all([username, email, password, icon]):
            # 验证不通过,提示参数不能为空,返回页面提示信息
            msg = '请填写完整信息'
            return render(request, 'user/user_register.html', {'msg': msg})
        if password != repwd:
            msg = '两次输入密码不一致'
            return render(request, 'user/user_register.html', {'msg': msg})

        # 加密password
        password = make_password(password)
        UserModel.objects.create(username=username,
                                 password=password,
                                 email=email,
                                 icon=icon)

        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证用户是否存在
        user = UserModel.objects.filter(username=username).first()
        if user:
            # 验证密码是否正确
            if check_password(password, user.password):
                # 1. 保存ticket在客户端
                ticket = get_ticket()
                response = HttpResponseRedirect(reverse('axf:mine'))
                out_time = datetime.now() + timedelta(days=14)
                response.set_cookie('ticket', ticket, expires=out_time)

                # 2. 保存ticket在服务端user_ticket表中
                UserTicketModel.objects.create(user_id=user.id, ticket=ticket, out_time=out_time)



                # user_ticket = UserTicketModel.objects.filter(user_id=user.id).first()
                # if user_ticket:
                #     user_ticket.out_time = out_time
                #     user_ticket.ticket = ticket
                #     user_ticket.save()
                # else:
                #     UserTicketModel.objects.create(user_id=user.id, ticket=ticket, out_time=out_time)

                return response
            else:
                msg = '用户名或密码错误'
                return render(request, 'user/user_login.html', {'msg': msg})
        else:
            msg = '用户不存在'
            return render(request, 'user/user_login.html', {'msg': msg})


def logout(request):
    """
    注销
    :param request:
    :return: 返回登录页面
    """
    if request.method == 'GET':

        # 注销,删除当前登录的用户的cookies中的ticket信息
        response = HttpResponseRedirect(reverse('user:login'))
        response.delete_cookie('ticket')
        return response
