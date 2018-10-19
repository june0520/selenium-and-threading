from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import unittest


class Douyu(unittest.TestCase):
    #初始化测试类
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.count = 0

    def testDouyu(self):
        #测试的方法必须以testk开头。直接利用无头浏览器直接访问网站
        self.driver.get('https://www.douyu.com/directory/all')
        while True:
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            names = soup.find_all('h3', attrs={'class': "ellipsis"})
            numbers = soup.find_all('span', attrs={'class': "dy-num fr"})
            #zip方法把列表组合成元组，并以列表的方式返回[(1,2),(3,4)...]
            for name, number in zip(names, numbers):
                print('观众人数' + number.get_text.strip()+'\t房间名:'+name.get_text().strip())
                self.count += 1
            #如果在页面源码中发现shark - pager - disable的隐藏标签，就推出循环
            if self.driver.page_source.find('shark - pager - disable') != -1:
                return
            else:
                #不断点击下一页


                #click（）方法失效。必须用ENTER才可以
                self.driver.find_element_by_class_name('shark - pager - next').click()
    #测试结束执行的方法
    def tearDown(self):
        #推出浏览器
        self.driver.quit()
        print('直播人数是' + str(self.count))


if __name__ == '__main__':
    #启动测试模块
    unittest.main()