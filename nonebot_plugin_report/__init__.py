from typing import Union, Optional, List

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, validator
from nonebot import get_driver, get_bot
from nonebot.log import logger
from nonebot.drivers import ReverseDriver
from nonebot.plugin import PluginMetadata

from .config import Config


__plugin_meta__ = PluginMetadata(
    name='推送钩子',
    description='实现消息推送自由',
    usage='详见项目 README.md'
)


driver = get_driver()
config = Config.parse_obj(driver.config)

if not isinstance(driver, ReverseDriver) or not isinstance(driver.server_app, FastAPI):
    raise NotImplementedError('Only FastAPI reverse driver is supported.')


ID = Union[str, int]

class Report(BaseModel):
    token: Optional[str] = None
    title: Optional[str] = None
    content: str = 'aa'
    send_to: Optional[List[ID]] = None
    send_to_group: Optional[List[ID]] = None

    def _validate(cls, v):
        print(type(v))
        if v is None or isinstance(v, list):
            return v
        else:
            return [v]

    _v_st = validator('send_to', pre=True)(_validate)
    _v_stg = validator('send_to_group', pre=True)(_validate)


app = FastAPI()

@app.post(config.report_route, status_code=200)
async def push(r: Report):
    if config.report_token is not None \
    and r.token != config.report_token:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    msg = config.report_template.format(
        title=r.title or '',
        content=r.content
    )
    bot = get_bot()

    if r.send_to is None:
        if r.send_to_group is None:
            uids = config.superusers
        else:
            uids = []
    else:
        uids = r.send_to

    for uid in uids:
        await bot.send_msg(user_id=uid, message=msg, message_type='private')

    if r.send_to_group is None:
        gids = []
    else:
        gids = r.send_to_group

    for gid in gids:
        await bot.send_msg(group_id=gid, message=msg, message_type='group')

    logger.info(
        'Report pushed:'
        f' title={repr(r.title)},'
        f' content={repr(r.content)},'
        f' send_to={repr(r.send_to)}'
    )


@driver.on_startup
async def startup():
    if not config.report_token and config.environment == 'prod':
        logger.warning('You are in production environment without setting a token')

    driver.server_app.mount('/', app)
    logger.info(f'Mounted to {config.report_route}')
