import os

from typing import TypedDict


class OcTranspoConfig(TypedDict):
    app_id: str
    api_key: str
    format: str


OC_TRANSPO: OcTranspoConfig = {
    "app_id": os.environ["OC_TRANSPO_APP_ID"],
    "api_key": os.environ["OC_TRANSPO_APP_KEY"],
    "format": "json",
}
