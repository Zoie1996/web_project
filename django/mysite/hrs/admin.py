from django.contrib import admin

# Register your models here.
from hrs.models import Dept, Emp

# 管理员页面显示
class DeptAdmin(admin.ModelAdmin):

    list_display = ('no', 'name','excellent', 'location')
    ordering = ('no',) # 升序  '-no' 降序


class EmpAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'job', 'sal', 'dept')
    search_fields = ('name', 'job')
    ordering = ('no',)


# 导入模型
admin.site.register(Dept, DeptAdmin)
admin.site.register(Emp, EmpAdmin)
