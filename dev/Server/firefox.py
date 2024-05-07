import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import subprocess
from subprocess import Popen, PIPE

from dev.Refactor.functions import formatDate


def main():
    # 创建浏览器实例
    driver = webdriver.Firefox()

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

    time.sleep(1)

    # 在关闭浏览器之前获取页面内容
    page_content = driver.page_source
    print("当前页面内容：", page_content)
    if '认证成功' in page_content:
        print('认证成功', formatDate('yyyy-MM-dd HH:mm:ss', time.time() * 1000))
        # 关闭浏览器
        driver.quit()

        # 密码
        sudo_password = "997975"

        # 创建一个子进程，并与其进行交互
        process = Popen(['sudo', '-S', 'pkill', '-f', 'ToDesk'], stdin=PIPE, stdout=PIPE, stderr=PIPE,
            universal_newlines=True)

        # 向子进程发送密码
        process.stdin.write(sudo_password + '\n')
        process.stdin.flush()

        # 获取输出
        output, err = process.communicate()

        # 打印输出
        # print("输出：", output)
        # print("错误：", err)

        time.sleep(2)

        # 打开应用程序
        subprocess.call(["open", "-n", "/Applications/ToDesk.app"])

        time.sleep(1800)
        main()
    else:
        main()


if __name__ == '__main__':
    main()
