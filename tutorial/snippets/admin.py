from django.contrib import admin

from snippets import models


class SnippetAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id', 'title', 'code', 'language')

    # 设置哪些字段可以点击进入编辑界面，默认是第一个字段
    list_display_links = ('id', 'title')



class UserAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id', 'username', 'email','last_login', 'date_joined','first_name', 'last_name')

    list_display_links = ('id', 'username')
    readonly_fields = ['last_login', 'date_joined']
    search_fields = ('username', 'first_name', 'last_name', 'email')
    # style_fields = {'username': 'm2m_transfer','email': 'm2m_transfer'}


admin.site.register(models.Snippet, SnippetAdmin)
admin.site.register(models.User, UserAdmin)
