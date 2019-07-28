# -*- coding: utf-8 -*-
import scrapy
from taobao.tools import register
from taobao.settings import *
from taobao.items import TaobaoItem
import time
import random
import re
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchSpider(scrapy.Spider):
    name = 'search'
    # allowed_domains = ['taobao.com']
    # start_urls = ['http://taobao.com/']
    base_url = 'https://s.taobao.com/search?q='
    key = '电脑'
    start_urls = [base_url + str(key)]
    i = 1

    def start_requests(self):
        #这里调用selenium登录的方法并返回browser和一个cookies
        self.browser,list = register()
        #使用browser登录淘宝商品搜索页面
        self.browser.get(self.start_urls[0])
        #使用execute_script执行js操作，这里是下拉到最底下
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        #获取selenium界面当前的url用来错误处理,html表示获取源代码
        html = self.browser.page_source
        #meta可以用来传递全局变量
        yield scrapy.Request(url=self.start_urls[0],cookies=list,callback=self.parse,meta={'html':html,'i':self.i})


    def parse(self, response):
        # print(response.body)


        print("1111111111111----------")
        time.sleep(5)
        
        i = response.meta.get("i")
        # url_i = response.meta.get("url")
        i +=1
        # print("2222222222222----------")
        if i > 100:
            return
        # try:
        # print("start:----------------------------")
        node_list = response.xpath("//div[@class='item J_MouserOnverReq  ']/div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']")
        print(node_list)
        for node in node_list:
            item = TaobaoItem()
            # print("--------------------------------")
            item['name'] = node.xpath("./div[@class='row row-2 title']/a[@class='J_ClickStat']/text()[2]").extract()[0].encode("utf-8")
            item['price'] = node.xpath("./div[@class='row row-1 g-clearfix']/div[@class='price g_price g_price-highlight']/strong/text()").extract()[0].encode("utf-8")
            item['payment_num'] = node.xpath("./div[@class='row row-1 g-clearfix']/div[@class='deal-cnt']/text()").extract()[0].encode("utf-8")
            item['shop_name'] = node.xpath("./div[@class='row row-3 g-clearfix']/div[@class='shop']/a/span[2]/text()").extract()[0].encode("utf-8")
            item['shop_address'] = node.xpath("./div[@class='row row-3 g-clearfix']/div[@class='location']/text()").extract()[0].encode("utf-8")
            yield item
        
        #点击下一页
        button = self.browser.find_elements(By.XPATH,'//a[@class="J_Ajax num icon-tag"]')[-1]
        button.click()
        time.sleep(random.random()*2)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        html = self.browser.page_source
        yield scrapy.Request(url=response.url,callback=self.parse,meta={'html':html},dont_filter=True)
        # except Exception as e:
        #     time.sleep(10)
        #     print(e)
        #     self.browser.close()
        #     self.browser,list = register()
        #     self.browser.get(url=url_i)
        #     time.sleep(random.random()*2)
        #     self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        #     html = self.browser.page_source
        #     yield scrapy.Request(url=response.url,callback=self.parse,meta={'html':html,'i':i,'url':url_i},dont_filter=True)


    def close(spider, reason):
        spider.browser.close()

       
