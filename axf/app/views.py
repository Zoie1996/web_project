from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render

from app.models import MainWheel, MainNav, MainMustBuy, MainShow, \
    MainShop, Goods, FoodType, CartModel, OrderModel, OrderGoodsModel
from user.models import UserTicketModel
from utils.functions import get_order_random_id


def home(request):
    """
    首页视图函数
    """
    if request.method == 'GET':
        mainwheels = MainWheel.objects.all()
        mainNavs = MainNav.objects.all()
        mainMustBuys = MainMustBuy.objects.all()
        mainShops = MainShop.objects.all()
        mainShows = MainShow.objects.all()
        data = {
            'title': '首页',
            'mainwheels': mainwheels,
            'mainNavs': mainNavs,
            'mainMustBuys': mainMustBuys,
            'mainShops': mainShops,
            'mainShows': mainShows,
        }
        return render(request, 'home/home.html', data)


def mine(request):
    """
    个人中心
    """
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user)
        # 待支付和待收货状态
        payed, wait_pay = 0, 0
        for order in orders:
            if order.o_status == 0:
                wait_pay += 1
            if order.o_status == 1:
                payed += 1
        data = {
            'wait_pay': wait_pay,
            'payed': payed,
        }
        return render(request, 'mine/mine.html', data)


def market(request):
    """
    闪购超市
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('axf:market_params', args=('104749', '0', '0')))


def user_market(requset, typeid, cid, sid):
    """
    :param typeid: 分类id
    :param cid: 子分类id
    :param sid: 排序id
    """
    if requset.method == 'GET':
        ticket = requset.COOKIES.get('ticket')
        user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
        if user_ticket:
            user = user_ticket.user
        else:
            user = ''
        if user:
            user_cart = CartModel.objects.filter(user=user)
        else:
            user_cart = ''

        # 闪购--左侧类型表
        foodtypes = FoodType.objects.all()
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid, childcid=cid)

        # 处理子分类
        foodtypes_current = FoodType.objects.filter(typeid=typeid).first()

        # 切片子分类与分类编号
        child_list = []
        if foodtypes_current:
            childtypes = foodtypes_current.childtypenames
            childtypenames = childtypes.split('#')
            for child in childtypenames:
                child_list.append(child.split(':'))

        # 排序
        if sid == '0':
            pass
        if sid == '1':
            goods = goods.order_by('productnum')
        if sid == '2':
            goods = goods.order_by('-price')
        if sid == '3':
            goods = goods.order_by('price')

        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'child_list': child_list,
            'cid': cid,
            'user_cart': user_cart,
        }
        return render(requset, 'market/market.html', data)


def add_Cart(request):
    """
    添加购物车
    """
    if request.method == 'POST':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        user = request.user
        goods_id = request.POST.get('goods_id')
        # 判断用户是否是系统自带的用户还是登陆的用户
        if user.id:
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if user_carts:
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                CartModel.objects.create(user=user, goods_id=goods_id)
                data['c_num'] = 1
            return JsonResponse(data)
        data['code'] = 403
        data['msg'] = '当前用户没有登录, 请登录'
        return JsonResponse(data)


def sub_Cart(request):
    """
    减少购物车用户下单商品数量
    """
    if request.method == 'POST':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        user = request.user

        goods_id = request.POST.get('goods_id')
        # 判断用户是否是系统自带的用户还是登陆的用户
        if user.id:
            # 获取用户下单对应的商品信息
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()

            # 如果购物车中已存在了商品信息
            if user_carts:
                if user_carts.c_num == 1:
                    data['c_num'] = 0
                    user_carts.delete()
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
                return JsonResponse(data)
            data['c_num'] = 0
            return JsonResponse(data)
        data['code'] = 403
        data['msg'] = '当前用户没有登录, 请登录'
        return JsonResponse(data)


def goods_num(request):
    """
    显示闪购页面商品数量数据
    """
    if request.method == 'GET':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        user = request.user
        user_carts = CartModel.objects.filter(user=user)
        source = []
        for cart in user_carts:
            goods_num = cart.c_num
            goods_id = cart.goods_id
            source.append({goods_id: goods_num})
        data['data'] = source

        return JsonResponse(data)


def cart(request):
    """
    购物车
    """
    if request.method == 'GET':
        # 获取用户信息
        user = request.user
        user_cart = CartModel.objects.filter(user=user)
        data = {'user_cart': user_cart}
        return render(request, 'cart/cart.html', data)


def change_cart_status(request):
    """
    更改商品的选择状态
    """
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.filter(id=cart_id).first()
        if cart.is_select:
            cart.is_select = False
        else:
            cart.is_select = True
        cart.save()
        data = {
            'code': 200,
            'msg': '请求成功',
            'is_select': cart.is_select,
        }
        return JsonResponse(data)


def select_all(request):
    """
    全选中/全不选
    """
    if request.method == 'GET':
        action = request.GET.get('action')
        # 全选
        if action == 'select':
            carts = CartModel.objects.filter(is_select=False)
            for cart in carts:
                cart.is_select = True
                cart.save()
        if action == 'unselect':
            carts = CartModel.objects.filter(is_select=True)
            for cart in carts:
                cart.is_select = False
                cart.save()
        data = {
            'code': 200,
            'msg': '请求成功',
        }
        return JsonResponse(data)


def generate_order(request):
    """
    下单
    """
    if request.method == 'GET':
        user = request.user
        # 创建订单
        o_num = get_order_random_id()
        order = OrderModel.objects.create(user=user, o_num=o_num)

        # 选择勾选的商品进行下单
        user_carts = CartModel.objects.filter(user=user, is_select=True)
        for cart in user_carts:
            # 创建商品和订单之间的关系
            OrderGoodsModel.objects.create(goods=cart.goods, order=order, goods_num=cart.c_num)
        # 电机订单之后删除购物车内商品
        user_carts.delete()
        return render(request, 'order/order_info.html', {'order': order})


def change_order_status(request):
    """
    修改订单状态
    """
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        OrderModel.objects.filter(id=order_id).update(o_status=1)
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def order_list_payed(request):
    """
    显示待发货页面
    """
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=1)
        data = {
            'orders': orders
        }
        return render(request, 'order/order_list_payed.html', data)


def order_list_wait_pay(request):
    """
    显示待付款页面
    """
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=0)
        data = {
            'orders': orders
        }
        return render(request, 'order/order_list_wait_pay.html', data)


def wait_pay_to_pay(request):
    """
    待付款页面支付
    """
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order = OrderModel.objects.filter(id=order_id).first()
        return render(request, 'order/order_info.html', {'order': order})


def total_price(request):
    """
    购物车商品总价
    """

    if request.method == 'GET':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        user = request.user
        user_carts = CartModel.objects.filter(user=user, is_select=1)
        source = []
        for cart in user_carts:
            goods_num = cart.c_num
            goods_price = cart.goods.price
            source.append({'goods_price': goods_price,
                           'goods_num': goods_num})
        data['data'] = source
        return JsonResponse(data)
