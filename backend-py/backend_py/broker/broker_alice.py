import os
import json
from datetime import datetime, timedelta, time as dttm
import logging
from pya3 import Aliceblue
from backend_py.config.config import get_server_config, get_system_config, get_user_config


logger = logging.getLogger(__name__)
FILE_DIR = os.path.abspath(os.path.join(__file__, '..'))


def get_alice(broker_config: dict = None) -> Aliceblue:
    broker_config = get_user_config() if broker_config is None else broker_config
    alice_broker = AliceBroker(broker_config)
    return alice_broker.alice


class AliceBroker():
    def __init__(self, broker_config: dict) -> None:
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
