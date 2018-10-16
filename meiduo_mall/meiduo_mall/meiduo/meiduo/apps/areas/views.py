from django.shortcuts import render
from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from . import models
from . import serializers

# Create your views here.


class AreasViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):  # 省市区添加缓存(对需要经常查询但并不会怎么改变的数据都可以缓存来提升性能)
    """
    list:
    返回所有省份的信息

    retrieve:
    返回特定省或市的下属行政区划
    """
    # queryset = models.Area.objects.all()
    # 关闭分页，后面会在全局开启分页
    pagination_class = None

    def get_queryset(self):
        if self.action == 'list':
            return models.Area.objects.filter(parent=None)

        return models.Area.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AreaSerializer

        return serializers.SubAreaSerializer