from pydantic import BaseModel
from typing import Optional, List


class PusherClient(BaseModel):
    instance_id: str
    secret_key: str

class PusherIntegratorConfiguration(BaseModel):
    interests: List[str] # string list     1-100
    time_to_live: Optional[int]
    notification: Optional[str]
    alert: Optional[str]
    title: Optional[str]
    body: Optional[str]
    icon: Optional[str]
    deep_link: Optional[str]
    hide_notification_if_site_has_focus: Optional[bool]
    data: Optional[object] #cannot contain key "pusher"
