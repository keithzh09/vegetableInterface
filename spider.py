# -*- coding:utf-8 -*-
import csv
import time
import requests
from lxml import etree

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36'
}

# 初始化访问地址
base_url = "http://www.jnmarket.net/import/list-1_"
offset = 1

# 获取总的页面数
url = base_url + str(offset) + ".html"
response = requests.get(url, headers=headers)
html = response.content.decode("utf-8")
selector = etree.HTML(html)
page_num = selector.xpath('/html/body/div[4]/div/div[2]/div[2]/div[2]/a[3]/text()')
response.close()

# 爬取数据并添加到字典中
while offset <= int(page_num):
    url = base_url + str(offset) + ".html"
    response = requests.get(url, headers=headers)
    html = response.content.decode("utf-8")
    selector = etree.HTML(html)

    spider_date = selector.xpath('//table/tbody/tr/td[5]/text()')  # 蔬菜名字
    spider_name = selector.xpath('//table/tbody/tr/td[1]/text()')  # 蔬菜产地
    spider_place = selector.xpath('//table/tbody/tr/td[2]/text()')  # 蔬菜价格
    spider_price = selector.xpath('//table/tbody/tr/td[3]/text()')  # 日期
    response.close()

    # 格式化日期
    for i in range(len(spider_date)):
        time_struct = time.strptime(spider_date[i], "%y-%m-%d")
        spider_date[i] = time.strftime("%Y/%m/%d", time_struct)

    # 每爬取一个页面就写入csv文件中
    with open('vegetable.csv', 'a+') as f:
        writer = csv.writer(f)
        length = spider_name
        for i in range(length):
            writer.writerow((spider_name[i], spider_date[i], spider_price[i], spider_date[i]))

    offset += 1

    # 每爬取20个页面就休眠5秒
    if offset % 20 == 0:
        time.sleep(5)
