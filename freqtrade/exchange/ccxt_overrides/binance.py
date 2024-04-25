from ccxt import binance as ccxt_binance
from ccxt.async_support import binance as async_binance
from freqtrade.configuration import Configuration

class BinanceOverrideAsync(async_binance):
    def parse_ohlcv(self, ohlcv, market=None):
        inverse = self.safe_bool(market, 'inverse')
        volumeIndex = 7 if inverse else 5
        configured_df_cols = Configuration.get_static_config()["dataframe_columns"]
        number_columns_to_index = {"openTime":0,
                                "open":1,
                                "high":2,
                                "low":3,
                                "close":4,
                                "volume":volumeIndex,
                                "number_of_trades":8,
                                "taker_buy_volume":10
                                }
        open_time_col = self.safe_integer_2(ohlcv, 0, 'openTime')
        return [open_time_col]+[self.safe_number_2(ohlcv,x,number_columns_to_index[x])  for x in configured_df_cols if x in number_columns_to_index]
class BinanceOverride(ccxt_binance):
    def parse_ohlcv(self, ohlcv, market=None):
        inverse = self.safe_bool(market, 'inverse')
        volumeIndex = 7 if inverse else 5
        configured_df_cols = Configuration.get_static_config()["dataframe_columns"]
        number_columns_to_index = {"openTime":0,
                                "open":1,
                                "high":2,
                                "low":3,
                                "close":4,
                                "volume":volumeIndex,
                                "number_of_trades":8,
                                "taker_buy_volume":10
                                }
        open_time_col = self.safe_integer_2(ohlcv, 0, 'openTime')
        return [open_time_col]+[self.safe_number_2(ohlcv,x,number_columns_to_index[x])  for x in configured_df_cols if x in number_columns_to_index]
