# from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

from snippets.models import Snippet, User
from snippets.pagination import MyPageNumberPagination
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework_jwt.views import obtain_jwt_token

"""     Snippet使用通用视图类     """


class SnippetList(generics.ListCreateAPIView):
    """
    片段展示
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # 当前用户是否为该Snippet的创建者，其他用户只有只读属性（注意，结尾的逗号一定要加上去）
    # 此处权限高于setting.py 权限
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # 设置智能登录后才能访问，setting.py 内统一设置后，此处不必再写
    # permission_classes = (permissions.IsAuthenticated,)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


"""     自定义实现分页功能      """

# class SnippetPageList(APIView):
# permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
# 自定义分页
# def get(self, request, *args, **kwargs):
#     # 获取所有数据
#     snippets = Snippet.objects.all()
#     # 创建分页对象
#     pg = MyPageNumberPagination()
#     # 获取分页的数据
#     page_snippets = pg.paginate_queryset(queryset=snippets, request=request, view=self)
#     # 对数据进行序列化
#     ser = SnippetSerializer(instance=page_snippets, many=True)
#     return Response(ser.data)


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


"""       使用ViewSets重构视图      """
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    viewset自动提供了list和detail动作
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers


# 为API创建根URL
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


# 代码高亮
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    列出所有已经存在的snippet或者创建一个新的snippet
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    检索，更新或者删除一个实列
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''

@csrf_exempt
def snippet_list(request):
    """
    列出所有已经存在的snippet或者创建一个新的snippet
    :param request:
    :return: 返回json数据
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        # 当输入参数many = True时, serializer还能序列化queryset
        serializer = SnippetSerializer(snippets, many=True)
        # 第一个参数，data应该是一个字典类型，当safe=False ,那data可以填入任何能被转换为JSON格式的对象，比如list, tuple, set。 默认的safe=True. 如果你传入的data数据类型不是字典类型，那么它就会抛出TypeError的异常。
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
'''
