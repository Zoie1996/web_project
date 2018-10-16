import os

from alipay import AliPay
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import OrderInfo
from .models import Payment


# Create your views here.


class PaymentView(APIView):
    """
    支付宝支付
    /orders/(?P<order_id>\d+)/payment/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request, order_id):
        user = request.user
        
        # 校验订单号
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return Response({'message': '订单信息有误'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 根据订单数据向支付宝发起请求，获取支付链接参数
        alipay_client = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/app_private_key.pem'),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                'keys/alipay_public_key.pem'),
            sign_type='RSA2',
            debug=settings.ALIPAY_DEBUG
        )
        
        # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do？+order_string
        order_string = alipay_client.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject='美多商城%s' % order_id,
            return_url="http://www.meiduo.site:8080/pay_success.html"
        )
        
        alipay_url = settings.ALIPAY_URL + '?' + order_string
        
        return Response({'alipay_url': alipay_url}, status=status.HTTP_201_CREATED)


class PaymentStatusView(APIView):
    """
    修改支付结果状态
    """
    
    def put(self, request: Request):
        # 取出请求的参数
        query_dict = request.query_params
        data = query_dict.dict()
        sign = data.pop('sign')
        
        alipay_client = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/app_private_key.pem'),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                'keys/alipay_public_key.pem'),
            sign_type='RSA2',
            debug=settings.ALIPAY_DEBUG
        )
        ret = alipay_client.verify(data, sign)
        if not ret:
            return Response({'message': '非法请求'}, status=status.HTTP_403_FORBIDDEN)
        
        # 保存支付数据
        # 修改订单数据
        order_id = data.get('out_trade_no')
        trade_id = data.get('trade_no')
        Payment.objects.create(
            order_id=order_id,
            trade_id=trade_id
        )
        OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
            status=OrderInfo.ORDER_STATUS_ENUM['UNSEND'])
        
        return Response({'trade_id': trade_id})