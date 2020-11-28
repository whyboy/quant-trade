from pytdx.hq import TdxHq_API
api = TdxHq_API()
with api.connect('119.147.212.81', 7709):
    data = api.to_df(api.get_security_bars(9, 0, '000001', 1, 2))
    print(data)