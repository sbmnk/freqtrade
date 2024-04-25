from ccxt import binance as ccxt_binance
from ccxt.async_support import binance as async_binance
from freqtrade.configuration import Configuration

class BinanceOverrideAsync(async_binance):
    def parse_ohlcv(self, ohlcv, market=None):
        inverse = self.safe_bool(market, 'inverse')
        volumeIndex = 7 if inverse else 5
        configured_df_cols = Configuration.get_static_config()["dataframe_columns"]
        columns_to_index_map = {"date":0,
                                "open":1,
                                "high":2,
                                "low":3,
                                "close":4,
                                "volume":volumeIndex,
                                "number_of_trades":8,
                                "taker_buy_volume":10
                                }
        
        return [self.safe_integer_2(ohlcv,x,columns_to_index_map[x])  for x in configured_df_cols]
class BinanceOverride(ccxt_binance):
    def parse_ohlcv(self, ohlcv, market=None):
        inverse = self.safe_bool(market, 'inverse')
        volumeIndex = 7 if inverse else 5
        configured_df_cols = Configuration.get_static_config()["dataframe_columns"]
        columns_to_index_map = {"date":0,
                                "open":1,
                                "high":2,
                                "low":3,
                                "close":4,
                                "volume":volumeIndex,
                                "number_of_trades":8,
                                "taker_buy_volume":10
                                }
        
        return [self.safe_integer_2(ohlcv,x,columns_to_index_map[x])  for x in configured_df_cols]
