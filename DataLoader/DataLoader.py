from pytdx.hq import TdxHq_API
from Common import DataCalculator
from Common import Helper
from pytdx.params import TDXParams
import datetime
import pandas as pd
import numpy as np
import time
import os

class DataLoader(object):
    def __init__(self, ip, port, source_data_dir):
        self.Api = TdxHq_API()
        self.IP = ip
        self.Port = port
        self.Max_bar_count = 8000
        self.Source_data_dir = source_data_dir

    # Given a stock and return it's business.
    def get_stockCode2business(self, file_path) -> dict:
        stockCode2business = dict()
        with open(file_path, 'r') as f:
            for (idx, line) in enumerate(f):
                line = line.split()
                if idx == 0:
                    code_index = Helper.index_helper(line, '代码')
                    name_index = Helper.index_helper(line, '名称')
                    business_index = Helper.index_helper(line, '细分行业')
                else:
                    if (len(line) < 3):
                        continue
                    code = line[code_index]
                    name = line[name_index]
                    business = line[business_index]
                    stockCode2business[code] = business

        print("total stock count is " + str(len(stockCode2business)))
        return stockCode2business

    # get the business to stock list dict.
    def get_business2stockCodes(self, file_path):
        business2stockCodes = dict()
        business_files = os.listdir(file_path)
        for business_file in business_files:
            sub_file_path = file_path + business_file
            sub_files = os.listdir(sub_file_path)
            stockCodes = [file_name[3:-4] for file_name in sub_files]
            business2stockCodes[business_file] = stockCodes
        return business2stockCodes

    @staticmethod
    def get_market(stock_code):
        if stock_code[0] == '6':
            return 1
        else:
            return 0

    # The category to minutes.
    @staticmethod
    def category2minutes(category):
        if category == 0:
            return 5
        elif category == 1:
            return 15
        elif category == 2:
            return 30
        elif category == 3:
            return 60
        elif category == 4:
            return 4 * 60
        else:
            print("current not consider")
            exit()

    def get_store_file_path(self, stock_code, category):
        interval_minutes = DataLoader.category2minutes(category)
        file_name = stock_code + "_" + str(interval_minutes) + '.csv'
        store_file_path = os.path.join(self.Source_data_dir, file_name)
        return store_file_path


    # Given a code list, get the security_bars data with dictionary format.
    # code2data: the key is code, the value is data.
    def download_security_bars(self, stock_code_list, category=2):
        while True:
            try:
                with self.Api.connect(self.IP, self.Port):
                    for stock_code in stock_code_list:
                        market = self.get_market(stock_code)
                        data = []
                        for i in range(10):
                            data += self.Api.get_security_bars(category,market,stock_code,(9-i)*800,800)
                        data_df = self.Api.to_df(data)
                        store_data_path = self.get_store_file_path(stock_code,category)
                        data_df.to_csv(store_data_path, index=False)
                        return data_df
            except:
                print("failure download bars, trying again!")

    # Given a code list and start date_time_day, get the security_bars data with dictionary format.
    # code2data: the key is code, the value is data.
    def download_security_bars_append(self, stock_code_list, category):
        cur_date_time_day = datetime.datetime.now().strftime("%Y-%m-%d")
        while True:
            try:
                with self.Api.connect(self.IP, self.Port):
                    for stock_code in stock_code_list:
                        market = self.get_market(stock_code)
                        store_file_path = self.get_store_file_path(stock_code,category)
                        old_data_df = pd.read_csv(store_file_path)
                        date_time_dict = None
                        row_cnt = old_data_df.shape[0]
                        data_time_dict = None
                        if row_cnt != 0:
                            date_time_dict = {key: 1 for key in old_data_df['datetime']}
                            latest_date_time = old_data_df['datetime'][row_cnt-1]
                            latest_date_time_day = latest_date_time.split()[0].replace('/', '-')
                            trade_days = DataCalculator.calculate_trade_days(latest_date_time_day, cur_date_time_day)
                            bars_count = trade_days * 240 // self.category2minutes(category)
                        else:
                            bars_count = self.Max_bar_count

                        append_data = []
                        batch = 800
                        start = bars_count - batch
                        while start >= 0:
                            append_data += self.Api.get_security_bars(category, market, stock_code, start, batch)
                            start -= batch

                        mod = bars_count % batch
                        if mod != 0:
                            append_data += self.Api.get_security_bars(category, market, stock_code, 0, mod)
                        append_data_df = self.Api.to_df(append_data)

                        if date_time_dict is None:
                            old_data_df = append_data_df

                        else:
                            for idx, row in enumerate(append_data_df.itertuples()):
                                date_time = getattr(row, 'datetime')
                                if date_time not in date_time_dict:
                                    old_data_df = pd.concat([old_data_df,append_data_df[idx::]], axis=0)
                                    break
                        old_data_df.to_csv(store_file_path, index=False)
                        return old_data_df
            except:
                print("failure download append bars, trying again!")


    def upload_security_bars(self, stock_code_list, category=2):
        data_list = []
        print(stock_code_list)
        for stock_code in stock_code_list:
            store_file_path = self.get_store_file_path(stock_code, category)
            if not os.path.exists(store_file_path):
                data = self.download_security_bars([stock_code], category)
            else:
                data = self.download_security_bars_append([stock_code], category)
            data_list.append(data)
        return data_list

    def get_zongguben(self, stock_code_list):
        zongguben_list = []
        with self.Api.connect(self.IP, self.Port):
            for stock_code in stock_code_list:
                market = self.get_market(stock_code)
                finance_info = self.Api.get_finance_info(market, stock_code)
                zongguben = finance_info['zongguben']
                zongguben_list.append(zongguben)

        return zongguben_list

