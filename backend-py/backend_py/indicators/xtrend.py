import sys
import numpy as np
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta


class Xtrend:
    def __init__(self):
        self.data = dict()
        self.last_bar = None

    def xtrend(self, series: pd.Series, fp: int=2, sp: int=3, ema_period: int=200) -> pd.DataFrame:
        if self.last_bar is not None and series['time'] != self.last_bar['time']:
            self.data['df'].loc[self.data['df'].index[-1]] = self.last_bar
            self.data['df'] = pd.concat([self.data['df'], series.to_frame().T], ignore_index=True)
        else:
            df_xt = self._initialize_xtrend(series)
            self.data['df'] = series.to_frame().T
            self.data['df_xt'] = df_xt
            self.last_bar = series
            return df_xt
        self.last_bar = series
        df = self.data['df'].copy()

        # ts_idx = df.index[-1]
        # df_xt.loc[ts_idx, df.columns] = df.loc[ts_idx, df.columns]
        # df_xt.at[ts_idx, 'lowest_low'] = df_xt['low'].rolling(window=3, min_periods=3).min().iloc[-1]

        lowest_low = df['low'].iloc[-sp:].rolling(window=sp, min_periods=sp).min().iloc[-1]
        ma_low = df['low'].iloc[-sp:].ewm(span=sp, adjust=False, min_periods=sp).mean().round(2).iloc[-1]

        highest_high = df['high'].iloc[-sp:].rolling(window=fp, min_periods=fp).max().iloc[-1]
        ma_high = df['high'].iloc[-sp:].rolling(window=fp, min_periods=fp).mean().iloc[-1]

        next_trend = self.data['df_xt']['next_trend'].iloc[-1]
        trend = self.data['df_xt']['trend'].iloc[-1]

        low_max = self.data['df_xt']['low_max'].iloc[-1]
        high_min = self.data['df_xt']['high_min'].iloc[-1]

        line_ht = self.data['df_xt']['line_ht'].iloc[-1]
        line_color = 'rgba(120, 123, 134, 1)' # gray
        arrow_shift = 0
        alert = 0

        # atr_10 = ta.atr(high=df.iloc[-10:]['high'], low=df.iloc[-10:]['low'], close=df.iloc[-10:]['close'],
        #                 length=10)
        ema_200 = ta.ema(close=df.iloc[-ema_period:]['close'], length=ema_period)
        # ema_200 = df['close'].iloc[-200:].ewm(span=200, adjust=False, min_periods=200).mean().round(2).iloc[-1]


        if next_trend == 1:
            low_max = np.nanmax([low_max, lowest_low])
            if (ma_high < low_max) and (df['close'].iloc[-1] < df['low'].iloc[-2]):
                trend = 1
                next_trend= 0
                high_min = highest_high

        if next_trend == 0:
            high_min = np.nanmin([high_min, highest_high])
            if ma_low > high_min and df['close'].iloc[-1] > df['high'].iloc[-2]:
                trend = 0
                next_trend = 1
                low_max = lowest_low

        if trend == 0:
            line_color = 'rgba(33, 150, 243, 1)'  # blue
            if self.data['df_xt']['trend'].iloc[-1] == 0:
                line_ht = np.nanmax([low_max, self.data['df_xt']['line_ht'].iloc[-1]])
            if self.data['df_xt']['trend'].iloc[-1] == 1:
                arrow_shift = -1  # * atr_10 if atr_10.iloc[-1] is not None else -1

        if trend == 1:
            line_color = 'rgba(255, 152, 0, 1)'  # orange
            if self.data['df_xt']['trend'].iloc[-1] == 1:
                line_ht = np.nanmin([high_min, self.data['df_xt']['line_ht'].iloc[-1]])
            if self.data['df_xt']['trend'].iloc[-1] == 0:
                arrow_shift = 1  # * atr_10.iloc[1] if atr_10 is not None else 1

        if arrow_shift < 0:
            alert = 1
        elif arrow_shift > 0:
            alert = -1

        df_xt = pd.DataFrame(data={
            'time': df['time'].iloc[-1],
            'lowest_low': lowest_low,
            'ma_low': ma_low,
            'highest_high': highest_high,
            'ma_high': ma_high,
            'next_trend': next_trend,
            'trend': trend,
            'low_max': low_max,
            'high_min': high_min,
            'line_ht': line_ht,
            'line_color': line_color,
            'arrow_shift': arrow_shift,
            'alert': alert,
            'ema_200': ema_200.iloc[-1] if ema_200 is not None else np.nan
        }, index=[df.index[-1]])
        self.data['df_xt'] = pd.concat([self.data['df_xt'], df_xt], ignore_index=True)
        return df_xt

    def _initialize_xtrend(self, series: pd.Series):
        return pd.DataFrame({
            'time': series['time'],
            'lowest_low': np.nan,
            'ma_low': np.nan,
            'highest_high': np.nan,
            'ma_high': np.nan,
            'next_trend': 0,
            'trend': 0,
            'low_max': series['low'],
            'high_min': series['high'],
            'line_ht': series['close'],
            'line_color': 'rgba(120, 123, 134, 1)',
            'arrow_shift': 0,
            'alert': 0,
            'ema_200': np.nan
        }, index=[0])


if __name__ == '__main__':
    import os
    import json
    import matplotlib.pyplot as plt
    from dotenv import load_dotenv

    token = 26000
    with open(f'/Users/apple/Documents/Work/GitRepoLocal/react-trading-app/data/{str(token)}.json', 'r') as fp:
        data = json.load(fp)
    for item in data:
        item['time'] = int(datetime.fromisoformat(item['time']).timestamp()) * 1000

    df = pd.DataFrame(data)
    # ---------
    df_xt = indicator.xtrend(df.iloc[:75*3])
    for idx, row in df.iloc[75*3:].iterrows():
        df_x = indicator.xtrend(row)
        df_xt = pd.concat([df_xt, df_x], ignore_index=True)
    # ---------
    print(pd.concat([df_xt.head(10), df_xt.tail(2)]))
    # df.to_csv('df.csv')
    df_xt.plot(x='time', y='line_ht')
    df_xt.plot(x='time', y='alert', kind='scatter')
    plt.show()