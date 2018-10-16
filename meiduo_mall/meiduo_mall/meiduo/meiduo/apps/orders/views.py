from decimal import Decimal

from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from goods.models import SKU
from . import serializers


class OrderSettlementView(APIView):
    """
    订单结算
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request):
        """
        获取
        :param request:
        :return:
        """
        user = request.user
        
        # 从购物车中获取用户勾选要结算的商品信息
        redis_conn = get_redis_connection('cart')
        redis_cart = redis_conn.hgetall('cart_%s' % user.id)
        cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)
        
        cart = {}
        for sku_id in cart_selected:
            # 取出勾选的购物车数据以及数量
            # cart = {sku_id: count}
            cart[int(sku_id)] = int(redis_cart[sku_id])
        
        # 查询所有勾选的商品信息
        skus = SKU.objects.filter(id__in=cart.keys())
        for sku in skus:
            sku.count = cart[sku.id]
            sku.selected = True
        
        # 运费
        freight = Decimal('10.00')
        
        serializer = serializers.OrderSettlementSerializer({'freight': freight, 'skus': skus})
        
        return Response(serializer.data)


class SaveOrderView(CreateAPIView):
    # 保存订单
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.SaveOrderSerializer