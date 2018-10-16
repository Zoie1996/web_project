import base64
import pickle

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from users.models import User
from .serializers import CartSKUSerializer
from .serializers import CartSerializer, CartDeleteSerializer


class CartView(APIView):
    """
    购物车
    """
    def perform_authentication(self, request):
        # APIView所有子类在dispatch分发前都会进行身份认证、权限校验和流量控制
        # 这里无论前端是否携带JWT，一致通过
        pass

    def post(self, request: Request):
        """
        保存购物车数据
        :param request:
        :return:
        """
        # 检查前端发送的数据是否正确
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']
        selected = serializer.validated_data['selected']

        # 判断用户是否登录
        try:
            # 在这里对jwt进行验证
            user = request.user  # type: User
        except Exception:
            # 前端携带错误的JWT， 判定用户未登录
            user = None

        # 保存购物车数据
        if user and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()
            pl.hincrby('cart_%s' % user.id, sku_id, count)

            if selected:
                pl.sadd('cart_selected_%s' % user.id, sku_id)

            pl.execute()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            # 用户未登录，保存到cookie中
            cart_str = request.COOKIES.get('cart')

            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}

            # 如果有相同商品，求和
            if sku_id in cart_dict:
                origin_count = cart_dict[sku_id]['count']
                count += origin_count
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }

            cart_cookie = base64.b64encode(pickle.dumps(cart_dict)).decode()

            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response.set_cookie('cart', cart_cookie)

            return response

    def get(self, request: Request):
        # 查询购物车数据
        # 判断用户是否登录
        try:
            user = request.user
        except Exception:
            user = None

        if user and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            redis_cart = redis_conn.hgetall('cart_%s' % user.id)
            cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)
            # 将redis数据整合形成一个字段，与cookie中解读的一致
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected
                }
        else:
            # 用户未登录
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}

        skus = SKU.objects.filter(id__in=cart_dict.keys())
        # 将count和selected添加进sku对象中
        for sku in skus:
            sku.count = cart_dict[sku.id]['count']
            sku.selected = cart_dict[sku.id]['selected']

        serializer = CartSKUSerializer(skus, many=True)

        return Response(serializer.data)

    def put(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 修改购物车数据
        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']
        selected = serializer.validated_data['selected']

        try:
            user = request.user
        except Exception:
            user = None
        if user and user.is_authenticated:
            # 如果用户登录，修改redis数据
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()
            pl.hset('cart_%s' % user.id, sku_id, count)
            if selected:
                # 勾选增加记录
                pl.sadd('cart_selected_%s' % user.id, sku_id)
            else:
                pl.srem('cart_selected_%s' % user.id, sku_id)
            pl.execute()

            return Response(serializer.data)
        else:
            # 未登录，修改cookie数据
            cart_str = request.COOKIES.get('cart')

            if cart_str:
                cart_dict = pickle.loads(base64.b64decode((cart_str.encode())))
            else:
                cart_dict = {}
            if sku_id in cart_dict:
                cart_dict[sku_id] = {
                    'count': count,
                    'selected': selected
                }

            cart_cookie = base64.b64encode(pickle.dumps(cart_dict)).decode()

            response = Response(serializer.data)
            response.set_cookie('cart', cart_cookie)

            return response

    def delete(self, request: Request):
        """
        删除购物车数据
        :param request:
        :return:
        """
        serializer = CartDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sku_id = serializer.validated_data['sku_id']

        try:
            user = request.user
        except Exception:
            user = None
        
        if user and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()
            pl.hdel('cart_%s' % user.id, sku_id)
            pl.srem('cart_selected_%s' % user.id, sku_id)
            pl.execute()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}

            response = Response(serializer.data)
            if sku_id in cart_dict:
                # 删除字典的键值对
                del cart_dict[sku_id]
                
                cart_cookie = base64.b64encode(pickle.dumps(cart_dict)).decode()
                response.set_cookie('cart', cart_cookie)
            
            return response
