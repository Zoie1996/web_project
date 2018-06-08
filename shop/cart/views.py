from json import dumps

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

from cart.models import Goods


def index(request):
    goods_list = list(Goods.objects.all())
    return render(request, 'goods.html', {'goods_list': goods_list})


class CartItem(object):
    """购物车项"""

    def __init__(self, no, goods, amount=1):
        """
        :param no: 编号
        :param goods: 商品
        :param amount: 数量
        """
        self.no = no
        self.goods = goods
        self.amount = amount

    @property
    def total(self):
        """单项商品小计"""
        return self.goods.price * self.amount


class ShoppingCart(object):
    """购物车"""

    def __init__(self):
        self.num = 0
        self.items = {}

    def add_item(self, item):
        """添加商品"""
        if item.goods.id in self.items:
            self.items[item.goods.id].amount += item.amount
        else:
            self.items[item.goods.id] = item

    def remove_item(self, id):
        """移除商品"""
        if id in self.items:
            self.items.pop(id)

    def clear_items(self):
        """清空购物车"""
        self.items.clear()

    @property
    def cart_items(self):
        return self.items.values()

    @property
    def total(self):
        """商品总计"""
        val = 0
        for item in self.items.values():
            val += item.total
        return val


# 添加到购物车
def add_to_cart(request, id):

    # 通过请求对象的session属性可以获取到session
    # session相当于是服务器DAU你用来保存用户数据的一个字典
    # session利用了Cookie保存sessionid, 通过sessionid就可以保存用户会话
    # 如果在浏览器中清除了Cookie也就清除了sessionid
    # 再次访问服务器是服务器会重新分配sessionid 这也就意味着之前的用户数据无
    # 默认情况下Django的session被设定为持久会话而非浏览器续存期会话
    # SESSION_COOKIE_AGE = 1209600  Session的cookie失效日期（2周）
    # SESSION_EXPIRE_AT_BROWSER_CLOSE 是否每次请求都保存Session，默认修改之后才保存
    # Django中的session死进行了持久化处理的 因此需要设定session的序列化方式
    # 1.6版开始 Django默认的session序列化是JSONSerializer
    # 可以通过SESSION_SERIALIZER来设定其他的序列化器(例如PickleSerializer)
    '''
    # 查询商品
    goods = Goods.objects.get(pk=id)
    # 购物车 拿到则返回 拿不到创建一个新的购物车
    cart = request.session.get('cart', ShoppingCart())
    # 添加商品项
    cart.add_item(CartItem(id, goods))
    # 把cart回写session
    request.session['cart'] = cart
    # 返回首页
    return redirect('/')
    '''

    # ajax
    goods = Goods.objects.get(pk=id)
    cart = request.session.get('cart', ShoppingCart())
    cart.add_item(CartItem(id, goods))
    request.session['cart'] = cart
    ctx = {'code': 200}
    return HttpResponse(dumps(ctx), content_type='application/json; charset=utf-8')



def delete_to_cart(request, id):
    # cart = request.session.get('cart')
    # cart.remove_item(id)
    # request.session['cart'] = cart
    # return redirect('/show_cart')

    # ajax删除购物车项
    try:
        cart = request.session.get('cart')
        cart.remove_item(id)
        ctx = {'code': 200, 'total': str(cart.total)}
        request.session['cart'] = cart
    except:
        ctx = {'code': 400}
    return HttpResponse(dumps(ctx), content_type='application/json; charset=utf-8')


def clear_cart(request):
    # cart = request.session.get('cart')
    # cart.clear_items()
    # request.session['cart'] = cart
    # return redirect('/show_cart')

    # ajax清空购物车
    try:
        cart = request.session.get('cart')
        cart.clear_items()
        request.session['cart'] = cart
        ctx = {'code': 200}
    except:
        ctx = {'code': 400}
    return HttpResponse(dumps(ctx), content_type='application/json; charset=utf-8')


def show_cart(request):
    # 获取购物车
    cart = request.session.get('cart', None)
    # 如果没有拿到cart 返回空列表

    return render(request, 'cart.html', {'cart': cart})
