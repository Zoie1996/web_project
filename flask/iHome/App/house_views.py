import os
import re

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from App.models import Area, Facility, House, HouseImage
from utils import status_code
from utils.decoration import is_login
from utils.setting import UPLOAD_DIR

house_blueprint = Blueprint('house', __name__)


@house_blueprint.route('/', methods=['GET'])
def index():
    """显示首页信息"""
    return render_template('index.html')


@house_blueprint.route('/my_house/', methods=['GET'])
@is_login
def my_house():
    """显示我的房源页面"""
    return render_template('myhouse.html')


@house_blueprint.route('/show_my_house/', methods=['GET'])
def show_my_house():
    """显示房屋信息"""
    houses = House.query.filter(House.user_id == session['user_id']).all()
    house_list = [house.to_dict() for house in houses]
    return jsonify(code=status_code.OK, houses=house_list)


@house_blueprint.route('/area_facility/', methods=['GET'])
@is_login
def area_facility():
    """显示发布新房源页面区域及设施信息"""
    areas = Area.query.all()
    facilitys = Facility.query.all()
    areas_list = [area.to_dict() for area in areas]
    facilitys_list = [facility.to_dict() for facility in facilitys]
    return jsonify(code=status_code.OK, area=areas_list, facility=facilitys_list)


@house_blueprint.route('/new_house/', methods=['GET'])
@is_login
def new_house():
    """显示发布新房源页面"""
    return render_template('newhouse.html')


@house_blueprint.route('/new_house/', methods=['POST'])
@is_login
def post_new_house():
    """保存发布的房源信息"""
    house = House()
    data = request.form.to_dict()
    house.user_id = session['user_id']
    house.title = data.get('title')
    house.price = data.get('price')
    house.area_id = data.get('area_id')
    house.address = data.get('address')
    house.oom_count = data.get('room_count')
    house.acreage = data.get('acreage')
    house.unit = data.get('unit')
    house.capacity = data.get('capacity')
    house.beds = data.get('beds')
    house.deposit = data.get('deposit')
    house.min_days = data.get('min_days')
    house.max_days = data.get('max_days')
    facility_ids = request.form.getlist('facility')
    # 根据设施的编号查询设施对象
    if facility_ids:
        facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facility_list
    house.add_update()
    return jsonify(code=status_code.OK, house_id=house.id)


@house_blueprint.route('/new_house_image/<int:house_id>/', methods=['POST'])
@is_login
def new_house_image(house_id):
    """保存新房源图片"""
    house_image = request.files.get('house_image')
    # 保存图片路径到本地
    if not re.match(r'image/.*', house_image.mimetype):
        return jsonify(status_code.USER_CHANGE_PROFILE_IMAGE)
    save_url = os.path.join(UPLOAD_DIR, house_image.filename)
    house_image.save(save_url)
    # 保存房屋图片信息数据库
    image_url = os.path.join('upload', house_image.filename)
    h_image = HouseImage()
    h_image.house_id = house_id
    h_image.url = image_url
    h_image.add_update()
    # 保存房屋首图
    house = House.query.get(house_id)
    # 判断首页展示图片是否存在,如果不存在则添加第一张图片为首页图片
    if not house.index_image_url:
        house.index_image_url = image_url
        house.add_update()
    return jsonify({'code': status_code.OK, 'image_url': image_url})


@house_blueprint.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@house_blueprint.route('/detail/<int:house_id>/', methods=['GET'])
def house_detail(house_id):
    house = House.query.get(house_id)
    house_info = house.to_full_dict()
    return jsonify(code=status_code.OK, house_info=house_info)


@house_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')
