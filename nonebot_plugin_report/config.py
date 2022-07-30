from typing import Optional, List
from pydantic import BaseSettings, Extra


class Config(BaseSettings, extra=Extra.ignore):
    report_token: Optional[str]
    report_route: Optional[str] = '/report'
    environment: str
    superusers: List[str]
