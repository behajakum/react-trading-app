"""
https://library.tradingtechnologies.com/trade/chrt-ti-adx-dms.html
"""
import sys
import numpy as np
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from scipy import stats


class Indicator:
    def __init__(self):
        self.round_ndigits = 2

    @staticmethod
    def add_ema(df: pd.DataFrame, col: str = 'close', length: int = 9) -> pd.DataFrame:
        """df must 'close' columns """
        df[f'EMA_{length}'] = ta.ema(df[col], length=length)
        return df

    @staticmethod
    def add_emas(df: pd.DataFrame, col: str = 'close', lengths: list = None) -> pd.DataFrame:
        lengths = lengths if lengths is not None else [9, 11]
        for length in lengths:
            df[f'EMA_{length}'] = ta.ema(df[col], length=length)
        return df

    @staticmethod
    def add_rsi(df: pd.DataFrame, col: str = 'close', length: int = 14) -> pd.DataFrame:
        df[f'RSI_{length}'] = ta.rsi(df[col], length=length)
        return df

    @staticmethod
    def add_supertrend(df: pd.DataFrame, length: int = 7, factor: int = 2) -> pd.DataFrame:
        """['SUPERT_7_2.0', 'SUPERTd_7_2.0', 'SUPERTl_7_2.0', 'SUPERTs_7_2.0']"""
        df_st = ta.supertrend(df.high, df.low, df.close, length=length, multiplier=factor)
        return pd.concat([df, df_st], axis=1)


if __name__ == '__main__':
    import json
    from backend_py.broker.broker_alice import AliceBroker

    token = 26000
    with open(f'/Users/apple/Documents/Work/GitRepoLocal/react-trading-app/data/{str(token)}.json', 'r') as fp:
        data = json.load(fp)
    for item in data:
        item['time'] = int(datetime.fromisoformat(item['time']).timestamp()) * 1000

    df = pd.DataFrame(data)
    indicator = Indicator()
    df_res = indicator.add_emas(df, 'close', [9, 21])
    df_res = indicator.add_rsi(df_res, 'close', 14)
    df_res = indicator.add_supertrend(df_res, 7, 2)
    print(pd.concat([df_res.head(2), df_res.tail(2)]))
    data_res = df_res.to_dict(orient='records')
    # df_ind.to_csv('df_ind.csv')
    print(data_res[:5])
