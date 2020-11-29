from Model.Model_A import Model_A

if __name__ == '__main__':
    source_data_dir = 'C:/Users/why/Desktop/quant-trade/data'
    model_obj = Model_A.Model('119.147.212.81', 7709, source_data_dir)
    model_obj.strategy()
