from django.shortcuts import render,redirect

# Create your views here.
from hrs.models import Dept, Emp


def index(req):
    return render(req, 'index.html', context={'greeting':'你好,世界'})

def depts(req):
    # DRY - Don't Repeat Yourself
    # 获取模型对象 Dept.objects.all()
    ctx = {'dept_list': Dept.objects.all()}
    return render(req,'depts.html', context=ctx)


def emps(req, dno):

    ctx = {'emp_list': Emp.objects.filter(dept__no=dno)}
    return render(req, 'emps.html', context=ctx)


def delete_dept(req, dno):

    emp = Emp.objects.filter(dept__no=dno)
    if not emp:
        Dept.objects.get(no=dno).delete()
    return redirect('/hrs/depts' )

