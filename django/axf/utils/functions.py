import random


def get_ticket():
    s = 'abcdefghijklmnopqrstvuwxyz1234567890'
    ticket = ''
    for _ in range(28):
        ticket += random.choice(s)
    ticket = 'TK_' + ticket
    return ticket

def get_order_random_id():
    """随机生成订单号"""
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    order_num = ''
    for _ in range(18):
        order_num += random.choice(s)
    return order_num