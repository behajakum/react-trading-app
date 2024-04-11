from typing import Any
import json
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import logging
from backend_py.broker.broker_alice import get_alice, AliceBroker
from pydantic import BaseModel

from backend_py.config.config import get_server_config, get_system_config, get_user_config
from backend_py.indicators.indicator import Indicator
from backend_py.services.data_handler import DataHandler

logger = logging.getLogger(__name__)

# broker_config = get_user_config()
# ab = AliceBroker(broker_config)
dh = DataHandler()
indicator = Indicator()


class IndicatorSpec(BaseModel):
    ema: bool
    emas: bool
    rsi: bool
    supertrend: bool


app = FastAPI()
templates = Jinja2Templates(
    directory='/Users/apple/Documents/Work/GitRepoLocal/react-trading-app/react-trading-app/backend-py/backend_py/templates')


def login_to_aliceblue(request) -> dict:
    cfg = get_user_config()
    try:
        alice = get_alice(dict(user_id=cfg['user_id'], api_key=cfg['api_key']))
        return dict(msg='Login Successful.', user_id=alice.user_id, session_id=alice.session_id)
    except Exception as exc:
        logger.exception(exc)
        return dict(msg='Login Failed.', exceptioin=exc.__str__())


@app.get("/")
async def root(request: Request) -> Any:
    return templates.TemplateResponse(request=request, name='index.html')


@app.get("/api/v1/alice/login")
async def login_alice(request: Request) -> dict:
    return login_to_aliceblue(request)


@app.get("/api/v1/alice/{token}/{interval}")
async def fetch_historical(token: int, interval: str) -> list:
    to_epoch = int(datetime.now().timestamp() * 1000)
    from_epoch = int(to_epoch - 1.5 * 24 * 3600 * 1000)
    res = dh.fetch_historical(token, interval, from_epoch, to_epoch)
    return res


@app.get("/api/v1/local/{token}/{interval}")
async def fetch_historical_local(token: int, interval: str) -> list:
    to_epoch = int(datetime.now().timestamp() * 1000)
    from_epoch = int(to_epoch - 1.5 * 24 * 3600 * 1000)
    with open(f'/Users/apple/Documents/Work/GitRepoLocal/react-trading-app/data/{str(token)}.json', 'r') as fp:
        data = json.load(fp)
    data = dh.convert_to_epoch(data)
    return data


@app.get("/api/v1/local/indicators/{token}/{interval}")
async def fetch_historical_local_indicators(token: int, interval: str):
    to_epoch = int(datetime.now().timestamp() * 1000)
    from_epoch = int(to_epoch - 1.5 * 24 * 3600 * 1000)
    with open(f'/Users/apple/Documents/Work/GitRepoLocal/react-trading-app/data/{str(token)}.json', 'r') as fp:
        data = json.load(fp)
    data = dh.convert_to_epoch(data)
    df = pd.DataFrame(data)

    df_ind = indicator.add_emas(df, 'close', [9, 21])
    df_ind = indicator.add_rsi(df_ind, 'close', 14)
    # data_ind = JSONResponse(df_ind.fillna(np.nan).replace([np.nan], [None]).to_dict(orient='records'))
    # data_ind = df_ind.to_dict(orient='records')
    data_ind = df_ind.fillna(np.nan).replace([np.nan], [None]).to_dict(orient='records')
    return data_ind


@app.get("/api/v1/positions")
async def positions() -> dict:
    alice = get_alice()
    return alice.get_netwise_positions()


@app.get("/api/v1/holdings")
async def holdings() -> dict:
    alice = get_alice()
    return alice.get_holding_positions()


if __name__ == "__main__":
    sys_cfg = get_system_config()
    uvicorn.run(app, host='0.0.0.0', port=8000)
