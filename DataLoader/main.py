from pytdx.hq import TdxHq_API
from DataLoader import DataLoader
from datetime import  datetime
api = TdxHq_API()
if __name__ == '__main__':
    data_dir = "C:/Users/why/Desktop/quant-trade/data"
    loader = DataLoader('119.147.212.81', 7709, data_dir,)
    stock_list = ['300015']

    # loader.download_security_bars(stock_list, 2)
    # loader.download_security_bars_append(stock_list, 2)
    date_1 = datetime.strptime("2020-9-29", "%Y-%m-%d")
    date_2 = datetime.strftime(date_1, "%Y-%m-%d")
    print(date_2)