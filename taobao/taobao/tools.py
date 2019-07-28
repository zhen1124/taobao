# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import time
import random
import re
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from taobao.settings import *


def register():
    
    # browser = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    # browser.get(request.url)
    # browser = driver.page_source.encode('utf-8')
    # browser.quit()  
    while True:
        # options = webdriver.ChromeOptions()
        # # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
         
     '''profile=webdriver.FirefoxOptions()
        # profile.add_argument('-headless') #设置无头模式
        #browser = webdriver.Firefox(executable_path='F:\SpiderLearn\geckodriver.exe',options=profile)

        #设置代理服务器
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.http', '127.0.0.1')#IP为你的代理服务器地址:如‘127.0.0.0’，字符串类型
        profile.set_preference('network.proxy.http_port', 8888)  #PORT为代理服务器端口号:如，9999，整数类型
       
        # browser = webdriver.Chrome(executable_path='F:\SpiderLearn\chromedriver.exe')
        browser = webdriver.Firefox(executable_path='F:\SpiderLearn\geckodriver.exe',options=profile)'''
        browser = webdriver.Firefox(executable_path='F:\SpiderLearn\geckodriver.exe')
        # browser = webdriver.Chrome(executable_path='F:\SpiderLearn\chromedriver.exe')

        browser.get('https://login.taobao.com/member/login.jhtml')

        # 防止有时打开网页是扫码登陆
        try:
            input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, 'J_Quick2Static')))
            input.click()
        except Exception as e:
            print(e)
        
        #输入账号和密码
        user = browser.find_element_by_id('TPL_username_1')
        password = browser.find_element_by_id('TPL_password_1')
        user.send_keys(USER)
        time.sleep(random.random() * 2)
        password.send_keys(PASSWORD)
        time.sleep(random.random() * 1)

        #输入账号密码后会有一个滑动验证
        browser.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")
        
        action = ActionChains(browser)
        time.sleep(random.random() * 1)
        butt = browser.find_element_by_id('nc_1_n1z')
        browser.switch_to.frame(browser.find_element_by_id('_oid_ifr_'))
        browser.switch_to.default_content()
        action.click_and_hold(butt).perform()  #鼠标左键按下不放
        # action.reset_actions()
        action.move_by_offset(285, 0).perform()
        time.sleep(random.random() * 1)

        #提交登陆按钮
        button = browser.find_element_by_id('J_SubmitStatic')
        time.sleep(random.random() * 2)
        button.click()
        time.sleep(random.random() * 2)
        # browser.get('https://www.taobao.com/')
        cookie = browser.get_cookies()
        list = {}
        for cookiez in cookie:
            name = cookiez['name']
            value = cookiez['value']
            list[name] = value
        if len(list) > 10:
            break
        else:
            browser.close()
    return browser,list