from ccxt import binance as ccxt_binance
from ccxt.async_support import binance as async_binance
from freqtrade.configuration import Configuration

class BinanceOverrideAsync(async_binance):
    def parse_ohlcv(self, ohlcv, market=None):
        # when api method = publicGetKlines or fapiPublicGetKlines or dapiPublicGetKlines
        #     [
        #         1591478520000,  # open time
        #         "0.02501300",  # open
        #         "0.02501800",  # high
        #         "0.02500000",  # low
        #         "0.02500000",  # close
        #         "22.19000000",  # volume
        #         1591478579999,  # close time
        #         "0.55490906",  # quote asset volume, base asset volume for dapi
        #         40,            # number of trades
        #         "10.92900000",  # taker buy base asset volume
        #         "0.27336462",  # taker buy quote asset volume
        #         "0"            # ignore
        #     ]
        #
        #  when api method = fapiPublicGetMarkPriceKlines or fapiPublicGetIndexPriceKlines
        #     [
        #         [
        #         1591256460000,          # Open time
        #         "9653.29201333",        # Open
        #         "9654.56401333",        # High
        #         "9653.07367333",        # Low
        #         "9653.07367333",        # Close(or latest price)
        #         "0",                    # Ignore
        #         1591256519999,          # Close time
        #         "0",                    # Ignore
        #         60,                     # Number of bisic data
        #         "0",                    # Ignore
        #         "0",                    # Ignore
        #         "0"                     # Ignore
        #         ]
        #     ]
        #
        # options
        #
        #     {
        #         "open": "32.2",
        #         "high": "32.2",
        #         "low": "32.2",
        #         "close": "32.2",
        #         "volume": "0",
        #         "interval": "5m",
        #         "tradeCount": 0,
        #         "takerVolume": "0",
        #         "takerAmount": "0",
        #         "amount": "0",
        #         "openTime": 1677096900000,
        #         "closeTime": 1677097200000
        #     }
        #
        inverse = self.safe_bool(market, 'inverse')
        volumeIndex = 7 if inverse else 5
        configured_df_cols = Configuration.get_static_config()["dataframe_columns"]
        number_columns_to_index = {"open":1,
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
        number_columns_to_index = {"open":1,
                                "high":2,
                                "low":3,
                                "close":4,
                                "volume":volumeIndex,
                                "number_of_trades":8,
                                "taker_buy_volume":10
                                }
        open_time_col = self.safe_integer_2(ohlcv, 0, 'openTime')
        return [open_time_col]+[self.safe_number_2(ohlcv,x,number_columns_to_index[x])  for x in configured_df_cols if x in number_columns_to_index]
