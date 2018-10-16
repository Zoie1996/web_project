from rest_framework.pagination import PageNumberPagination


class StandardPageNumPagination(PageNumberPagination):
    """如果前端没有传递分页参数，按照分页类指定的参数设置"""
    page_size = 5
    # 指明前端传来的查询字符串中的page——size数量
    page_size_query_param = 'page_size'
    # 前端请求的每页数量上限
    max_page_size = 20