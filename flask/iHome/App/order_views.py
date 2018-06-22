from datetime import datetime

from flask import Blueprint, render_template, request, session, jsonify
from App.models import Order, House
from utils import status_code
from utils.decoration import is_login

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/create_order/', methods=['POST'])
@is_login
def create_order():
    """创建订单"""
    start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    house_id = request.form.get('house_id')
    user_id = session['user_id']
    if not all([start_date, end_date, house_id, user_id]):
        return jsonify(status_code.ORDER_BEGIN_DATA_NOT_NULL)
    if start_date > end_date:
        return jsonify(status_code.ORDER_BEGIN_START_DATE_GT_END_DATE)

    order = Order()
    order.user_id = user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = (end_date - start_date).days + 1

    house = House.query.get(house_id)
    order.house_price = house.price
    order.amount = order.days * order.house_price
    order.add_update()
    return jsonify(status_code.SUCCESS)


@order_blueprint.route('/orders/')
@is_login
def orders():
    """返回我的订单页面"""
    return render_template('orders.html')


@order_blueprint.route('/allorders/', methods=['GET'])
@is_login
def all_orders():
    """作为租客查询订单"""
    user_id = session['user_id']
    orders = Order.query.filter(Order.user_id == user_id).order_by(Order.id.desc())
    order_list = [order.to_dict() for order in orders]
    return jsonify(code=status_code.OK, order_list=order_list)


@order_blueprint.route('/lorders/', methods=['GET'])
@is_login
def lorders():
    """返回客户订单页面"""
    return render_template('lorders.html')


@order_blueprint.route('/client_orders/', methods=['GET'])
@is_login
def client_orders():
    # 通过用户id查询用户发布的房屋
    houses = House.query.filter(House.user_id == session['user_id']).all()
    # 获取房屋id
    house_id_list = [house.id for house in houses]
    # 通过房屋id获取客户订单
    orders = Order.query.filter(Order.house_id.in_(house_id_list)).all()
    order_list = [order.to_dict() for order in orders]
    return jsonify(code=status_code.OK, order_list=order_list)


@order_blueprint.route('/order_accept/<int:order_id>/', methods=['PUT'])
@is_login
def order_accept(order_id):
    order = Order.query.get(order_id)
    order.status = "WAIT_PAYMENT"
    order.add_update()
    houses = House.query.filter(House.user_id == session['user_id']).all()
    house_id_list = [house.id for house in houses]
    orders = Order.query.filter(Order.house_id.in_(house_id_list)).all()
    order_list = [order.to_dict() for order in orders]
    return jsonify(code=status_code.OK, order_list=order_list)

@order_blueprint.route('/order_operate/<int:order_id>/', methods=['PATCH'])
@is_login
def order_operate(order_id):
    operate = request.form.get('operate')
    order = Order.query.get(order_id)
    # 已接单,待支付
    if operate == 'accept':
        order.status = "WAIT_PAYMENT"
    # 已拒单
    elif operate == 'reject':
        order.status = "REJECTED"
        order.comment = request.form.get('comment')
    order.add_update()
    return jsonify(status_code.SUCCESS)

@order_blueprint.route('/search/', methods=['GET'])
@is_login
def search():
    return render_template('search.html')


