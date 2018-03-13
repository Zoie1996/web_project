class Stack(object):
    """堆栈"""

    def __init__(self):
        self.max_size = 3
        self.stack_list = []

    def size(self):
        """元素大小"""
        return len(self.stack_list)

    def push(self, temp):
        """添加元素"""
        if self.size() < self.max_size:
            self.stack_list.append(temp)
        else:
            pass

    def pop(self):
        """推出元素"""
        if self.size() > 0:
            return self.stack_list.pop()
        else:
            # raise Exception('没有元素可删除')
            return False

    def is_none(self):
        """是否为空"""
        if self.size() == 0:
            return True
        else:
            return False

    def is_full(self):
        """是否为满"""
        if self.size() == self.max_size:
            return True
        else:
            return False
