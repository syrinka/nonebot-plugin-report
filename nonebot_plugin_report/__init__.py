from typing import Union, Optional, List

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from nonebot import get_driver, get_bot
from nonebot.log import logger
from nonebot.drivers import ReverseDriver

from .config import Config


driver = get_driver()
config = Config.parse_obj(driver.config)

if not isinstance(driver, ReverseDriver) or not isinstance(driver.server_app, FastAPI):
    raise NotImplementedError('Only FastAPI reverse driver is supported.')


class Report(BaseModel):
    token: Optional[str] = None
    title: Optional[str] = None
    content: str
    send_to: Optional[Union[str, List[str]]] = None


app = FastAPI()

@app.post(config.report_route, status_code=200)
async def push(r: Report):
    if config.report_token is not None \
    and r.token != config.report_token:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    r.title = r.title or ''

    msg = config.report_template.format(title=r.title, content=r.content)
    if r.send_to is None:
        send_to = config.superusers
    elif isinstance(r.send_to, str):
        send_to = [r.send_to]
    else:
        send_to = r.send_to

    bot = get_bot()
    for id in send_to:
        await bot.send_msg(user_id=id, message=msg)

    logger.info(
        'Report pushed:'
        f' title={repr(r.title)},'
        f' message={repr(r.content)},'
        f' send_to={repr(r.send_to)}'
    )


@driver.on_startup
async def startup():
    if not config.report_token and config.environment == 'prod':
        logger.warning('You are in production environment without setting a token, everyone can access your webhook')

    driver.server_app.mount('/', app)
    logger.info(f'Mounted to {config.report_route}')
