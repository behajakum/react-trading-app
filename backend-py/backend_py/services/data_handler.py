from datetime import datetime
import logging
from backend_py.broker.broker_alice import AliceBroker
from backend_py.config.config import get_server_config, get_system_config, get_user_config

logger = logging.getLogger(__name__)

class DataHandler:
    def __init__(self):
        self.ab = AliceBroker(broker_config=get_user_config())

    def fetch_historical(self, token: int, interval: str, from_epoch: int, to_epoch: int):
        res = self.ab.fetch_historical(token, from_epoch, to_epoch, interval)
        return self.convert_to_epoch(res)

    def convert_to_epoch(self, data: list) -> list:
        for item in data:
            item['time'] = int(datetime.fromisoformat(item['time']).timestamp())  # sec
        return data