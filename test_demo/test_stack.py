import unittest

from stack import Stack


class TestClass(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_case01(self):
        """测试推入元素顺序"""
        self.stack.push(1)
        self.stack.push(2)
        self.assertTrue(self.stack.stack_list == [1, 2])

    def test_case02(self):
        """测试是否能推入超出堆栈原本大小"""
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.stack.push(4)
        self.assertTrue(self.stack.size() == self.stack.max_size)
        self.assertTrue(self.stack.stack_list == [1, 2, 3])

    def test_case03(self):
        """测试有元素时推出元素是先进元素还是后进元素"""
        self.stack.push(1)
        self.stack.push(2)
        self.assertTrue(self.stack.pop() == 2)

    def test_case04(self):
        """测试无元素时是否能删除"""
        self.assertFalse(self.stack.pop())

    def test_case05(self):
        """测试是否为空"""
        self.assertTrue(self.stack.is_none())
        self.stack.push(123)
        self.assertFalse(self.stack.is_none())

    def test_case06(self):
        """测试是否为满"""
        self.stack.push(1)
        self.stack.push(2)
        self.assertFalse(self.stack.is_full())
        self.stack.push(3)
        self.assertTrue(self.stack.is_full())

    def test_case07(self):
        """测试大小"""
        self.assertIsNone(self.stack.size())
        self.stack.push(1)
        self.assertTrue(self.stack.size() == 1)


if __name__ == '__main__':
    unittest.main()
