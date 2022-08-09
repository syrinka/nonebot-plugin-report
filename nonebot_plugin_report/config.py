from typing import Optional, List
from pydantic import BaseSettings, Extra


class Config(BaseSettings, extra=Extra.ignore):
    report_token: Optional[str] = None
    report_route: str = '/report'
    report_template: str = '{title}\n{content}'
    environment: str
    superusers: List[str]
