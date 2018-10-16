from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 2
    # 默认每页显示3个，可以通过传入/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大页数不超过10
    max_page_size = 10
    # 获取页码数, 父类默认参数
    # page_query_param = "page"
