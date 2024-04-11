"""
https://library.tradingtechnologies.com/trade/chrt-ti-adx-dms.html
"""
import sys
import numpy as np
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from scipy import stats


class Indicators:
    def __init__(self):
        self.round_ndigits = 2

    @staticmethod
    def ema(df: pd.DataFrame, col: str = 'close', length: int = 9) -> pd.DataFrame:
        """df must 'close' columns """
        df[f'EMA_{length}'] = ta.ema(df[col], length=length)
        return df


if __name__ == '__main__':
    import json
    from backend_py.broker.broker_alice import AliceBroker

    token = 26000
    with open(f'/Users/apple/Documents/Work/GitRepoLocal/react-trading-app/data/{str(token)}.json', 'r') as fp:
        data = json.load(fp)

    df = pd.DataFrame(data)
    indicator = Indicators()
    df_res = indicator.ema(df, 'close', 9)
    print(pd.concat([df_res.head(2), df_res.tail(2)]))
    data_res = df_res.to_dict(orient='records')
    # df_ind.to_csv('df_ind.csv')
    print(data_res)
