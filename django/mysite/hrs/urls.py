from django.conf.urls import url
from django.urls import path, re_path

from hrs import views





urlpatterns = [
    path('depts/',views.depts),
    path('delete_dept/<int:dno>',views.delete_dept,name='delete_dept'),
    path('emps/<int:dno>/',views.emps, name='emps')
]
