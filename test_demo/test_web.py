from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class NewVisitorTest(unittest.TestCase):
    """
    自动化测试是否登录百度
    """

    def setUp(self):
        self.timeout = 40 # 等待时间
        self.browser = webdriver.Chrome() # 浏览器对象
        self.browser.set_page_load_timeout(self.timeout) # 超时时间
        self.wait = WebDriverWait(self.browser, self.timeout)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 获取百度链接
        self.browser.get('https://www.baidu.com')
        # 判断是否能打开百度链接
        self.assertIn('百度', self.browser.title)
        # 点击登录
        login_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, '登录')))
        login_link.click()
        # 点击用户名登录
        login_link_2 = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'TANGRAM__PSP_10__footerULoginBtn')))
        login_link_2.click()
        # 输入用户名
        username_input = self.wait.until(
            EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_10__userName')))
        # 清空输入框
        username_input.clear()
        # 输入你的百度账号
        username_input.send_keys('username')
        # 输入密码
        password_input = self.wait.until(
            EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_10__password')))
        # 清空输入框
        password_input.clear()
        # 输入你的密码
        password_input.send_keys('password')
        # 点击登录按钮
        login_submit_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'TANGRAM__PSP_10__submit')))
        login_submit_button.click()
        # 获取已登录页面的用户名
        username_span = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#s_username_top > span')))
        # 如果用户名与输入的用户名相等，则已登录
        self.assertEqual(username_span.text, 'username')

    # user_login_link = self.browser.find_element_by_id('TANGRAM__PSP_10__footerULoginBtn')
    # user_login_link.click()


if __name__ == '__main__':
    unittest.main(warnings='ignore')
