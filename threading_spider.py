import threading
from queue import Queue
import urllib
from lxml import etree
import json


class ThreadCrawl(threading.Thread):
    def __init__(self, thread_name, page_queue, data_queue):
        super(ThreadCrawl, self).__init__()
        self.thread_name = thread_name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64;Trident/7.0;rv:11.0 )like Gecko'
             }

    def run(self):#重写run方法
        while not PAGE_EXIST:
            #从队列中取出页码，与URL进行拼接，发送请求获取页面HTML
            #设置block 为FALSE，在page_queue为空时，触发异常。变为非阻塞状态
            #将得到的HTML写入data_queue 队列中
            try:
                page = self.page_queue.get(False)
                url = 'https://www.qiushibaike.com/8hr/page/'
                full_url = url + str(page)
                request = urllib.request.Request(full_url, headers=self.headers)
                response = urllib.request.urlopen(request)
                html = response.read()
                self.data_queue.put(html, block=False)
            except:
                pass
    print('-------1---------------')


class Parse(threading.Thread):
    def __init__(self, data_queue, parse_name, filename, lock):

        super(Parse, self).__init__()
        self.data_queue = data_queue
        self.parse_name = parse_name
        self.filename = filename
        self.lock = lock

    def run(self):
        #重写run方法
        while not DATA_EXIST:
            try:
                #从data_queue 中取出HTML，并进行解析
                html = self.data_queue.get(False)
                self.parse(html)
            except:
                pass

    def parse(self, html):
        html = etree.HTML(html)
        t = html.xpath("//div[contains(@id,'qiushi_tag_')]")
        dict = {}
        for list in t:
            name = list.xpath(".//h2/text()")[0]
            img = list.xpath(".//img/@src")
            content = list.xpath(".//div[@class='content']/span/text()")
            haoxiao = list.xpath(".//i[0]/text()")
            comment = list.xpath(".//i[1]/text()")
            dict = {
                'name': name,
                'img': img,
                'content': content,
                'haoxiao': haoxiao,
                'comment': comment, }
            with self.lock:
                #以jSON 格式写入文件
                self.filename.write(json.dumps(dict, ensure_ascii=False)+'\n')
    print('------------5----------')


def main():
    #采集队列，将得到的HTML放入到队列当中，括号为空表示不限制
    data_queue = Queue()
    #页码队列，将页码遍历依次放入到队列中。
    page_queue = Queue(10)
    for i in range(1,11):
        page_queue.put(i)
    #以追加的方式写入文件
    filename = open('duanzi.json','a')
    #创建锁
    lock = threading.Lock()
    #采集线程名称
    thread_names = ['采集线程一号', '采集线程2号', '采集线程3号']
    #储存三个线程的集合
    thread_crawl = []
    #依次遍历名称列表创建Thread实例对象
    for thread_name in thread_names:
        thread = ThreadCrawl(thread_name, page_queue, data_queue)
        thread.start()
        thread_crawl.append(thread)
    #解析线程名称
    parse_names = ['下载线程一号', '下载线程2号', '下载线程3号']
    #储存三个下载线程集合
    parse = []
    #依次遍历创建三个下载线程
    for parse_name in parse_names:
        thread_parse = Parse(parse_name, data_queue, filename, lock)
        thread_parse.start()
        parse.append(thread_parse)
    #当页面队列不为空时
    while not page_queue.empty():
        pass
    #如果page-queue为空，采集线程退出循环
    global PAGE_EXIST
    PAGE_EXIST = True
    for thread in thread_crawl:
        thread.join()
    while not data_queue.empty():
        pass
    #声明全局变量
    global DATA_EXIST
    DATA_EXIST = True
    for thread in parse:
        thread.join()
    with lock:
        filename.close()
#全局变量必须大写
PAGE_EXIST = False
DATA_EXIST = False

if __name__ =='__main__':
    main()
