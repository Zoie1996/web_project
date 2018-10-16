from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    使每个Snippet只允许其创建者编辑它
    """

    def has_object_permission(self, request, view, obj):
        # 任何用户或者游客都可以访问任何Snippet，所以当请求动作在安全范围内，
        # 也就是GET，HEAD，OPTIONS请求时，都会被允许
        if request.method in permissions.SAFE_METHODS:
            return True

        # 而当请求不是上面的安全模式的话，那就需要判断一下当前的用户
        # 如果Snippet所有者和当前的用户一致，那就允许，否则返回错误信息
        return obj.owner == request.user
