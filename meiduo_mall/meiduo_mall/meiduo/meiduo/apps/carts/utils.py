import base64
import pickle

from django_redis import get_redis_connection
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import User


def merge_cart_cookie_to_redis(request: Request, response: Response, user: User):
	"""
	合并购物车，将cookie数据保存到redis中
	:param request: 用于从请求中取出cookie
	:param response: 用于从响应中清楚cookie
	:param user: 用于取出用户的redis存储的购物车数据
	:return:
	"""
	# 从cookie中取出购物车数据
	cart_str = request.COOKIES.get('cart')
	if not cart_str:
		return response
	cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
	
	# 从redis中取出购物车数据
	redis_conn = get_redis_connection('cart')
	cart_redis = redis_conn.hgetall('cart_%s' % user.id)
	
	cart = {}
	# {
	# 	sku_id: count,
	# 	sku_id: count
	# }
	for sku_id, count in cart_redis.items():
		cart[int(sku_id)] = int(count)
	
	# 勾选状态列表
	selected_sku_id_list = []
	for sku_id, selected_count_dict in cart_dict.items():
		# 如果redis中原有商品数据，数量覆盖，如果没有，新添
		cart[sku_id] = selected_count_dict['count']
		
		# 处理勾选状态
		if selected_count_dict['selected']:
			selected_sku_id_list.append(sku_id)
		
	# 合并
	pl = redis_conn.pipeline()
	# 将合并后的映射字典数据一次性添加到redis中
	pl.hmset('cart_%s' % user.id, cart)
	
	pl.sadd('cart_selected_%s' % user.id, *selected_sku_id_list)
	
	pl.execute()
	
	# 清楚cookie数据
	response.delete_cookie('cart')
	
	return response