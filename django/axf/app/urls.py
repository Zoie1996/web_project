from django.conf.urls import url

from app import views

urlpatterns = [
    # 首页
    url(r'^home/', views.home, name='home'),
    # 个人中心
    url(r'^mine/', views.mine, name='mine'),
    # 闪购超市
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.user_market, name='market_params'),
    # 闪购页面商品数量数据
    url(r'^goods_num/$', views.goods_num, name='goods_num'),
    # 添加购物车
    url(r'^addCart/', views.add_Cart, name='addCart'),
    url(r'^subCart/', views.sub_Cart, name='subCart'),
    # 购物车页面
    url(r'^cart/', views.cart, name='cart'),
    # 修改购物车车中商品的状态
    url(r'^change_cart_status/', views.change_cart_status, name='change_cart_status'),
    # 全选/全不选
    url(r'select_all/', views.select_all, name='select_all'),
    # 下单
    url(r'^generate_order/', views.generate_order, name='generate_order'),
    # 总价
    url(r'^total_price/', views.total_price, name='total_price'),
    # 修改订单状态
    url(r'^change_order_status/',views.change_order_status, name='change_order_status'),
    # 已付款
    url(r'^order_list_payed/', views.order_list_payed, name='order_list_payed'),
    # 待支付
    url(r'^order_list_wait_pay/', views.order_list_wait_pay, name='order_list_wait_pay'),
    # 待付款订单支付
    url(r'^waitPayToPay/', views.wait_pay_to_pay, name='wait_pay_to_pay')

]




