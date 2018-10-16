import xadmin
from xadmin.plugins import auth

from .models import User


# Register your models here.


class UserAdmin(auth.UserAdmin):
    # 修改用户模型样式
    list_display = ['id', 'username', 'mobile', 'email', 'date_joined']
    readonly_fields = ['last_login', 'date_joined']
    search_fields = ('username', 'first_name', 'last_name', 'email', 'mobile')
    style_fields = {'user_permissions': 'm2m_transfer', 'groups': 'm2m_transfer'}

    def get_model_form(self, **kwargs):
        # org_obj代表原始user对象
        if self.org_obj is None:
            # 新增，添加用户表单（扩展字段，不然无法通过后台创建用户）
            self.fields = ['username', 'mobile', 'is_staff']

        return super().get_model_form(**kwargs)


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)