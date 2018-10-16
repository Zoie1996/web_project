from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from snippets import views

urlpatterns = [

    url(r'^snippets/$',views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$',views.snippet_detail),

    # 基于类的视图 snippets url
    # url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),

    # url(r'^users/$', views.UserList.as_view(), name='user-list'),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    # 设置根路由
    url(r'^$', views.api_root),
    # 设置代码高亮
    url(r'^snippets/(?P<pk>[0-9]+)/highlighted/$', views.SnippetHighlight.as_view(), name='snippet-highlight'),

    # JWT用户验证路由
    url(r'^api-token-auth/', obtain_jwt_token),

]
# DefaultRouter 类还会自动帮我们创建API根视图，也就是说view.py中的api_root方法也可以删除掉了
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
urlpatterns += router.urls

# format_suffix_patterns格式后缀模式
# urlpatterns = format_suffix_patterns(urlpatterns)
