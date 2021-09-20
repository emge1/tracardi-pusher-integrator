from pydantic import BaseModel
from typing import Optional


class PusherClient(BaseModel):
    instance_id: str
    secret_key: str

class PusherIntegratorConfiguration(BaseModel):
    interests: Optional[list]
    user_ids: Optional[list]
    time_to_live: Optional[int]
    title: Optional[str]
    body: Optional[str]
    icon: Optional[str]
    deep_link: Optional[str]
    hide_notification_if_site_has_focus: Optional[bool]
    data: Optional[dict]