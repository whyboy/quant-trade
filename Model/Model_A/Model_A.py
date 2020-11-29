import sys
sys.path.append('../')
from Common import DataCalculator
from Common import Helper
from DataLoader import DataLoader
from datetime import datetime
import numpy as np

class Model(object):
    def __init__(self, ip, port, source_data_dir):
        self.type_count = 5
        self.data_loader = DataLoader.DataLoader(ip, port, source_data_dir)

    @staticmethod
    def __get_volume_price_type(volume_diff, price_diff):
        if volume_diff > 0 and price_diff > 0:
            return 0
        elif volume_diff > 0 and price_diff < 0:
            return 1
        elif volume_diff < 0 and price_diff > 0:
            return 2
        elif volume_diff < 0 and price_diff < 0:
            return 3
        else:
            return 4

    # Given a stock code, and with the start_date, end_date, category, calculate the stock type
    # Return is a dict, the Key is date, the Value is the volume_price_type vector.
    def get_datetime2type_and_date2price(self, stock_code, category):
        print("input stock_code: %s" % stock_code)
        datetime2type = dict()
        date2price = dict()
        raw_data = self.data_loader.upload_security_bars([stock_code], category)[0]

        if (raw_data.shape[0] != 0):
            open_price_list = raw_data['open'].values
            close_price_list = raw_data['close'].values
            vol_list = raw_data['vol'].values
            date_time_list = raw_data['datetime'].values

            for idx, (open_price, close_price, vol, date_time) in enumerate(
                    zip(open_price_list, close_price_list, vol_list, date_time_list)):

                date_of_day = date_time.split()[0]
                date2price[date_of_day] = open_price
                if idx == 0:
                    continue
                volume_diff = vol - vol_list[idx - 1]
                price_diff = close_price - close_price_list[idx - 1]
                volume_price_type = self.__get_volume_price_type(volume_diff, price_diff)

                if date_time not in datetime2type:
                    datetime2type[date_time] = np.array([0.] * self.type_count)

                datetime2type[date_time][volume_price_type] += 1.

        return (datetime2type, date2price)

    # Give a stock code list, get the weighted volume-price type of the stock list.
    def get_compose_date2type(self, code_list, category):

        date2type_weighted = dict()
        datetime2type_list = []
        date2price_list = []
        zongguben_list = self.data_loader.get_zongguben(code_list)
        datetime_union = None
        for (idx, code) in enumerate(code_list):
            (datetime2type, date2price) = self.get_datetime2type_and_date2price(code, category)
            datetime2type_list.append(datetime2type)
            date2price_list.append(date2price)
            if datetime_union is None:
                datetime_union = set(datetime2type.keys())
            else:
                datetime_union = datetime_union.union(set(datetime2type.keys()))

        datetime_intersection_sorted = sorted(datetime_union)
        for datetime_str in datetime_intersection_sorted:
            market_value_list = []
            cur_date = datetime_str.split()[0]
            for idx, datetime2type in enumerate(datetime2type_list):
                if cur_date in date2price_list[idx]:
                    market_value = date2price_list[idx][cur_date] * zongguben_list[idx]
                else:
                    market_value = 0.
                market_value_list.append(market_value)

            tot_market_value = sum(market_value_list)
            weight_list = [tmp / tot_market_value for tmp in market_value_list]

            type_weight = np.array([0.] * self.type_count)
            for idx, datetime2type in enumerate(datetime2type_list):
                if datetime_str in datetime2type:
                    volume_price_type = datetime2type[datetime_str]
                else:
                    volume_price_type = np.array([0.] * self.type_count)
                type_weight += volume_price_type * weight_list[idx]
            date2type_weighted[datetime_str] = type_weight

        return date2type_weighted

    def strategy(self):
        file_path = "C:/Users/why/Desktop/Stock/data/创业板50/创业板50-20201115.xls"
        code2business = self.data_loader.get_stockCode2business(file_path)
        business2code = self.data_loader.get_business2stockCodes('C:/Users/why/Desktop/Stock/data/行业板块/')
        print(code2business)

        # Get the 创业板50 stocks code list.
        code_list = code2business.keys()

        # 获取个股所组成的指数 时间——类型 字典.
        date2type_weighted = self.get_compose_date2type(code_list, 2)
        save_file_path = 'C:/Users/why/Desktop/quant-trade/result/'

        Helper.write_dict_to_file(date2type_weighted, save_file_path+'baseStock')

        # # 获取每只个股包含的行业指数 时间——类型 字典 并存储起来
        # for idx, code in enumerate(code_list):
        #     print("cur idx: %d   code: %s" % (idx, code))
        #     business = code2business[code]
        #     business_code_list = business2code[business]
        #     date2type_weighted_business = self.get_compose_date2type(business_code_list, 2)