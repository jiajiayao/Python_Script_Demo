# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

#reload(sys);
#sys.setdefaultencoding("utf8");

# 设置用户名密码
username = '15156019782'
password = '924915ge'
# 声明浏览器
# browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
browser = webdriver.Chrome()

# brower.get('http://moocs.unipus.cn/')
# 开始的页面
num = 10723
# 最大页面
maxnum = 10802
# 拼接URL
url = 'http://moocs.unipus.cn/course/176/task/' + str(num) + '/show'
browser.get(url)
# 登录
# 输入用户名
user_input = browser.find_element_by_name('username')
user_input.send_keys(username)
# 输入密码
pass_input = browser.find_element_by_name('password')
pass_input.send_keys(password)
# 点击登录
button = browser.find_element_by_id('login')
button.click()
# print(brower.page_source)
for i in range(num, maxnum):
    time.sleep(3)
    # 获取标题
    title = browser.find_element_by_class_name('dashboard-header')
    print(title.text[5:])
    print("课程url:%d"%num)
    back = (str)(title.text)
    back = back[-4:]
    if (back != '单元测试' and back != '思辨讨论'):
        browser.switch_to.default_content()
        # 进到子frame，因为视频是单独的frame
        browser.switch_to_frame('task-content-iframe')
        text = browser.find_element_by_tag_name("iframe")
        browser.switch_to.frame(text)
        time.sleep(2)
        # 获取视频时间
        times = browser.find_element_by_class_name('vjs-duration-display').text
        print(times)
        minutes, seconds = times.split(':')
        minutes = (int)(minutes)
        seconds = (int)(seconds)
        sleeptime = minutes * 60 + seconds
        # 获取播放按钮
        button = browser.find_element_by_css_selector('.vjs-play-control.vjs-control.vjs-button')
        button.click()
        time.sleep(sleeptime)
    else:
        time.sleep(5)
    num = num + 1
    url = 'http://moocs.unipus.cn/course/176/task/' + str(num) + '/show'
    browser.get(url)