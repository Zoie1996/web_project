from datetime import datetime

from flask import Blueprint, render_template, request, session, jsonify
from App.models import Order, House
from utils import status_code
from utils.decoration import is_login

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/create_order/', methods=['POST'])
@is_login
def create_order():
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
