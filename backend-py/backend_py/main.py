from typing import Any
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import logging
from broker.broker_alice import get_alice

from backend_py.config.config import get_server_config, get_system_config, get_user_config

logger = logging.getLogger(__name__)

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


@app.get("/apis/broker/login/aliceblue")
async def login_alice(request: Request) -> dict:
    return login_to_aliceblue(request)


@app.get("/positions")
async def positions() -> dict:
    alice = get_alice()
    return alice.get_netwise_positions()


@app.get("/holdings")
async def holdings() -> dict:
    alice = get_alice()
    return alice.get_holding_positions()

if __name__ == "__main__":
    sys_cfg = get_system_config()
    uvicorn.run(app, host='0.0.0.0', port=8000)
