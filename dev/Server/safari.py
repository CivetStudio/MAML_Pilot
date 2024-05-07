import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def main():
    # 创建浏览器实例
    driver = webdriver.Safari('/usr/bin/safaridriver')

    # 打开登录页面
    driver.get('http://192.168.0.1/noAuth/user_auth.html')

    # 查找用户名和密码输入框，并输入相应内容
    username_input = driver.find_element(By.NAME, 'userName')
    password_input = driver.find_element(By.NAME, 'userPasswd')

    username_input.send_keys('vgoing')
    password_input.send_keys('1122334455')

    # 点击登录按钮
    login_btn = driver.find_element(By.ID, 'login_btn')
    login_btn.click()

    # 关闭浏览器
    driver.quit()
    time.sleep(10)
    main()


if __name__ == '__main__':
    main()
