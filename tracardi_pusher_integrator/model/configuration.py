from pydantic import BaseModel
from typing import Optional


class PusherClient(BaseModel):
    instance_id: str
    secret_key: str

        
class PusherPlatform(BaseModel):
    web: bool
    ios: bool
    android: bool


class PusherConfiguration(BaseModel):
    interests: Optional[list]
    user_ids: Optional[list]

    title: str
    body: str
    data: Optional[dict]

    time_to_live: Optional[int]
    icon: Optional[str]
    deep_link: Optional[str]
    hide_notification_if_site_has_focus: Optional[bool]
