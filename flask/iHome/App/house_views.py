from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from App.models import Area, Facility, User, House
from utils import status_code
from utils.decoration import is_login

house_blueprint = Blueprint('house', __name__)


@house_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@house_blueprint.route('/my_house/', methods=['GET'])
def my_house():
    return render_template('myhouse.html')


@house_blueprint.route('/show_my_house/', methods=['GET'])
def show_my_house():
    houses = House.query.filter(House.user_id == session['user_id']).all()
    house_list = [house.to_dict() for house in houses]
    return jsonify(code=status_code.OK, houses=house_list)


@house_blueprint.route('/new_house/', methods=['GET'])
@is_login
def new_house():
    return render_template('newhouse.html')


@house_blueprint.route('/new_house/', methods=['POST'])
@is_login
def post_new_house():
    house = House()
    # params = request.form.to_dict()
    house.user_id = session['user_id']
    house.title = request.form.get('title')
    house.price = request.form.get('price')
    house.area_id = request.form.get('area_id')
    house.address = request.form.get('address')
    house.oom_count = request.form.get('room_count')
    house.acreage = request.form.get('acreage')
    house.unit = request.form.get('unit')
    house.capacity = request.form.get('capacity')
    house.beds = request.form.get('beds')
    house.deposit = request.form.get('deposit')
    house.min_days = request.form.get('min_days')
    house.max_days = request.form.get('max_days')
    facility_ids = request.form.getlist('facility')
    # 根据设施的编号查询设施对象
    if facility_ids:
        facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facility_list
    house.add_update()
    return jsonify(status_code.SUCCESS)


@house_blueprint.route('/area_facility/', methods=['GET'])
def area_facility():
    areas = Area.query.all()
    facilitys = Facility.query.all()
    areas_list = [area.to_dict() for area in areas]
    facilitys_list = [facility.to_dict() for facility in facilitys]
    return jsonify(code=status_code.OK, area=areas_list, facility=facilitys_list)
