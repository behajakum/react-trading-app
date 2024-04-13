import os
import json
import pandas as pd
from collections import namedtuple
from datetime import datetime, timedelta, time as dttm
import logging

import requests
from pya3 import Aliceblue
from backend_py.config.config import get_server_config, get_system_config, get_user_config

logger = logging.getLogger(__name__)
FILE_DIR = os.path.abspath(os.path.join(__file__, '..'))


def get_alice(broker_config: dict = None) -> Aliceblue:
    broker_config = get_user_config() if broker_config is None else broker_config
    alice_broker = AliceBroker(broker_config)
    return alice_broker.alice


class AliceBroker():
    def __init__(self, broker_config: dict = None) -> None:
        broker_config = get_user_config() if broker_config is None else broker_config
        self.user_id = broker_config['user_id']
        self.session_id = self._get_session_id(broker_config['api_key'])
        self.alice = Aliceblue(self.user_id, broker_config['api_key'], session_id=self.session_id)
        self.base_url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api'
        self.base_url_option = 'https://optiondata.aliceblueonline.com/api'

    def _get_session_id(self, api_key):
        """Gets session from json file if exists for the day"""
        session_fpath = f'{FILE_DIR}/sessions/alice_session.json'
        if os.path.exists(session_fpath):
            with open(session_fpath, 'r') as fp:
                session = json.load(fp)
            if 'sessionID' in session and \
                    datetime.fromisoformat(session['timestamp']) > datetime.combine(datetime.now().date(),
                                                                                    dttm(7, 0)):
                return session['sessionID']
            else:
                os.makedirs(os.path.dirname(session_fpath), mode=0o777, exist_ok=True)
                alice = Aliceblue(self.user_id, api_key)
                session = alice.get_session_id()
                session.update(dict(timestamp=datetime.now().isoformat(sep=' ', timespec='seconds')))
                with open(session_fpath, 'w') as fp:
                    json.dump(session, fp)
                return session['sessionID']
        else:
            os.makedirs(os.path.dirname(session_fpath), mode=0o777, exist_ok=True)
            alice = Aliceblue(self.user_id, api_key)
            session = alice.get_session_id()
            session.update(dict(timestamp=datetime.now().isoformat(sep=' ', timespec='seconds')))
            with open(session_fpath, 'w') as fp:
                json.dump(session, fp)
            return session['sessionID']

    def _historical_alice_api(self, instrument: namedtuple, from_datetime: datetime, to_datetime: datetime,
                              interval: str = "1", indices: bool = False) -> pd.DataFrame | dict:
        result_cols = ['open', 'high', 'low', 'close', 'volume']

        payload = json.dumps({"token": str(instrument.token),
                              "exchange": instrument.exchange if not indices else f"{instrument.exchange}::index",
                              "from": str(int(from_datetime.timestamp() * 1000)),  # "1660128489000", 1666268893
                              "to": str(int(to_datetime.timestamp() * 1000)),  # "1660221861000", 1666355293
                              "resolution": interval
                              })
        headers = {
            'Authorization': f'Bearer {self.user_id} {self.session_id}',
            'Content-Type': 'application/json'
        }
        lst = requests.post(f'{self.base_url}/chart/history', data=payload, headers=headers)
        response = lst.json()
        if response['stat'] == 'Not_Ok':
            return response
        else:
            df = pd.DataFrame(lst.json()['result'])
            df = df.rename(columns={'time': 'datetime'})
            df = df[['datetime'] + result_cols]
            df.set_index(pd.DatetimeIndex(df['datetime']), inplace=True)
            df.drop(columns='datetime', inplace=True)
            df['volume'] = df['volume'].astype(int)
            return df[result_cols]

    def fetch_historical(self, token: int, from_epoch: int, to_epoch: int,
                         interval: str = "1", exchange: str = 'NSE', indices: str = True) -> list:
        """Returns list of object"""
        payload = json.dumps({"token": str(token),
                              "exchange": exchange if not indices else f"{exchange}::index",
                              "from": str(from_epoch),  # "1660128489000", 1666268893
                              "to": str(to_epoch),  # "1660221861000", 1666355293
                              "resolution": interval  # "1", "D"
                              })
        headers = {
            'Authorization': f'Bearer {self.user_id} {self.session_id}',
            'Content-Type': 'application/json'
        }
        lst = requests.post(f'{self.base_url}/chart/history', data=payload, headers=headers)
        response = lst.json()
        if response['stat'] == 'Not_Ok':
            return response
        return response['result']


if __name__ == '__main__':
    ab = AliceBroker()
    token = 26000
    to_epoch = int(datetime.now().timestamp() * 1000)
    from_epoch = int(to_epoch - 7 * 24 * 3600 * 1000)
    data = ab.fetch_historical(token, from_epoch, to_epoch, "1")
    logger.info(data)
    # with open(f'/Users/apple/Documents/Work/GitRepoLocal/react-trading-app/data/{str(token)}.json', 'w') as fp:
    #     json.dump(data, fp)
