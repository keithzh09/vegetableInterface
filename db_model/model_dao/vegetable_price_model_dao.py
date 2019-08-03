# coding: utf-8
# @author  : lin
# @time    : 19-3-3


from ..model import VegetablePriceModel
from peewee import chunked


class VegetablePriceModelDao:

    @staticmethod
    def add_one_data(veg_id, date, price, place):
        """
        插入一条新数据
        :param veg_id:
        :param date:
        :param price:
        :param place:
        :return:
        """
        try:
            # if not VegetablePriceModelDao.query_vegetable_price_data(5, veg_id=veg_id, start_date=date, stop_date=date
            # ):
            #     return False
            VegetablePriceModel.insert(veg_id=veg_id, date=date, price=price, place=place).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def add_many_data(veg_id, veg_df_data):
        """
        同时插入很多数据
        :param veg_id: 蔬菜id
        :param veg_df_data: 一个dataframe格式的数据，必须包含字段date, price, place
        :return:
        """
        try:
            all_data = []
            for index, row in veg_df_data.iterrows():
                # all_data的格式要符合field，ed. [(1, '2018-01-01', 12.1, '山东'), (...)]，本质是list&tuple
                all_data.append((veg_id, row['date'], row['price'], row['place']))
            field = [VegetablePriceModel.veg_id, VegetablePriceModel.date, VegetablePriceModel.price,
                     VegetablePriceModel.place]
            for data_chunk in chunked(all_data, 1000):
                VegetablePriceModel.insert_many(data_chunk, field).execute()
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def query_vegetable_price_data(func_code=0, veg_id='', start_date='', stop_date='', start_price=0, stop_price=0):
        # TODO:加个修饰器，当func_code与访问值不符合时返回错误
        """
        查找价格数据
        :param func_code: 条件类型，0为查找全部，1为按蔬菜名查找，2为按蔬菜名加日期，3为按蔬菜名加价格，
                          5为以日期查找多条数据，4为组合三种因素，
        :param veg_id:
        :param start_date: 开始日期
        :param stop_date: 结束日期
        :param start_price: 价格下限
        :param stop_price: 价格上限
        :return:
        """
        try:
            if func_code == 0:
                func = VegetablePriceModel.select().execute()
            elif func_code == 1:
                func = VegetablePriceModel.select().where(VegetablePriceModel.veg_id == veg_id).execute()
            elif func_code == 2:
                func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                          (VegetablePriceModel.date >= start_date) &
                                                          (VegetablePriceModel.date <= stop_date)).execute()
            elif func_code == 3:
                func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                          (VegetablePriceModel.price >= start_price) &
                                                          (VegetablePriceModel.price <= stop_price)).execute()
            elif func_code == 5:
                func = VegetablePriceModel.select().where(VegetablePriceModel.date == start_date).execute()
            #     for i in func:
            #         print(i)
            else:
                func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                          (VegetablePriceModel.date >= start_date) &
                                                          (VegetablePriceModel.date <= stop_date) &
                                                          (VegetablePriceModel.price >= start_price) &
                                                          (VegetablePriceModel.price <= stop_price)).execute()
            return func
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def delete_all_data():
        func = VegetablePriceModel.delete()
        return func.execute()


