from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.deprecation import MiddlewareMixin

from user.models import UserModel, UserTicketModel


# import logging
# logger = logging.getLogger('console')
# logger.info('获取到cookies中ticket的参数')


class UserAuthMiddle(MiddlewareMixin):

    def process_request(self, request):

        # 需要登录验证, 个人中心和购物车
        need_login = ['/axf/mine/', '/axf/addCart/','/axf/subCart/',
                      '/axf/cart/', '/xaf/change_cart_status/',
                      '/axf/generate_order/', '/axf/total_price/',
                      '/axf/order_list_wait_pay/','/axf/order_list_payed/',
                      '/axf/goods_num/']

        if request.path in need_login:
            # 先获取cookies中的ticket参数
            ticket = request.COOKIES.get('ticket')
            # 如果没有ticket, 跳转到登录
            if not ticket:
                return HttpResponseRedirect(reverse('user:login'))

            user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
            if user_ticket:
                # 获取到认证的相关信息
                # 1. 验证当前认证信息是否过期, 如果没有过期, request.user赋值
                # 2. 如果过期, 跳转到登录, 并删除认证信息
                if user_ticket.out_time.replace(tzinfo=None) < datetime.utcnow():
                    # 过期
                    UserTicketModel.objects.filter(user=user_ticket.user).delete()
                    return HttpResponseRedirect(reverse('user:login'))
                else:
                    # 如果没有过期, 赋值request.user,并删除多余信息
                    request.user = user_ticket.user
                    # 删除多余的认证信息
                    # 从UserTicket中查询当前user,并且删除ticket不等于cookie中的ticket
                    UserTicketModel.objects.filter(Q(user=user_ticket.user) & ~Q(ticket=ticket)).delete()
        else:
            return None

