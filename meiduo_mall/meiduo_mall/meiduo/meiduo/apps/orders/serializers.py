from decimal import Decimal

from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django_redis import get_redis_connection
from rest_framework import serializers

from carts.serializers import CartSKUSerializer
from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


class OrderSettlementSerializer(serializers.Serializer):
    freight = serializers.DecimalField(label='运费', max_digits=10, decimal_places=2)
    skus = CartSKUSerializer(many=True, read_only=True)


class SaveOrderSerializer(serializers.ModelSerializer):  # 模型类序列化器在反序列化的时候已经映射好了字段验证行为
    # 保存订单的序列化器
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'address', 'pay_method')
        read_only_fields = ('order_id',)
        extra_kwargs = {
            'address': {
                'write_only': True,
                'required': True
            },
            'pay_method': {
                'write_only': True,
                'required': True
            }
        }
    
    def create(self, validated_data):
        """保存订单"""
        # 获取当前下单用户
        user = self.context['request'].user
        
        # 保存订单基本信息 OrderInfo
        # 创建订单编号
        # timezone.now() -> datetime
        order_id = timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        address = validated_data['address']
        pay_method = validated_data['pay_method']
        # 开启事务
        with transaction.atomic():
            # 创建保存点记录当前数据状态
            save_id = transaction.savepoint()
            try:
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal('0'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNSEND'] if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']
                    else OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                )
                
                # 从redis获取购物车数据
                redis_conn = get_redis_connection('cart')
                cart_redis = redis_conn.hgetall('cart_%s' % user.id)
                cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)
                
                cart = {}
                # cart = {
                #     sku_id: count
                #     sku_id: count
                # }
                for sku_id in cart_selected:
                    cart[int(sku_id)] = int(cart_redis[sku_id])
                
                # skus = SKU.objects.filter(id__in=cart.keys())
                # 遍历勾选要下单的商品数据
                for sku_id in cart.keys():
                    # 判断商品库存
                    while True:
                        # sku = SKU.objects.get(id=sku_id)
                        # 解决查询集有缓存特性的问题
                        ret = SKU.objects.filter(id=sku_id, stock__gte=cart[sku_id]).update(
                            stock=F('stock') - cart[sku_id], sales=F('sales') + cart[sku_id])
                        # if sku.stock < cart[sku.id]:
                        # 事务回滚
                        # transaction.savepoint_rollback(save_id)
                        # raise serializers.ValidationError('商品库存不足')
                        
                        # 减少商品库存
                        # sku.stock -= cart[sku.id]
                        # sku.sales += cart[sku.id]
                        # sku.save()
                        
                        # 通过乐观锁解决并发问题
                        # ret = SKU.objects.filter(id=sku.id, stock=sku.stock).update(stock=sku.stock - cart[sku.id],
                        #                                                             sales=sku.sales + cart[sku.id])
                        if ret == 0:
                            # 继续尝试
                            continue
                        
                        sku = SKU.objects.get(id=sku_id)
                        
                        order.total_count += cart[sku.id]
                        order.total_amount += sku.price * cart[sku.id]
                        
                        # 保存到OrderGoods
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count=cart[sku.id],
                            price=sku.price
                        )
                        break
                # 更新订单金额和数量订单数据
                order.save()
            # except serializers.ValidationError as e:
            #     raise e
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                raise e
            
            # 提交事务
            transaction.savepoint_commit(save_id)
            
            # 清除购物车中结算的商品
            pl = redis_conn.pipeline()
            pl.hdel('cart_%s' % user.id, *cart_selected)
            pl.srem('cart_selected_%s' % user.id, *cart_selected)
            
            pl.execute()
            
            return order
