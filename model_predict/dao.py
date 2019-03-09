# coding: utf-8
# @author  : lin
# @time    : 19-3-8

from datetime import datetime


def strtime_to_timestamp(strtime):
    """
    字符串时间转时间戳
    :param strtime:
    :return: timestamp
    """
    default_format = '%Y-%m-%d %H:%M:%S'
    if len(strtime) == 19:  # '2018-07-20 12:00:00'
        time_format = default_format
    elif len(strtime) == 10:
        time_format = '%Y-%m-%d'
    elif len(strtime) == 7:
        time_format = '%Y-%m'
    elif len(strtime) == 4:
        time_format = '%Y'
    else:
        time_format = default_format
    timestamp = datetime.strptime(strtime, time_format).timestamp()
    return timestamp


def timestamp_to_strtime(timestamp):
    """
    时间戳转字符串时间， 默认精确到秒
    :param timestamp:
    :return:
    """
    if len(str(timestamp)) == 13:
        timestamp *= 0.001
    strtime = datetime.strftime(datetime.fromtimestamp(timestamp), '%Y-%m-%d %H:%M:%S')
    return strtime
    

def day_increase(strtime, increase_days):
    """
    日期加减
    :param strtime:
    :param increase_days:
    :return:
    """
    timestamp = strtime_to_timestamp(strtime)
    timestamp += increase_days * 86400  # 1 days = 86400s
    time = timestamp_to_strtime(timestamp)
    return time


def day_decrease(strtime, decrease_days):
    """
    日期加减
    :param strtime:
    :param decrease_days:
    :return:
    """
    timestamp = strtime_to_timestamp(strtime)
    timestamp -= decrease_days * 86400  # 1 days = 86400s
    time = timestamp_to_strtime(timestamp)
    return time
