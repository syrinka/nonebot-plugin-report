from typing import Optional, List, Union
from pydantic import Extra
from pydantic_settings import BaseSettings


ID = Union[str, int]

class Config(BaseSettings, extra=Extra.ignore):
    report_token: Optional[str] = None
    report_from: Optional[ID] = None
    report_route: str = '/report'
    report_template: str = '{title}\n{content}'
    environment: str
    superusers: List[str]
