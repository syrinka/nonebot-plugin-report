from typing import Union, Optional, List

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field, validator, root_validator
from nonebot import get_plugin_config, get_bot, get_driver
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
config = get_plugin_config(Config)

if not isinstance(driver, ReverseDriver) or not isinstance(driver.server_app, FastAPI):
    raise NotImplementedError('Only FastAPI reverse driver is supported.')


ID = Union[str, int]

class Report(BaseModel):
    token: Optional[str] = Field(None, exclude=True)
    title: Optional[str] = None
    content: str
    send_from: Optional[ID] = None
    send_to: Optional[List[ID]] = None
    send_to_group: Optional[List[ID]] = None

    @root_validator(pre=True)
    def _aliases(cls, v):
        if v.get('send_from') is None:
            v['send_from'] = v.get('from')
        if v.get('send_to') is None:
            v['send_to'] = v.get('to')
        if v.get('send_to_group') is None:
            v['send_to_group'] = v.get('to_group')
        return v

    def _validate(cls, v):
        if v is None or isinstance(v, list):
            return v
        else:
            return [v]

    _v_st = validator('send_to', pre=True, allow_reuse=True)(_validate)
    _v_stg = validator('send_to_group', pre=True, allow_reuse=True)(_validate)


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
    try:
        bot = get_bot(r.send_from or config.report_from)
    except KeyError:
        logger.warning(f'No bot with specific id: {r.send_from}')
        return
    except ValueError:
        logger.warning('No bot available or driver not initialized')
        return

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
        f'Report pushed: {r.json()}'
    )


@driver.on_startup
async def startup():
    if not config.report_token and config.environment == 'prod':
        logger.warning('You are in production environment without setting a token')

    driver.server_app.mount('/', app)
    logger.info(f'Mounted to {config.report_route}')
