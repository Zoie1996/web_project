from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from drf_haystack.viewsets import HaystackViewSet
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin

from goods.models import SKU
from . import constants
from .serializers import SKUSerializer, SKUIndexSerializer


# Create your views here.


class HotSKUListView(ListCacheResponseMixin, ListAPIView):
	"""
	返回热销数据
	/categories/(?P<category_id>\d+)/hotskus/
	"""
	serializer_class = SKUSerializer
	pagination_class = None
	
	def get_queryset(self):
		category_id = self.kwargs['category_id']
		return SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[
			:constants.HOT_SKUS_COUNT_LIMIT]


class SKUListView(ListAPIView):
	serializer_class = SKUSerializer
	# 通过定义过滤后端来实现过滤行为
	filter_backends = [OrderingFilter]
	ordering_fields = ('create_time', 'price', 'sales')

	def get_queryset(self):
		# 取出类视图对象中的url参数
		category_id = self.kwargs.get('category_id')
		return SKU.objects.filter(category_id=category_id, is_launched=True)


class SKUSearchViewSet(HaystackViewSet):
	"""
	SKU搜索
	"""
	serializer_class = SKUIndexSerializer
	index_models = [SKU]
