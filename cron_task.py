# coding: utf-8
# @author  : lin
# @time    : 19-3-10
from multiprocessing import Process, Pool

pool = Pool(processes=4)


if __name__ == '__main__':
    pool.apply_async(cron_task, ('02:38',))
