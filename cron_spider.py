import requests
from lxml import etree
import time
from db_model.model_dao import VegetableModelDao, VegetablePriceModelDao
import schedule
from multiprocessing import Process


def spider_vegetable():
    print("SPIDER START!!")
    name = []  # 蔬菜名字
    place = []  # 蔬菜产地
    price = []  # 蔬菜价格
    date = []  # 日期

    # 获取今天的日期
    today = time.strftime('%y-%m-%d', time.localtime(time.time()))

    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.133 Safari/537.36'
    }

    # 初始化访问地址
    base_url = "http://www.jnmarket.net/import/list-1_"
    offset = 1

    # 爬取数据并添加到字典中
    while 1:
        # 获取响应并定义选择器
        url = base_url + str(offset) + ".html"
        response = requests.get(url, headers=headers)
        html = response.text
        selector = etree.HTML(html)

        spider_date = selector.xpath('//table/tbody/tr/td[5]/text()')
        spider_name = selector.xpath('//table/tbody/tr/td[1]/text()')
        spider_place = selector.xpath('//table/tbody/tr/td[2]/text()')
        spider_price = selector.xpath('//table/tbody/tr/td[3]/text()')

        if len(spider_date) == spider_date.count(today):
            # 格式化日期，如2016/01/01
            for i in range(len(spider_date)):
                time_struct = time.strptime(spider_date[i], "%y-%m-%d")
                spider_date[i] = time.strftime("%Y/%m/%d", time_struct)

            name += spider_name
            place += spider_place
            price += spider_price
            date += spider_date

            offset += 1
        else:
            # 截取长度
            length = spider_date.count(today)

            # 格式化日期，如2016/01/01
            for i in range(len(spider_date)):
                time_struct = time.strptime(spider_date[i], "%y-%m-%d")
                spider_date[i] = time.strftime("%Y/%m/%d", time_struct)

            name += spider_name[:length]
            place += spider_place[:length]
            price += spider_price[:length]
            date += spider_date[:length]

            break

    # 添加到数据库中
    for i in range(len(name)):
        veg_id = VegetableModelDao.get_id_by_name(name[i])
        VegetablePriceModelDao.add_one_data(veg_id, date[i], price[i], place[i])


def cron_task(the_time):
    """
    定时任务
    :param the_time:
    :return:
    """
    schedule.every().day.at(the_time).do(spider_vegetable)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    p = Process(target=cron_task, args=('21:49',))
    p.start()

