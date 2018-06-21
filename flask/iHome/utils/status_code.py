OK = 200
SUCCESS = {'code': 200, 'msg': '请求成功'}

DATABASE_ERROR = {'code':0,'msg':'数据库错误,请稍后重试'}

# 用户模块
USER_REGISTER_DATA_NOT_NULL = {'code': 1001, 'msg': '信息填写不完整，请补全信息'}
USER_REGISTER_MOBILE_ERROR = {'code': 1002, 'msg': '手机号码不正确'}
USER_REGISTER_PASSWORD_IS_NOT_VALID = {'code': 1003, 'msg': '两次密码不一致'}
USER_REGISTER_IS_LOGIN = {'code': 1004, 'msg': '用户已注册, 请直接登录'}

USER_LOGIN_USER_NOT_EXISTS = {'code':1005, 'msg':'用户不存在'}
USER_LOGIN_PASSWORD_IS_NOT_VALID = {'code':1006, 'msg':'用户名或密码错误'}

USER_CHANGE_PROFILE_IMAGE = {'code':1007, 'msg':'上传图片不正确'}
USER_CHANGE_NAME_IS_VALID = {'code':1008, 'msg':'用户名已重复, 请重新输入'}

USER_AUTH_ID_CARD_IS_VALID =  {'code':1009, 'msg':'身份证号不正确, 请重新输入'}

# 订单模块
ORDER_BEGIN_DATA_NOT_NULL = {'code':1100, 'msg':'房屋信息预约不能为空'}
ORDER_BEGIN_START_DATE_GT_END_DATE = {'code':1101, 'msg':'入住时间不能大于结束时间'}