from typing import List
from pydantic import BaseSettings, Extra


class Config(BaseSettings, extra=Extra.ignore):
    report_webhook_port: int = 8081
    report_access_token: str = None
    environment: str
    superusers: List[str]
