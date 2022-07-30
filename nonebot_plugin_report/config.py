from typing import List
from pydantic import BaseSettings, Extra


class Config(BaseSettings, extra=Extra.ignore):
    report_token: str = None
    report_route: str = '/report'
    environment: str
    superusers: List[str]
