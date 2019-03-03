# coding: utf-8
# @author  : lin
# @time    : 19-3-3


from ..model import VegetablePriceModel


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
            VegetablePriceModel.insert(veg_id=veg_id, date=date, price=price, place=place).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def query_vegetable_price_data(func_code, veg_id="", date="", date_type=True, price=1, price_type=True):
        """
        查找价格数据
        :param func_code: 条件类型，0为查找全部，1为按蔬菜名查找，2为按蔬菜名加日期，3为按蔬菜名加价格，4为组合三种因素
        :param veg_id: 蔬菜id
        :param date: 日期
        :param date_type: 按日期上限或下限进行搜索，True为上限，否则下限
        :param price: 价格
        :param price_type: 按价格上限或下限进行搜索，True为上限，否则下限
        :return:model列表
        """
        try:
            if func_code == 0:
                func = VegetablePriceModel.select()
            elif func_code == 1:
                func = VegetablePriceModel.select().where(VegetablePriceModel.veg_id == veg_id)
            elif func_code == 2:
                if date_type:
                    func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                              (VegetablePriceModel.date <= date))
                else:
                    func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                              (VegetablePriceModel.date >= date))
            elif func_code == 3:
                if price_type:
                    func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                              (VegetablePriceModel.price <= price))
                else:
                    func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                              (VegetablePriceModel.price >= price))
            else:
                if date_type:
                    if price_type:
                        func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                                  (VegetablePriceModel.date <= date) &
                                                                  (VegetablePriceModel.price <= price))
                    else:
                        func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                                  (VegetablePriceModel.date <= date) &
                                                                  (VegetablePriceModel.price >= price))
                else:
                    if price_type:
                        func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                                  (VegetablePriceModel.date >= date) &
                                                                  (VegetablePriceModel.price <= price))
                    else:
                        func = VegetablePriceModel.select().where((VegetablePriceModel.veg_id == veg_id) &
                                                                  (VegetablePriceModel.date >= date) &
                                                                  (VegetablePriceModel.price >= price))
            return func.execute()
        except Exception as error:
            print(error)
            return False

